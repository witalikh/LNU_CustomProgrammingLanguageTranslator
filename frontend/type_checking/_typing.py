from ..abstract_syntax_tree import *
from ..semantics import TypeEnum

from .shared import error_logger, class_definitions, function_definitions


def get_type_of_literal(
    literal: LiteralNode
) -> TypeNode | None:
    if isinstance(literal, IntegerLiteralNode):
        match literal.size:
            case IntegerSizes.BYTE:
                type_of_literal = TypeEnum.BYTE
            case IntegerSizes.INTEGER:
                type_of_literal = TypeEnum.INTEGER
            case _:
                type_of_literal = TypeEnum.LONG_INTEGER

        return TypeNode(
            TypeCategory.PRIMITIVE,
            TypeLiteral(type_of_literal, *literal.location),
            None,
            *literal.location
        )
    elif isinstance(literal, FloatLiteralNode):
        pass
    # TODO: other literals


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
        if current_type_name == TypeEnum.INTEGER:
            return target_type in (
                TypeEnum.LONG_INTEGER,
                TypeEnum.FLOAT,
                TypeEnum.LONG_FLOAT,
                TypeEnum.COMPLEX
            )
        elif current_type_name == TypeEnum.LONG_INTEGER:
            return target_type in (
                TypeEnum.LONG_FLOAT,
                TypeEnum.COMPLEX,
            )
        elif current_type_name == TypeEnum.FLOAT:
            return target_type in (
                TypeEnum.LONG_FLOAT,
                TypeEnum.COMPLEX
            )
        elif current_type_name == TypeEnum.LONG_FLOAT:
            return target_type in (
                TypeEnum.COMPLEX,
            )

        else:
            return False

    elif current_type.category == TypeCategory.COLLECTION:

        # TODO: list literal might be suitable for array, set and list

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
