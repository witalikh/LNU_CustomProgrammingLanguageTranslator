from typing import Tuple, Union, TypedDict, Unpack

from .._syntax.operators import OperatorMethods, Operator

from ..abstract_syntax_tree import (
    ASTNode, TypeNode, TypeCategory,
    ClassDefNode, ClassFieldDeclarationNode,
    LiteralNode, FloatLiteralNode, IntegerLiteralNode, StringLiteralNode,
    ByteStringLiteralNode, BooleanLiteralNode,
    NullLiteralNode, UndefinedLiteralNode, KeymapLiteralNode, ListLiteralNode,
    CharLiteralNode, TypeLiteral, ImaginaryFloatLiteralNode, EmptyLiteralNode, KeymapElementNode,
    BinaryOperatorABCNode,
    UnaryOperatorABCNode,
    MemberOperatorNode,
    FunctionCallNode, IndexNode,
    IdentifierNode,
    AssignmentNode,
    ThisNode,
    IntegerSizes, FloatSizes,
)
from ..semantics import TypeEnum

from ._type_cast import common_base, common_primitive_type
from ._type_match import match_types
from .._syntax.operators import Assignment

from .shared import error_logger

from ._helpers_class import get_class_method, get_class_field, get_class_by_name, instantiate_generic_type
from ._helpers_function import get_function


class _ContextParams(TypedDict):
    outermost: bool
    context_class: ClassDefNode | None
    is_nonstatic_method: bool


def check_arithmetic_expression(
    expression: ASTNode,
    environment: dict[str, TypeNode],
    outermost: bool = False,
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    allow_compound_constructor = context.pop('allow_compound_constructor', False)
    if isinstance(expression, LiteralNode):
        valid_expr, expr_type = _check_primitive_literal(literal=expression, environment=environment, **context)
        expression.valid = valid_expr
        return valid_expr, expr_type

    elif isinstance(expression, BinaryOperatorABCNode):
        valid_expr, expr_type = _check_binary_operator(expression=expression, environment=environment, **context)
        expression.valid = valid_expr
        return valid_expr, expr_type

    elif isinstance(expression, UnaryOperatorABCNode):
        valid_expr, expr_type = _check_unary_operator(unary_op_expr=expression, environment=environment, **context)
        expression.valid = valid_expr
        return valid_expr, expr_type

    elif isinstance(expression, MemberOperatorNode):
        valid_expr, expr_type = _check_member(expression=expression, environment=environment, **context)
        expression.valid = valid_expr
        return valid_expr, expr_type

    elif isinstance(expression, FunctionCallNode):
        valid_expr, expr_type = _get_type_of_function_call(expression=expression, environment=environment, **context)
        expression.valid = valid_expr
        return valid_expr, expr_type

    elif isinstance(expression, IndexNode):
        res = _get_type_of_indexation_call(
            expression=expression, environment=environment, **context,
            allow_compound_constructor=allow_compound_constructor
        )
        if len(res) == 2:
            valid_expr, expr_type = res
        elif len(res) == 3:
            valid_expr, expr_type, _num = res
            expression.is_overload = True
            expression.overload_number = _num
        else:
            # unreachable
            return False, None
        expression.valid = valid_expr
        return valid_expr, expr_type

    elif isinstance(expression, IdentifierNode):
        valid_expr, expr_type = _get_type_of_identifier(expression=expression, environment=environment, **context)
        expression.valid = valid_expr
        return valid_expr, expr_type

    elif isinstance(expression, ThisNode):
        valid_expr, expr_type = _check_this_literal(expression=expression, environment=environment, **context)
        expression.valid = valid_expr
        return valid_expr, expr_type

    elif isinstance(expression, AssignmentNode):
        valid_expr, expr_type = _check_assignment(expression=expression, environment=environment, **context, outermost=outermost)
        expression.valid = valid_expr
        return valid_expr, expr_type
    else:
        # print(expression)
        error_logger.add(
            location=expression.location,
            reason="Unexpected expression"
        )
        return False, None


def _check_assignment(
    expression: AssignmentNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, TypeNode | None]:
    outermost = context.pop("outermost", False)
    if not outermost:
        error_logger.add(
            location=expression.location,
            reason="Unexpected place for assignment expression"
        )
        return False, None

    if not isinstance(expression.left, (IndexNode, IdentifierNode, MemberOperatorNode)):
        error_logger.add(
            location=expression.location,
            reason=f"Invalid expression to assign into: {type(expression.left).__name__}"
        )
        return False, None

    valid_left_expr, left_expr_type = check_arithmetic_expression(
        expression=expression.left, environment=environment, **context
    )
    valid_right_expr, right_expr_type = check_arithmetic_expression(
        expression=expression.right, environment=environment, **context, outermost=outermost
    )

    if not (valid_left_expr and valid_right_expr):
        # error is already logged
        return False, None

    if not match_types(current_type=right_expr_type, target_type=left_expr_type):
        error_logger.add(
            location=expression.location,
            reason=f"Type assignment mismatch: {left_expr_type.name} != {right_expr_type.name}"
        )
        return False, None

    if left_expr_type.is_reference and expression.operator == Assignment.VALUE_ASSIGNMENT:
        error_logger.add(
            location=expression.location,
            reason="Invalid assignment operator for reference: ':='"
        )
        return False, None

    if not left_expr_type.is_reference and expression.operator == Assignment.REFERENCE_ASSIGNMENT:
        error_logger.add(
            location=expression.location,
            reason="Invalid assignment operator for value: '='"
        )
        return False, None

    return True, left_expr_type


def _check_this_literal(
    expression: ThisNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    context_class: ClassDefNode | None = context.get("context_class")
    is_nonstatic_method = context.get("is_nonstatic_method", False)

    if context_class and is_nonstatic_method:
        return True, TypeNode(
            TypeCategory.CLASS if not context_class.generic_params else TypeCategory.GENERIC_CLASS,
            IdentifierNode(context_class.name, *context_class.location),
            context_class.generic_params,
            *context_class.location
        )
    error_logger.add(
        location=expression.location,
        reason="Invalid context for using this keyword"
    )
    return False, None


def _check_member(
    expression: MemberOperatorNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    """
    Checks if the MembershipOperatorNode is valid and returns a field
    :param expression:
    :param environment:
    :return:
    """
    # right operand of membership operator should be parsed as identifier no matter what
    if not isinstance(expression.right, IdentifierNode):
        print(expression)
        raise AssertionError(f"Unexpected expression: {type(expression.right)}")

    member_name = expression.right.name
    operator = expression.operator
    valid, class_type = check_arithmetic_expression(expression=expression.left, environment=environment, **context)

    if not valid:
        # error is logged by this point
        return False, None

    if class_type is None:
        error_logger.add(
            location=expression.location,
            reason=f"Invalid expression on the left side of the membership {operator} operator"
        )
        return False, None
    else:
        expression.associated_class = class_type

    class_instance = get_class_by_name(
        class_name=class_type.name
    )

    class_field: ClassFieldDeclarationNode = get_class_field(
        _class=class_instance,
        field_name=member_name
    )

    if class_field is None:
        error_logger.add(
            location=expression.location,
            reason=f"Field {member_name} of the class {class_type.name} does not exist"
        )
        expression.right.valid = False
        return False, None
    else:
        expression.right.valid = True

    is_valid, return_type = instantiate_generic_type(
        possibly_generic_type=class_field.type,
        class_instance=class_instance,
        generic_args=class_type.arguments
    )

    if not is_valid:
        error_logger.add(
            location=expression.location,
            reason="Invalid return type"
        )
        return False, None

    class_field.use()
    return True, return_type


def _check_binary_operator(
    expression: BinaryOperatorABCNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    lhs_valid, lhs_type = check_arithmetic_expression(expression=expression.left, environment=environment, **context)
    rhs_valid, rhs_type = check_arithmetic_expression(expression=expression.right, environment=environment, **context)
    operator = expression.operator

    if not (lhs_valid and rhs_valid):
        # error is already logged
        return False, None

    if expression.is_arithmetic:
        res = __get_type_of_arithmetic_binary_operator(lhs_type=lhs_type, rhs_type=rhs_type, operator=operator, location=expression.location)
        if len(res) == 2:
            return res
        elif len(res) == 3:
            _valid, _type, _num = res
            expression.is_overload = True
            expression.overload_number = _num
            return _valid, _type
        else:
            # unreachable
            return False, None

    elif expression.is_logical:
        return __get_type_of_logical_binary_operator(lhs_type=lhs_type, rhs_type=rhs_type, operator=operator, location=expression.location)
    elif expression.is_comparison:
        res = __get_type_of_comparison_binary_operator(lhs_type=lhs_type, rhs_type=rhs_type, operator=operator, location=expression.location)
        if len(res) == 2:
            return res
        elif len(res) == 3:
            _valid, _type, _num = res
            expression.is_overload = True
            expression.overload_number = _num
            return _valid, _type
        else:
            # unreachable
            return False, None
    elif expression.is_casting:
        if not isinstance(expression.right, TypeNode):
            error_logger.add(
                location=expression.location,
                reason="Invalid type to cast"
            )
            return False, None
        return True, expression.right
    elif expression.is_coalesce:
        return check_arithmetic_expression(expression=expression.left, environment=environment, **context)
    else:
        error_logger.add(
            location=expression.location,
            reason="Unsupported expression"
        )
        return False, None


def ___get_type_of_overloaded_operator(
    signature: list[TypeNode],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]] | Tuple[bool, Union[TypeNode, None], int]:
    if not OperatorMethods.overloadable(operator) and operator not in ["call", "index"]:
        error_logger.add(
            location=location,
            reason=f"Operator {operator} is not overridable and cannot be applied to this types"
        )
        return False, None

    if OperatorMethods.overloadable(operator):
        function_name = f"$operator_{OperatorMethods.translate(operator, 2)}"
    else:
        function_name = f"$operator_{operator}"
    is_valid, function_node = get_function(func_name=function_name, args_signature=signature)

    if not is_valid or function_node is None:
        error_logger.add(
            location=location,
            reason=f"Operator {operator} is overridable, but no override definition found"
        )
        return False, None

    if not isinstance(function_node.external_to, ClassDefNode):
        error_logger.add(
            location=location,
            reason="Operator overload is not associated to some class"
        )
        return False, None

    # TODO: support operator overloading for generics
    # TODO: deduce generic args
    is_valid, return_type = instantiate_generic_type(
        possibly_generic_type=function_node.return_type,
        class_instance=function_node.external_to,
        generic_args=[]
    )

    if not is_valid:
        error_logger.add(
            location=location,
            reason="Failed to deduce return type for operator overload"
        )
        return False, None

    return True, return_type, function_node.overload_number


def __get_type_of_arithmetic_binary_operator(
    lhs_type: Union[TypeNode, None],
    rhs_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if lhs_type.category == rhs_type.category == TypeCategory.PRIMITIVE:
        common_type = common_primitive_type(left_type=lhs_type.name, right_type=rhs_type.name)
        if operator == Operator.DIVIDE:
            common_type = common_primitive_type(left_type=lhs_type.name, right_type=TypeEnum.FLOAT)

        if common_type is None:
            error_logger.add(
                location=location,
                reason=f"Unsupported operation {operator} for types {lhs_type.name} and {rhs_type.name}"
            )
            return False, None

        if lhs_type.name == common_type:
            return True, lhs_type
        else:
            return True, rhs_type
    elif (
        (lhs_type.category == TypeCategory.PRIMITIVE and rhs_type.type == TypeCategory.COLLECTION) or
        (lhs_type.category == TypeCategory.COLLECTION and rhs_type.category == TypeCategory.PRIMITIVE)
    ):
        error_logger.add(
            location=location,
            reason=f"Unsupported operation {operator} for types {lhs_type.name} and {rhs_type.name}"
        )
        return False, None

    elif lhs_type.category == rhs_type.category == TypeCategory.COLLECTION:
        if lhs_type.type != rhs_type.type:
            error_logger.add(
                location=location,
                reason=f"Unsupported operation {operator} for types {lhs_type.name} and {rhs_type.name}"
            )
            return False, None

        if lhs_type.type == TypeEnum.KEYMAP:
            error_logger.add(
                location=location,
                reason=f"Unsupported operation {operator} for type {lhs_type.name}"
            )
            return False, None

        common_type = common_base(left_type=lhs_type, right_type=rhs_type)
        if common_type is None:
            error_logger.add(
                location=location,
                reason=f"Unsupported operation {operator} for types {lhs_type.name} and {rhs_type.name}"
            )
            return False, None
        return True, common_type

    else:
        return ___get_type_of_overloaded_operator(signature=[lhs_type, rhs_type], operator=operator, location=location)


def __get_type_of_logical_binary_operator(
    lhs_type: Union[TypeNode, None],
    rhs_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if not (lhs_type.type == rhs_type.type == TypeEnum.BOOLEAN):
        error_logger.add(
            location=location,
            reason=f"Operator {operator} supports only boolean types"
        )
        return False, None
    return True, lhs_type


def __get_type_of_comparison_binary_operator(
    lhs_type: Union[TypeNode, None],
    rhs_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:

    numeric_types = (
        TypeEnum.BYTE,
        TypeEnum.SHORT_INTEGER,
        TypeEnum.INTEGER,
        TypeEnum.LONG_INTEGER,
        TypeEnum.EXTENDED_INTEGER,
        TypeEnum.FLOAT,
        TypeEnum.DOUBLE,
        TypeEnum.COMPLEX
    )
    if lhs_type.type in numeric_types and rhs_type.type in numeric_types:
        return True, TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.BOOLEAN, *lhs_type.location),
            None,
            *lhs_type.location
        )
    else:
        return ___get_type_of_overloaded_operator(signature=[lhs_type, rhs_type], operator=operator, location=location)


def _check_unary_operator(
    unary_op_expr: UnaryOperatorABCNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    allow_compound_constructor = (unary_op_expr.operator == Operator.NEW_INSTANCE)

    valid_expr, expression_type = check_arithmetic_expression(
        expression=unary_op_expr.expression, environment=environment, **context,
        allow_compound_constructor=allow_compound_constructor
    )
    operator = unary_op_expr.operator
    if unary_op_expr.is_arithmetic:
        res = __get_type_of_arithmetic_unary_operator(expression_type=expression_type, operator=operator, location=unary_op_expr.location)
        if len(res) == 2:
            return res
        elif len(res) == 3:
            _valid, _type, _num = res
            unary_op_expr.is_overload = True
            unary_op_expr.overload_number = _num
            return _valid, _type
        else:
            # unreachable
            return False, None

    elif unary_op_expr.is_allocation:
        return __get_type_of_allocation_unary_operator(expression_type=expression_type, operator=operator, location=unary_op_expr.location)

    elif unary_op_expr.is_logical:
        return __get_type_of_logical_unary_operator(expression_type=expression_type, operator=operator, location=unary_op_expr.location)

    elif unary_op_expr.is_reference:
        return __get_type_of_reference_unary_operator(expression_type=expression_type, operator=operator, location=unary_op_expr.location)

    else:
        error_logger.add(
            location=unary_op_expr.location,
            reason="Unsupported expression"
        )
        return False, None


def __get_type_of_arithmetic_unary_operator(
    expression_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if expression_type.category == TypeCategory.PRIMITIVE:
        compatible_type = common_primitive_type(left_type=expression_type.name, right_type=TypeEnum.BYTE)
        if compatible_type is None:
            error_logger.add(
                location=location,
                reason=f"Unsupported unary operation {operator} for types {expression_type.name}"
            )
            return False, None
        return True, expression_type

    elif expression_type.category == TypeCategory.COLLECTION:
        error_logger.add(
            location=location,
            reason=f"Unsupported unary operation {operator} for types {expression_type.name}"
        )
        return False, None

    else:
        return ___get_type_of_overloaded_operator(signature=[expression_type], operator=operator, location=location)


def __get_type_of_logical_unary_operator(
    expression_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if expression_type.type != TypeEnum.BOOLEAN:
        error_logger.add(
            location=location,
            reason=f"Operator {operator} supports only boolean types"
        )
        return False, None
    return True, expression_type


def __get_type_of_allocation_unary_operator(
    expression_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if expression_type is None:
        error_logger.add(
            location=location,
            reason="Unsupported expression for allocation before even checking"
        )
        return False, None

    # TODO: complex check
    if operator == Operator.NEW_INSTANCE:
        return True, expression_type
    elif operator == Operator.DELETE_INSTANCE:
        return True, None
    else:
        error_logger.add(
            location=location,
            reason="Unsupported expression for allocation"
        )
        return False, None


def __get_type_of_reference_unary_operator(
    expression_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if operator == Operator.REFERENCE:
        if expression_type.is_reference:
            error_logger.add(
                location=location,
                reason="Cannot reference already referenced type"
            )
            return False, None
        copy = expression_type.shallow_copy()
        copy.set_reference()
        return True, copy
    elif operator == Operator.DEREFERENCE:
        error_logger.add(
            location=location,
            reason="Cannot dereference non-reference type"
        )
        if not expression_type.is_reference:
            return False, None
        copy = expression_type.shallow_copy()
        copy.unset_reference()
        return True, copy
    else:
        error_logger.add(
            location=location,
            reason="Unsupported expression"
        )
        return False, None


def _get_type_of_identifier(
    expression: IdentifierNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    maybe_local_var = environment.get(expression.name)
    if maybe_local_var is not None:
        return True, maybe_local_var

    # function name, class name...
    error_logger.add(
        location=expression.location,
        reason=f"Unresolved reference for {expression.name}"
    )
    return False, None


def _get_type_of_function_call(
    expression: FunctionCallNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:

    function_id = expression.identifier
    if isinstance(function_id, MemberOperatorNode):
        return __get_method_call(expression=expression, environment=environment, **context)

    elif isinstance(function_id, IdentifierNode):
        return __get_function_call(expression=expression, environment=environment, **context)

    elif isinstance(function_id, TypeNode):
        return __get_constructor_call(expression=expression, environment=environment, **context)

    # Assume no static, functors etc
    else:
        error_logger.add(
            location=expression.location,
            reason="Unsupported expression"
        )
        return False, None


def __get_method_call(
    expression: FunctionCallNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    function_id: MemberOperatorNode = expression.identifier
    valid, class_type_node = check_arithmetic_expression(expression=function_id, environment=environment, **context)
    if not valid:
        # error is already logged
        return False, None

    if not isinstance(class_type_node, TypeNode):
        error_logger.add(
            location=expression.location,
            reason="Invalid expression for method call"
        )
        return False, None
    else:
        expression.identifier.associated_class = class_type_node

    potentially_method_name = function_id.right
    if not isinstance(potentially_method_name, IdentifierNode):
        error_logger.add(
            location=expression.location,
            reason=f"Invalid expression for method name: {type(potentially_method_name).__name__}"
        )
        return False, None

    if class_type_node.category not in (TypeCategory.CLASS, TypeCategory.GENERIC_CLASS):
        error_logger.add(
            location=expression.location,
            reason=f"Invalid type: {class_type_node.type}"
        )
        return False, None

    args_signature = []
    for arg in expression.arguments:
        valid_arg, arg_type = check_arithmetic_expression(expression=arg, environment=environment, **context)
        if not valid_arg:
            # error is already logged
            return False, None
        args_signature.append(arg_type)

    class_instance = get_class_by_name(
        class_name=class_type_node.name
    )

    class_method = get_class_method(
        _class=class_instance,
        method_name=potentially_method_name.name,
        type_signature=args_signature)

    if not class_method:
        error_logger.add(
            location=expression.location,
            reason=f"Invalid type: method {potentially_method_name.name} doesn't exist"
        )
        return False, None

    is_valid, return_type = instantiate_generic_type(
        possibly_generic_type=class_method.return_type,
        class_instance=class_instance,
        generic_args=class_type_node.arguments
    )
    if not is_valid:
        error_logger.add(
            location=expression.location,
            reason="Invalid return type"
        )
        return False, None

    expression.overload_number = class_method.overload_number
    class_method.use()
    return True, return_type


def __get_function_call(
    expression: FunctionCallNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    function_id: IdentifierNode = expression.identifier
    args_signature = []
    for arg in expression.arguments:
        valid_arg, arg_type = check_arithmetic_expression(expression=arg, environment=environment, **context)
        if not valid_arg:
            # error is already logged
            return False, None
        args_signature.append(arg_type)

    is_valid, function_node = get_function(func_name=function_id.name, args_signature=args_signature)
    if not is_valid or function_node is None:
        error_logger.add(
            location=expression.location,
            reason=f"Invalid function: {function_id.name}"
        )
        return False, None

    expression.overload_number = function_node.overload_number
    function_node.use()
    return True, function_node.return_type


def __get_constructor_call(
    expression: FunctionCallNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
):
    function_id: TypeNode = expression.identifier
    args_signature = []
    for arg in expression.arguments:
        valid_arg, arg_type = check_arithmetic_expression(expression=arg, environment=environment, **context)
        if not valid_arg:
            # error is already logged
            return False, None
        args_signature.append(arg_type)

    # TODO: generic constructor
    class_node = get_class_by_name(function_id.name)
    if not class_node:
        error_logger.add(
            location=expression.location,
            reason=f"Class {function_id.name} doesn't exist!"
        )
        return False, None

    constructor_node = get_class_method(function_id.name, "$constructor", args_signature, False)
    if constructor_node is None:
        error_logger.add(
            location=expression.location,
            reason=f"Invalid constructor for class {function_id.name}"
        )
        return False, None

    expression.overload_number = constructor_node.overload_number
    constructor_node.use()
    return True, TypeNode(
        TypeCategory.CLASS,
        IdentifierNode(class_node.name, *expression.location),
        None,
        *expression.location
    )


def _get_type_of_indexation_call(
    expression: IndexNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    allow_compound_constructor = context.pop('allow_compound_constructor', False)
    valid_expr, expression_type = check_arithmetic_expression(expression=expression.variable, environment=environment, **context)

    if not valid_expr:
        # error is already logged
        return False, None

    if expression_type.category == TypeCategory.PRIMITIVE:
        error_logger.add(
            location=expression.location,
            reason=f"Invalid type: {expression_type.name}"
        )
        return False, None

    elif expression_type.category == TypeCategory.COLLECTION:
        if expression_type.name not in (TypeEnum.ARRAY, TypeEnum.KEYMAP):
            error_logger.add(
                location=expression.location,
                reason=f"Invalid type: {expression_type.name}"
            )
            return False, None

    argument_signature = [expression_type]
    for arg in expression.arguments:
        valid, arg_type = check_arithmetic_expression(expression=arg, environment=environment, **context)
        if not valid:
            error_logger.add(
                location=arg.location,
                reason="Invalid expression"
            )
            return False, None
        argument_signature.append(arg_type)

    if expression_type.category == TypeCategory.COLLECTION:

        if not expression_type.arguments:
            error_logger.add(
                location=expression.location,
                reason="Invalid collection: no containing type provided"
            )
            return False, None

        if len(argument_signature) == 0:
            error_logger.add(
                location=expression.location,
                reason="No argument provided for collection type"
            )
        if len(argument_signature) > 1:
            if True:
                error_logger.add(
                    location=expression.location,
                    reason="Too many arguments for collection type"
                )
        if expression_type.name == TypeEnum.ARRAY:
            cpt = common_primitive_type(left_type=argument_signature[1].name, right_type=TypeEnum.INTEGER)
            if not cpt or cpt != TypeEnum.INTEGER:
                error_logger.add(
                    location="Non-integer type argument provided for array type in index"
                )
                return False, None

            return True, expression_type.arguments[0]

        else:
            cpt = common_primitive_type(left_type=argument_signature[1].name, right_type=expression_type.arguments[0].name)
            if not cpt:
                error_logger.add(
                    location="Incompatible type argument provided for keymap type in index"
                )
                return False, None

            return True, expression_type.arguments[1]
    else:
        return ___get_type_of_overloaded_operator(signature=argument_signature, operator="index", location=expression.location)


def _check_primitive_literal(
    literal: LiteralNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    if isinstance(literal, IntegerLiteralNode):
        match literal.size:
            case IntegerSizes.BYTE:
                type_of_literal = TypeEnum.BYTE
            case IntegerSizes.SHORT:
                type_of_literal = TypeEnum.SHORT_INTEGER
            case IntegerSizes.INTEGER:
                type_of_literal = TypeEnum.INTEGER
            case IntegerSizes.LONG:
                type_of_literal = TypeEnum.LONG_INTEGER
            case IntegerSizes.EXTENDED:
                type_of_literal = TypeEnum.EXTENDED_INTEGER
            case _:
                raise ValueError(f"Invalid literal type: {literal.size}")

        return True, TypeNode(
            category=TypeCategory.PRIMITIVE,
            type_node=TypeLiteral(type_of_literal, *literal.location),
            args=None,
            line=literal.location[0], position=literal.location[1],
            _literal=True,

        )
    elif isinstance(literal, FloatLiteralNode):
        match literal.size:
            case FloatSizes.FLOAT:
                type_of_literal = TypeEnum.FLOAT
            case FloatSizes.DOUBLE:
                type_of_literal = TypeEnum.DOUBLE
            case _:
                raise ValueError(f"Invalid literal type: {literal.size}")

        return True, TypeNode(
            category=TypeCategory.PRIMITIVE,
            type_node=TypeLiteral(type_of_literal, *literal.location),
            args=None,
            line=literal.location[0], position=literal.location[1],
            _literal=True,
        )
    elif isinstance(literal, ImaginaryFloatLiteralNode):
        return True, TypeNode(
            category=TypeCategory.PRIMITIVE,
            type_node=TypeLiteral(TypeEnum.COMPLEX, *literal.location),
            args=None,
            line=literal.location[0], position=literal.location[1],
            _literal=True,
        )
    elif isinstance(literal, StringLiteralNode):
        return True, TypeNode(
            category=TypeCategory.PRIMITIVE,
            type_node=TypeLiteral(TypeEnum.STRING, *literal.location),
            args=None,
            line=literal.location[0], position=literal.location[1],
            _literal=True,
        )
    elif isinstance(literal, BooleanLiteralNode):
        return True, TypeNode(
            category=TypeCategory.PRIMITIVE,
            type_node=TypeLiteral(TypeEnum.BOOLEAN, *literal.location),
            args=None,
            line=literal.location[0], position=literal.location[1],
            _literal=True,
        )
    elif isinstance(literal, ByteStringLiteralNode):
        return True, TypeNode(
            category=TypeCategory.PRIMITIVE,
            type_node=TypeLiteral(TypeEnum.BYTESTRING, *literal.location),
            args=None,
            line=literal.location[0], position=literal.location[1],
            _literal=True,
        )
    elif isinstance(literal, NullLiteralNode):
        return True, TypeNode(
            category=TypeCategory.PRIMITIVE,
            type_node=TypeLiteral(TypeEnum.NULL, *literal.location),
            args=None,
            line=literal.location[0], position=literal.location[1],
            _literal=True,
        )
    elif isinstance(literal, UndefinedLiteralNode):
        return True, TypeNode(
            category=TypeCategory.PRIMITIVE,
            type_node=TypeLiteral(TypeEnum.UNDEFINED, *literal.location),
            args=None,
            line=literal.location[0], position=literal.location[1],
            _literal=True,
        )
    elif isinstance(literal, CharLiteralNode):
        return True, TypeNode(
            category=TypeCategory.PRIMITIVE,
            type_node=TypeLiteral(TypeEnum.CHAR, *literal.location),
            args=None,
            line=literal.location[0], position=literal.location[1],
            _literal=True,
        )

    elif isinstance(literal, ListLiteralNode):
        elements: list[TypeNode] = []
        for arg in literal.elements:
            valid_arg, arg_type = check_arithmetic_expression(expression=arg, environment=environment, **context)
            if not valid_arg:
                # error is already logged
                return False, None
            elements.append(arg_type)

        if len(elements) == 0:
            raise AssertionError("Tree shouldn't be parsed like that")

        common_compatible_type = elements[0]

        if len(elements) > 1:
            for element in elements:
                common_compatible_type = common_base(left_type=element, right_type=common_compatible_type)
                if common_compatible_type is None:
                    error_logger.add(
                        location=element.location,
                        reason="Type inconsistency in list/array literal"
                    )
                    return False, None

        return True, TypeNode(
            category=TypeCategory.COLLECTION,
            type_node=TypeLiteral(TypeEnum.ARRAY, *literal.location),
            args=[common_compatible_type],
            line=literal.location[0], position=literal.location[1],
            _literal=True,
        )

    elif isinstance(literal, KeymapLiteralNode):
        elements: list[tuple[TypeNode, TypeNode]] = []
        for arg in literal.elements:
            valid_arg, arg_type = __check_keymap_literal(arg=arg, environment=environment, **context)
            if not valid_arg:
                # error is already logged
                return False, None
            elements.append(arg_type)

        if len(elements) == 0:
            raise AssertionError("Tree shouldn't be parsed like that")

        common_compatible_key_type, common_compatible_value_type = elements[0]

        if len(elements) > 1:
            for element in elements:
                common_compatible_key_type = common_base(left_type=element[0], right_type=common_compatible_key_type)
                common_compatible_value_type = common_base(left_type=element[1], right_type=common_compatible_value_type)
                if common_compatible_key_type is None or common_compatible_value_type is None:
                    error_logger.add(
                        location=element[0].location,
                        reason="Type inconsistency in keymap literal"
                    )
                    return False, None

        return True, TypeNode(
            category=TypeCategory.COLLECTION,
            type_node=TypeLiteral(name=TypeEnum.ARRAY, *literal.location),
            args=[common_compatible_key_type, common_compatible_value_type],
            line=literal.location[0], position=literal.location[1],
            _literal=True,
        )

    elif isinstance(literal, EmptyLiteralNode):
        # special case: can be any empty sequence
        return True, TypeNode(
            category=TypeCategory.COLLECTION,
            type_node=TypeLiteral(name=TypeEnum.ARRAY, *literal.location),
            args=None,
            line=literal.location[0], position=literal.location[1],
            _literal=True
        )
    else:
        return False, None


def __check_keymap_literal(
    arg: KeymapElementNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> tuple[bool, tuple[TypeNode, TypeNode] | None]:
    valid_key, key_type = check_arithmetic_expression(expression=arg.left, environment=environment, **context)
    valid_value, value_type = check_arithmetic_expression(expression=arg.right, environment=environment, **context)

    if not valid_key or not valid_value:
        return False, None

    return True, (key_type, value_type)
