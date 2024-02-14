from ..abstract_syntax_tree import *
from ..semantics import TypeEnum


from ._type_inheritance import least_common_base


def common_base(left_type: TypeNode, right_type: TypeNode) -> TypeNode | None:

    # if fully equal, return
    if left_type == right_type:
        return left_type

    if left_type.category != right_type.category:
        return None

    if left_type.is_reference != right_type.is_reference:
        return None

    literal = left_type.is_literal and right_type.is_literal
    const = left_type.is_constant and right_type.is_constant
    nullable = left_type.is_nullable or right_type.is_nullable
    reference = left_type.is_reference

    if left_type.category == TypeCategory.PRIMITIVE:

        common = common_primitive_type(left_type.name, right_type.name)
        if common is None:
            return None

        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(common, *left_type.location),
            None,
            *left_type.location,
            _literal=literal,
            _const=const,
            _nullable=nullable,
            _reference=reference
        )

    elif left_type.category == TypeCategory.COLLECTION:
        if left_type.name != right_type.name:
            return None

        if len(left_type.arguments) != len(right_type.arguments):
            return None

        common_arg_types = []
        for i in range(len(left_type.arguments)):
            _common = common_base(left_type.arguments[i], right_type.arguments[i])
            if _common is None:
                return None
            common_arg_types.append(_common)

        return TypeNode(
            TypeCategory.COLLECTION,
            left_type.type,
            common_arg_types,
            *left_type.location,
            _literal=literal,
            _const=const,
            _nullable=nullable,
            _reference=reference
        )
    else:
        lcb_name = least_common_base(left_type, right_type)
        if lcb_name is None:
            return None

        return TypeNode(
            TypeCategory.CLASS,
            IdentifierNode(lcb_name, *left_type.location),
            left_type.arguments,
            *left_type.location,
            _const=const,
            _nullable=nullable,
            _reference=reference
        )


def common_primitive_type(left_type: TypeEnum | str, right_type: TypeEnum | str) -> TypeEnum | None:
    """
    Returns the common primitive type from the given primitive type names
    :param left_type:
    :param right_type:
    :return:
    """

    if left_type == right_type:
        return left_type

    # TODO: other implicit casts (maybe)
    integer_types = (
        TypeEnum.BYTE,
        TypeEnum.SHORT_INTEGER,
        TypeEnum.INTEGER,
        TypeEnum.LONG_INTEGER,
        TypeEnum.EXTENDED_INTEGER
    )
    float_types = (
        TypeEnum.FLOAT,
        TypeEnum.DOUBLE,
        TypeEnum.COMPLEX
    )
    numeric_types = integer_types + float_types

    if not (left_type in numeric_types and right_type in numeric_types):
        return None

    if left_type == TypeEnum.BYTE:
        return right_type

    elif left_type == TypeEnum.SHORT_INTEGER:
        return right_type if right_type != TypeEnum.BYTE else left_type

    elif left_type == TypeEnum.INTEGER:
        return right_type if right_type not in (TypeEnum.BYTE, TypeEnum.SHORT_INTEGER) else left_type

    elif left_type == TypeEnum.INTEGER:
        return right_type if right_type not in (TypeEnum.BYTE, TypeEnum.SHORT_INTEGER, TypeEnum.INTEGER) else left_type

    # extended int is not compatible with floats
    elif left_type == TypeEnum.EXTENDED_INTEGER:
        if right_type in float_types:
            return None
        else:
            return left_type

    elif left_type == TypeEnum.FLOAT:
        if right_type == TypeEnum.EXTENDED_INTEGER:
            return None
        return right_type if right_type in float_types else left_type

    elif left_type == TypeEnum.DOUBLE:
        if right_type == TypeEnum.EXTENDED_INTEGER:
            return None
        return right_type if right_type == TypeEnum.COMPLEX else left_type

    elif left_type == TypeEnum.COMPLEX:
        if right_type == TypeEnum.EXTENDED_INTEGER:
            return None
        return left_type
    else:
        return None
