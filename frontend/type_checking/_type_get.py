from ..abstract_syntax_tree import *
from ..semantics import TypeEnum

from .shared import error_logger, class_definitions, function_definitions

from ._type_cast import common_base, common_primitive_type
from ..syntax import Operator


def get_type_of_expression(
    expression: ASTNode,
    environment: dict[str, TypeNode]
) -> TypeNode | None:
    if isinstance(expression, LiteralNode):
        return _get_type_of_primitive_literal(expression, environment)

    elif isinstance(expression, BinaryOperatorNode):
        return _get_type_of_binary_operator(expression, environment)

    elif isinstance(expression, UnaryOperatorNode):
        return _get_type_of_unary_operator(expression, environment)

    elif isinstance(expression, FunctionCallNode):
        return _get_type_of_function_call(expression, environment)

    elif isinstance(expression, IndexNode):
        return _get_type_of_indexation_call(expression, environment)

    elif isinstance(expression, IdentifierNode):
        return _get_type_of_identifier(expression, environment)


def _get_type_of_binary_operator(
    expression: BinaryOperatorNode,
    environment: dict[str, TypeNode]
) -> TypeNode | None:

    if isinstance(expression, KeymapLiteralNode):
        raise AssertionError("KeymapLiteralNode shouldn't be used directly by this function.")

    if isinstance(expression, MemberOperatorNode):
        return __get_type_of_member(expression, environment)

    lhs_type = get_type_of_expression(expression.left, environment)
    rhs_type = get_type_of_expression(expression.right, environment)
    operator = expression.operator

    if isinstance(operator, ArithmeticOperatorNode):
        return __get_type_of_arithmetic_binary_operator(lhs_type, rhs_type, operator)
    elif isinstance(operator, LogicalOperatorNode):
        if not (lhs_type.type == rhs_type.type == TypeEnum.BOOLEAN):
            return None
        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.BOOLEAN, *expression.location),
            None,
            *expression.location
        )
    elif isinstance(operator, ComparisonNode):
        return __get_type_of_comparison_binary_operator(lhs_type, rhs_type, operator)


def __get_type_of_arithmetic_binary_operator(lhs_type, rhs_type, operator):
    if lhs_type.category == rhs_type.category == TypeCategory.PRIMITIVE:
        common_type = common_primitive_type(lhs_type.type, rhs_type.type)
        if operator == Operator.DIVIDE:
            common_type = common_primitive_type(lhs_type.type, TypeEnum.FLOAT)
        return common_type
    elif (
        (lhs_type.category == TypeCategory.PRIMITIVE and rhs_type.type == TypeCategory.COLLECTION) or
        (lhs_type.category == TypeCategory.COLLECTION and rhs_type.category == TypeCategory.PRIMITIVE)
    ):
        return None

    elif lhs_type.category == rhs_type.category == TypeCategory.COLLECTION:
        common_type = common_base(lhs_type, rhs_type)

def _get_type_of_unary_operator(
    expression: UnaryOperatorNode,
    environment: dict[str, TypeNode]
) -> TypeNode | None:
    expression_type = get_type_of_expression(expression.expression, environment)
    rhs_type = get_type_of_expression(expression.right, environment)
    if isinstance(expression, ArithmeticOperatorNode):
        pass


def _get_type_of_identifier(
    expression: IdentifierNode,
    environment: dict[str, TypeNode]
) -> TypeNode | None:
    return environment.get(expression.name)


def _get_type_of_function_call(
    expression: FunctionCallNode,
    environment: dict[str, TypeNode]
) -> TypeNode | None:
    return environment.get(expression.name)


def _get_type_of_indexation_call(
    expression: IndexNode,
    environment: dict[str, TypeNode]
) -> TypeNode | None:
    return environment.get(expression.name)


def _get_type_of_primitive_literal(
    literal: LiteralNode,
    environment: dict[str, TypeNode]
) -> TypeNode | None:
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

        return TypeNode(
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

        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(type_of_literal, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, ImaginaryFloatLiteralNode):
        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.COMPLEX, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, StringLiteralNode):
        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.STRING, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, BooleanLiteralNode):
        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.BOOLEAN, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, ByteStringLiteralNode):
        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.BYTESTRING, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, NullLiteralNode):
        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.NULL, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, UndefinedLiteralNode):
        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.UNDEFINED, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )
    elif isinstance(literal, CharLiteralNode):
        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(TypeEnum.CHAR, *literal.location),
            None,
            *literal.location,
            _literal=True,
        )

    elif isinstance(literal, ListLiteralNode):
        elements = [get_type_of_expression(arg, environment) for arg in literal.elements]
        if len(elements) == 0:
            return None

        common_compatible_type = elements[0]

        if len(elements) > 1:
            for element in elements:
                common_compatible_type = common_base(element, common_compatible_type)
                if common_compatible_type is None:
                    return None

        return TypeNode(
            TypeCategory.COLLECTION,
            TypeLiteral(TypeEnum.ARRAY, *literal.location),
            [common_compatible_type],
            *literal.location,
            _literal=True,
        )

    elif isinstance(literal, KeymapLiteralNode):
        elements = [get_type_of_expression(arg, environment) for arg in literal.elements]
        if len(elements) == 0:
            return None

        common_compatible_key_type, common_compatible_value_type = elements[0]

        if len(elements) > 1:
            for element in elements:
                common_compatible_key_type = common_base(element, common_compatible_key_type)
                common_compatible_value_type = common_base(element, common_compatible_value_type)
                if common_compatible_key_type is None or common_compatible_value_type is None:
                    return None

        return TypeNode(
            TypeCategory.COLLECTION,
            TypeLiteral(TypeEnum.ARRAY, *literal.location),
            [common_compatible_key_type, common_compatible_value_type],
            *literal.location,
            _literal=True,
        )

    elif isinstance(literal, EmptyLiteralNode):
        # special case: can be any empty sequence
        return TypeNode(
            TypeCategory.COLLECTION,
            TypeLiteral(TypeEnum.ARRAY, *literal.location),
            None,
            *literal.location,
            _literal=True
        )
    else:
        return None
