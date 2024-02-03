from ..abstract_syntax_tree import *
from ..semantics import TypeEnum

from .shared import error_logger, class_definitions, function_definitions


def get_type_of_expression(
    expression: ASTNode,
    environment: dict[str, TypeNode]
) -> TypeNode | None:
    if isinstance(expression, LiteralNode):
        return _get_type_of_primitive_literal(expression, environment)

    # TODO: implement all of this
    elif isinstance(expression, BinaryOperatorNode):
        return _get_type_of_binary_operator(expression, environment)

    elif isinstance(expression, UnaryOperatorNode):
        return _get_type_of_unary_operator(expression, environment)

    elif isinstance(expression, FunctionCallNode):
        return _get_type_of_function_call(expression, environment)

    elif isinstance(expression, FunctionCallNode):
        return _get_type_of_indexation_call(expression, environment)

    elif isinstance(expression, FunctionCallNode):
        return _get_type_of_identifier(expression, environment)


def _get_type_of_identifier(
    expression: IdentifierNode,
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
                common_compatible_type = get_common_base(element, common_compatible_type)
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
                common_compatible_key_type = get_common_base(element, common_compatible_key_type)
                common_compatible_value_type = get_common_base(element, common_compatible_value_type)
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


def get_common_base(lhs_type, rhs_type):
    pass

def match_types(
    current_type: TypeNode,
    target_type: TypeNode,
):
    # absolute equal
    if current_type == target_type:
        return True

    # the only case when constant marker really matters
    if not current_type.is_constant and target_type.is_constant:
        return False

    # the only case when nullable marker itself matters
    if current_type.is_nullable and not target_type.is_nullable:
        return False

    # cannot assign reference into non-reference and vise versa
    # the only case
    if current_type.is_reference != target_type.is_reference:
        return False

    # if null, check if nullable
    if current_type.type == TypeEnum.NULL:
        return target_type.is_nullable

    # different types => False
    # in rest cases, check only current_type_category
    if current_type.category != target_type.category:
        return False

    # implicit conditions from here:
    # 1. current_type.category == target_type.category
    # => no need to make conditions complex
    # 2. current_type.is_reference == target_type.is_reference => no need to check reference
    # 3. if lhs is not const and rhs is const, then it's invalidated => no need to check const
    # 4. if lhs is nullable and rhs is not, then it's invalidated
    # 5. passing null into target is already predicted => no need to check nullable
    # => no need to check any modifier
    # all is needed is
    # 1. lookup current_type category
    # 2. lookup current and target types
    # 3. if types m

    current_type_name = current_type.type.name
    target_type_name = target_type.type.name

    if current_type.category == TypeCategory.PRIMITIVE:

        # basic case: types match
        if current_type_name == target_type_name:
            return True

        # non-basic cases: implicit cast
        if current_type_name == TypeEnum.BYTE:
            return target_type in (
                TypeEnum.SHORT_INTEGER,
                TypeEnum.INTEGER,
                TypeEnum.LONG_INTEGER,
                TypeEnum.EXTENDED_INTEGER,
                TypeEnum.FLOAT,
                TypeEnum.DOUBLE,
                TypeEnum.COMPLEX
            )
        elif current_type_name == TypeEnum.SHORT_INTEGER:
            return target_type in (
                TypeEnum.INTEGER,
                TypeEnum.LONG_INTEGER,
                TypeEnum.EXTENDED_INTEGER,
                TypeEnum.FLOAT,
                TypeEnum.DOUBLE,
                TypeEnum.COMPLEX
            )
        elif current_type_name == TypeEnum.INTEGER:
            return target_type in (
                TypeEnum.LONG_INTEGER,
                TypeEnum.EXTENDED_INTEGER,
                TypeEnum.FLOAT,
                TypeEnum.DOUBLE,
                TypeEnum.COMPLEX
            )
        elif current_type_name == TypeEnum.LONG_INTEGER:
            return target_type in (
                TypeEnum.EXTENDED_INTEGER,
                TypeEnum.DOUBLE,
                TypeEnum.COMPLEX,
            )
        elif current_type_name == TypeEnum.FLOAT:
            return target_type in (
                TypeEnum.DOUBLE,
                TypeEnum.COMPLEX
            )
        elif current_type_name == TypeEnum.DOUBLE:
            return target_type in (
                TypeEnum.COMPLEX,
            )

        else:
            return False

    elif current_type.category == TypeCategory.COLLECTION:

        # TODO: list literal might be suitable for array, set and list
        # case 1: literal
        if current_type.is_literal and current_type_name == TypeEnum.ARRAY:
            pass

        # case 2: everything else
        # type mismatch == False, no implicit casts
        if current_type_name != target_type_name:
            return False

        # if arg length mismatch => false
        if len(current_type.arguments) != len(target_type.arguments):
            return False

        return all((
            match_types(current_type.arguments[i], target_type.arguments[i])
            for i, _ in enumerate(current_type.arguments)
        ))

    elif current_type.category == TypeCategory.CLASS:
        if current_type.arguments or target_type.arguments:
            return False

        return current_type_name == target_type_name

    elif current_type.category == TypeCategory.GENERIC_CLASS:
        if current_type_name != target_type_name:
            return False

        if not current_type.arguments or not target_type.arguments:
            return False

        if len(current_type.arguments) != len(target_type.arguments):
            return False

        return all((
            match_types(current_type.arguments[i], target_type.arguments[i])
            for i, _ in enumerate(current_type.arguments)
        ))

    # unpredicted situations
    else:
        return False
