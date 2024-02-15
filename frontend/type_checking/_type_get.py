from typing import Tuple, Union, TypedDict, Unpack

from ..abstract_syntax_tree import *
from ..semantics import TypeEnum, POSSIBLE_OVERLOAD_OPERATORS, OPERATOR_NAMES

from ._type_cast import common_base, common_primitive_type
from ._type_match import match_types
from ..syntax import Operator, Assignment

from .shared import error_logger

from ._helpers_class import get_class_method, get_class_field, get_class_by_name, instantiate_generic_type
from ._helpers_function import get_function


class _ContextParams(TypedDict):
    outermost: bool
    context_class: ClassDefinitionNode | None
    is_nonstatic_method: bool


def check_arithmetic_expression(
    expression: ASTNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    outermost = context.pop("outermost", False)

    if isinstance(expression, LiteralNode):
        return _check_primitive_literal(expression, environment, **context)

    elif isinstance(expression, BinaryOperatorNode):
        return _check_binary_operator(expression, environment, **context)

    elif isinstance(expression, UnaryOperatorNode):
        return _check_unary_operator(expression, environment, **context)

    elif isinstance(expression, MemberOperatorNode):
        return _check_member(expression, environment, **context)

    elif isinstance(expression, FunctionCallNode):
        return _get_type_of_function_call(expression, environment, **context)

    elif isinstance(expression, IndexNode):
        return _get_type_of_indexation_call(expression, environment, **context)

    elif isinstance(expression, IdentifierNode):
        return _get_type_of_identifier(expression, environment, **context)

    elif isinstance(expression, ThisNode):
        return _check_this_literal(expression, environment, **context)

    elif isinstance(expression, AssignmentNode):
        return _check_assignment(expression, environment, **context, outermost=outermost)
    else:
        error_logger.add(
            expression.location,
            f"Unexpected expression"
        )
        return False, None


def _check_assignment(
    expression: AssignmentNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
):
    outermost = context.pop("outermost", False)
    if not outermost:
        error_logger.add(
            expression.location,
            f"Unexpected place for assignment expression"
        )
        return False, None

    if not isinstance(expression.left, (IndexNode, IdentifierNode, MemberOperatorNode)):
        error_logger.add(
            expression.location,
            f"Invalid expression to assign into: {expression.left.__class__.__name__}"
        )
        return False, None

    valid_left_expr, left_expr_type = check_arithmetic_expression(
        expression.left, environment, **context
    )
    valid_right_expr, right_expr_type = check_arithmetic_expression(
        expression.right, environment, **context, outermost=outermost
    )

    if not (valid_left_expr and valid_right_expr):
        # error is already logged
        return False, None

    if not match_types(right_expr_type, left_expr_type):
        error_logger.add(
            expression.location,
            f"Type assignment mismatch: {left_expr_type.name} != {right_expr_type.name}"
        )
        return False, None

    if left_expr_type.is_reference and expression.operator == Assignment.VALUE_ASSIGNMENT:
        error_logger.add(
            expression.location,
            f"Invalid assignment operator for reference: ':='"
        )
        return False, None

    if not left_expr_type.is_reference and expression.operator == Assignment.REFERENCE_ASSIGNMENT:
        error_logger.add(
            expression.location,
            f"Invalid assignment operator for value: '='"
        )
        return False, None

    return True, left_expr_type


def _check_this_literal(
    expression: ThisNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    context_class: ClassDefinitionNode | None = context.get("context_class")
    is_nonstatic_method = context.get("is_nonstatic_method", False)

    if context_class and is_nonstatic_method:
        return True, TypeNode(
            TypeCategory.CLASS if not context_class.generic_params else TypeCategory.GENERIC_CLASS,
            IdentifierNode(context_class.name, *context_class.location),
            context_class.generic_params,
            *context_class.location
        )
    error_logger.add(
        expression.location,
        f"Invalid context for using this keyword"
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
        raise AssertionError(f"Unexpected expression: {expression.right.__class__.__name__}")

    member_name = expression.right.name
    operator = expression.operator
    valid, class_type = check_arithmetic_expression(expression.left, environment, **context)

    if not valid:
        # error is logged by this point
        return False, None

    if class_type is None:
        error_logger.add(
            expression.location,
            f"Invalid expression on the left side of the membership {operator} operator"
        )
        return False, None

    class_instance = get_class_by_name(
        class_type.name
    )

    class_field: ClassFieldDeclarationNode = get_class_field(
        class_instance,
        member_name
    )

    if class_field is None:
        error_logger.add(
            expression.location,
            f"Field {member_name} of the class {class_type.name} does not exist"
        )
        return False, None

    is_valid, return_type = instantiate_generic_type(
        class_field.type,
        class_instance,
        class_type.arguments
    )

    if not is_valid:
        error_logger.add(
            expression.location,
            f"Invalid return type"
        )
        return False, None

    class_field.use()
    return True, return_type


def _check_binary_operator(
    expression: BinaryOperatorNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    lhs_valid, lhs_type = check_arithmetic_expression(expression.left, environment, **context)
    rhs_valid, rhs_type = check_arithmetic_expression(expression.right, environment, **context)
    operator = expression.operator

    if not (lhs_valid and rhs_valid):
        # error is already logged
        return False, None

    if expression.is_arithmetic:
        return __get_type_of_arithmetic_binary_operator(lhs_type, rhs_type, operator, expression.location)
    elif expression.is_logical:
        return __get_type_of_logical_binary_operator(lhs_type, rhs_type, operator, expression.location)
    elif expression.is_comparison:
        return __get_type_of_comparison_binary_operator(lhs_type, rhs_type, operator, expression.location)
    elif expression.is_casting:
        if not isinstance(expression.right, TypeNode):
            error_logger.add(
                expression.location,
                f"Invalid type to cast"
            )
            return False, None
        return True, expression.right
    elif expression.is_coalesce:
        return check_arithmetic_expression(expression.left, environment, **context)
    else:
        error_logger.add(
            expression.location,
            f"Unsupported expression"
        )
        return False, None


def ___get_type_of_overloaded_operator(
    signature: list[TypeNode],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if operator not in POSSIBLE_OVERLOAD_OPERATORS and operator not in ["call", "index"]:
        error_logger.add(
            location,
            f"Operator {operator} is not overridable and cannot be applied to this types"
        )
        return False, None

    if operator in OPERATOR_NAMES:
        function_name = f"$operator_{OPERATOR_NAMES[operator]}"
    else:
        function_name = f"$operator_{operator}"
    is_valid, function_node = get_function(function_name, signature)

    if not is_valid or function_node is None:
        error_logger.add(
            location,
            f"Operator {operator} is overridable, but no override definition found"
        )
        return False, None

    if not isinstance(function_node.external_to, ClassDefinitionNode):
        error_logger.add(
            location,
            f"Operator overload is not associated to some class"
        )
        return False, None

    # TODO: support operator overloading for generics
    # TODO: deduce generic args
    is_valid, return_type = instantiate_generic_type(
        function_node.return_type,
        function_node.external_to,
        []
    )

    if not is_valid:
        error_logger.add(
            location,
            f"Failed to deduce return type for operator overload"
        )
        return False, None

    return True, return_type


def __get_type_of_arithmetic_binary_operator(
    lhs_type: Union[TypeNode, None],
    rhs_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if lhs_type.category == rhs_type.category == TypeCategory.PRIMITIVE:
        common_type = common_primitive_type(lhs_type.name, rhs_type.name)
        if operator == Operator.DIVIDE:
            common_type = common_primitive_type(lhs_type.name, TypeEnum.FLOAT)

        if common_type is None:
            error_logger.add(
                location,
                f"Unsupported operation {operator} for types {lhs_type.name} and {rhs_type.name}"
            )
            return False, None

        if lhs_type.name == common_type.name:
            return True, lhs_type
        else:
            return True, rhs_type
    elif (
        (lhs_type.category == TypeCategory.PRIMITIVE and rhs_type.type == TypeCategory.COLLECTION) or
        (lhs_type.category == TypeCategory.COLLECTION and rhs_type.category == TypeCategory.PRIMITIVE)
    ):
        error_logger.add(
            location,
            f"Unsupported operation {operator} for types {lhs_type.name} and {rhs_type.name}"
        )
        return False, None

    elif lhs_type.category == rhs_type.category == TypeCategory.COLLECTION:
        if lhs_type.type != rhs_type.type:
            error_logger.add(
                location,
                f"Unsupported operation {operator} for types {lhs_type.name} and {rhs_type.name}"
            )
            return False, None

        if lhs_type.type == TypeEnum.KEYMAP:
            error_logger.add(
                location,
                f"Unsupported operation {operator} for type {lhs_type.name}"
            )
            return False, None

        common_type = common_base(lhs_type, rhs_type)
        if common_type is None:
            error_logger.add(
                location,
                f"Unsupported operation {operator} for types {lhs_type.name} and {rhs_type.name}"
            )
            return False, None
        return True, common_type

    else:
        return ___get_type_of_overloaded_operator([lhs_type, rhs_type], operator, location)


def __get_type_of_logical_binary_operator(
    lhs_type: Union[TypeNode, None],
    rhs_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if not (lhs_type.type == rhs_type.type == TypeEnum.BOOLEAN):
        error_logger.add(
            location,
            f"Operator {operator} supports only boolean types"
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
        return ___get_type_of_overloaded_operator([lhs_type, rhs_type], operator, location)


def _check_unary_operator(
    unary_op_expr: UnaryOperatorNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    valid_expr, expression_type = check_arithmetic_expression(unary_op_expr.expression, environment, **context)
    operator = unary_op_expr.operator
    if unary_op_expr.is_arithmetic:
        return __get_type_of_arithmetic_unary_operator(expression_type, operator, unary_op_expr.location)

    elif unary_op_expr.is_allocation:
        return __get_type_of_allocation_unary_operator(expression_type, operator, unary_op_expr.location)

    elif unary_op_expr.is_logical:
        return __get_type_of_logical_unary_operator(expression_type, operator, unary_op_expr.location)

    elif unary_op_expr.is_reference:
        return __get_type_of_reference_unary_operator(expression_type, operator, unary_op_expr.location)

    else:
        error_logger.add(
            unary_op_expr.location,
            f"Unsupported expression"
        )
        return False, None


def __get_type_of_arithmetic_unary_operator(
    expression_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if expression_type.category == TypeCategory.PRIMITIVE:
        compatible_type = common_primitive_type(expression_type.name, TypeEnum.BYTE)
        if compatible_type is None:
            error_logger.add(
                location,
                f"Unsupported unary operation {operator} for types {expression_type.name}"
            )
            return False, None
        return True, expression_type

    elif expression_type.category == TypeCategory.COLLECTION:
        error_logger.add(
            location,
            f"Unsupported unary operation {operator} for types {expression_type.name}"
        )
        return False, None

    else:
        return ___get_type_of_overloaded_operator([expression_type], operator, location)


def __get_type_of_logical_unary_operator(
    expression_type: Union[TypeNode, None],
    operator: str,
    location: tuple[int, int]
) -> Tuple[bool, Union[TypeNode, None]]:
    if expression_type.type != TypeEnum.BOOLEAN:
        error_logger.add(
            location,
            f"Operator {operator} supports only boolean types"
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
            location,
            f"Unsupported expression"
        )
        return False, None

    # TODO: complex check
    if operator == Operator.NEW_INSTANCE:
        return True, expression_type
    elif operator == Operator.DELETE_INSTANCE:
        return True, None
    else:
        error_logger.add(
            location,
            f"Unsupported expression"
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
                location,
                f"Cannot reference already referenced type"
            )
            return False, None
        copy = expression_type.shallow_copy()
        copy.set_reference()
        return True, copy
    elif operator == Operator.DEREFERENCE:
        error_logger.add(
            location,
            f"Cannot dereference non-reference type"
        )
        if not expression_type.is_reference:
            return False, None
        copy = expression_type.shallow_copy()
        copy.unset_reference()
        return True, copy
    else:
        error_logger.add(
            location,
            f"Unsupported expression"
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
        expression.location,
        f"Unresolved reference for {expression.name}"
    )
    return False, None


def _get_type_of_function_call(
    expression: FunctionCallNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:

    function_id = expression.identifier
    if isinstance(function_id, MemberOperatorNode):
        return __get_method_call(expression, environment, **context)

    elif isinstance(function_id, IdentifierNode):
        return __get_function_call(expression, environment, **context)

    # Assume no static, functors etc
    else:
        error_logger.add(
            expression.location,
            f"Unsupported expression"
        )
        return False, None


def __get_method_call(
    expression: FunctionCallNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    function_id = expression.identifier
    valid, class_type_node = check_arithmetic_expression(function_id, environment, **context)
    if not valid:
        # error is already logged
        return False, None

    if class_type_node is None:
        error_logger.add(
            expression.location,
            f"Invalid expression for method call"
        )
        return False, None

    if not isinstance(class_type_node, TypeNode):
        error_logger.add(
            expression.location,
            f"Invalid expression for method call"
        )
        return False, None

    potentially_method_name = function_id.right
    if not isinstance(potentially_method_name, IdentifierNode):
        error_logger.add(
            expression.location,
            f"Invalid expression for method name: {type(potentially_method_name).__name__}"
        )
        return False, None

    if class_type_node.category not in (TypeCategory.CLASS, TypeCategory.GENERIC_CLASS):
        error_logger.add(
            expression.location,
            f"Invalid type: {class_type_node.type}"
        )
        return False, None

    args_signature = []
    for arg in expression.arguments:
        valid_arg, arg_type = check_arithmetic_expression(arg, environment, **context)
        if not valid_arg:
            # error is already logged
            return False, None
        args_signature.append(arg_type)

    class_instance = get_class_by_name(
        class_type_node.name
    )

    class_method = get_class_method(
        class_instance,
        potentially_method_name.name,
        args_signature)

    if not class_method:
        error_logger.add(
            expression.location,
            f"Invalid type: method {potentially_method_name.name} doesn't exist"
        )
        return False, None

    is_valid, return_type = instantiate_generic_type(
        class_method.return_type,
        class_instance,
        class_type_node.arguments
    )
    if not is_valid:
        error_logger.add(
            expression.location,
            f"Invalid return type"
        )
        return False, None

    expression.function = class_method
    class_method.use()
    return True, return_type


def __get_function_call(
    expression: FunctionCallNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    function_id = expression.identifier
    args_signature = []
    for arg in expression.arguments:
        valid_arg, arg_type = check_arithmetic_expression(arg, environment, **context)
        if not valid_arg:
            # error is already logged
            return False, None
        args_signature.append(arg_type)

    is_valid, function_node = get_function(function_id.name, args_signature)

    if not is_valid or function_node is None:
        error_logger.add(
            expression.location,
            f"Invalid function: {function_id.name}"
        )
        return False, None

    expression.function = function_node
    function_node.use()
    return True, function_node.return_type


def _get_type_of_indexation_call(
    expression: IndexNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> Tuple[bool, Union[TypeNode, None]]:
    valid_expr, expression_type = check_arithmetic_expression(expression.variable, environment, **context)

    if not valid_expr:
        # error is already logged
        return False, None

    if expression_type.category == TypeCategory.PRIMITIVE:
        error_logger.add(
            expression.location,
            f"Invalid type: {expression_type.name}"
        )
        return False, None

    elif expression_type.category == TypeCategory.COLLECTION:
        if expression_type.name not in (TypeEnum.ARRAY, TypeEnum.KEYMAP):
            error_logger.add(
                expression.location,
                f"Invalid type: {expression_type.name}"
            )
            return False, None

    argument_signature = [expression_type]
    for arg in expression.arguments:
        valid, arg_type = check_arithmetic_expression(arg, environment, **context)
        if not valid:
            error_logger.add(
                arg.location,
                f"Invalid expression"
            )
            return False, None
        argument_signature.append(arg_type)

    if expression_type.category == TypeCategory.COLLECTION:

        if not expression_type.arguments:
            error_logger.add(
                expression.location,
                "Invalid collection: no containing type provided"
            )
            return False, None

        if len(argument_signature) == 0:
            error_logger.add(
                expression.location,
                "No argument provided for collection type"
            )
        if len(argument_signature) > 1:
            error_logger.add(
                expression.location,
                "Too many arguments for collection type"
            )
        if expression_type.name == TypeEnum.ARRAY:
            cpt = common_primitive_type(argument_signature[1].name, TypeEnum.INTEGER)
            if not cpt or cpt != TypeEnum.INTEGER:
                error_logger.add(
                    "Non-integer type argument provided for array type in index"
                )
                return False, None

            return True, expression_type.arguments[0]

        else:
            cpt = common_primitive_type(argument_signature[1].name, expression_type.arguments[0].name)
            if not cpt:
                error_logger.add(
                    "Incompatible type argument provided for keymap type in index"
                )
                return False, None

            return True, expression_type.arguments[1]
    else:
        return ___get_type_of_overloaded_operator(argument_signature, "index", expression.location)


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
            TypeCategory.PRIMITIVE,
            TypeLiteral(type_of_literal, *literal.location),
            None,
            *literal.location,
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
            TypeCategory.PRIMITIVE,
            TypeLiteral(type_of_literal, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, ImaginaryFloatLiteralNode):
        return True, TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.COMPLEX, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, StringLiteralNode):
        return True, TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.STRING, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, BooleanLiteralNode):
        return True, TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.BOOLEAN, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, ByteStringLiteralNode):
        return True, TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.BYTESTRING, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, NullLiteralNode):
        return True, TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.NULL, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, UndefinedLiteralNode):
        return True, TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.UNDEFINED, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, CharLiteralNode):
        return True, TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.CHAR, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )

    elif isinstance(literal, ListLiteralNode):
        elements: list[TypeNode] = []
        for arg in literal.elements:
            valid_arg, arg_type = check_arithmetic_expression(arg, environment, **context)
            if not valid_arg:
                # error is already logged
                return False, None
            elements.append(arg_type)

        if len(elements) == 0:
            raise AssertionError("Tree shouldn't be parsed like that")

        common_compatible_type = elements[0]

        if len(elements) > 1:
            for element in elements:
                common_compatible_type = common_base(element, common_compatible_type)
                if common_compatible_type is None:
                    error_logger.add(
                        element.location,
                        f"Type inconsistency in list/array literal"
                    )
                    return False, None

        return True, TypeNode(
            TypeCategory.COLLECTION,
            TypeLiteral(TypeEnum.ARRAY, *literal.location),
            [common_compatible_type],
            *literal.location,
            _literal=True,
        )

    elif isinstance(literal, KeymapLiteralNode):
        elements: list[tuple[TypeNode, TypeNode]] = []
        for arg in literal.elements:
            valid_arg, arg_type = __check_keymap_literal(arg, environment, **context)
            if not valid_arg:
                # error is already logged
                return False, None
            elements.append(arg_type)

        if len(elements) == 0:
            raise AssertionError("Tree shouldn't be parsed like that")

        common_compatible_key_type, common_compatible_value_type = elements[0]

        if len(elements) > 1:
            for element in elements:
                common_compatible_key_type = common_base(element[0], common_compatible_key_type)
                common_compatible_value_type = common_base(element[1], common_compatible_value_type)
                if common_compatible_key_type is None or common_compatible_value_type is None:
                    error_logger.add(
                        element[0].location,
                        f"Type inconsistency in keymap literal"
                    )
                    return False, None

        return True, TypeNode(
            TypeCategory.COLLECTION,
            TypeLiteral(TypeEnum.ARRAY, *literal.location),
            [common_compatible_key_type, common_compatible_value_type],
            *literal.location,
            _literal=True,
        )

    elif isinstance(literal, EmptyLiteralNode):
        # special case: can be any empty sequence
        return True, TypeNode(
            TypeCategory.COLLECTION,
            TypeLiteral(TypeEnum.ARRAY, *literal.location),
            None,
            *literal.location,
            _literal=True
        )
    else:
        return False, None


def __check_keymap_literal(
    arg: KeymapElementNode,
    environment: dict[str, TypeNode],
    **context: Unpack[_ContextParams]
) -> tuple[bool, tuple[TypeNode, TypeNode] | None]:
    valid_key, key_type = check_arithmetic_expression(arg.left, environment, **context)
    valid_value, value_type = check_arithmetic_expression(arg.right, environment, **context)

    if not valid_key or not valid_value:
        return False, None

    return True, (key_type, value_type)
