"""
Contains validate_type function that checks if the TypeNode is valid given in the program
"""


from ..abstract_syntax_tree import TypeNode, ASTNode, TypeCategory, ClassDefinitionNode, GenericParameterNode
from .shared import error_logger

from ._helpers_class import get_class_by_name


def validate_type(
    type_to_check: TypeNode | ASTNode,
    generic_parameters_context: list[GenericParameterNode] | None = None,
) -> bool:
    """
    Method that checks if the given type ever exists.
    """

    # Everything beside TypeNode is invalid
    if not isinstance(type_to_check, TypeNode):
        error_logger.add(type_to_check, "Invalid type expression")
        if type_to_check is not None:
            type_to_check.valid = False
        return False

    # Validation end: TypeNode, TypeLiteral, IdentifierNode(1/?)
    # Every primitive type is valid as it's recognized by parser
    if type_to_check.category == TypeCategory.PRIMITIVE:
        type_to_check.valid = True
        type_to_check.type.valid = True
        return True

    # Every builtin collection is valid when elements type are also valid
    elif type_to_check.category == TypeCategory.COLLECTION:
        valid = _validate_builtin_compound_type(type_to_check)
        type_to_check.valid = valid
        type_to_check.type.valid = valid
        return valid

    elif type_to_check.category == TypeCategory.CLASS:
        valid = _validate_non_generic_class_or_generic(type_to_check, generic_parameters_context)
        type_to_check.valid = valid
        type_to_check.type.valid = valid
        return valid

    else:
        valid = _validate_generic_class(type_to_check)
        type_to_check.valid = valid
        type_to_check.type.valid = valid
        return valid


# TODO: parser changes for specific cases
def _validate_builtin_compound_type(type_to_check: TypeNode) -> bool:
    if not type_to_check.arguments:
        error_logger.add(
            type_to_check.location,
            f"Type {type_to_check.type} should contain at least one argument"
        )
        return False
    type_of_first_argument = validate_type(type_to_check.arguments[0])
    if not type_of_first_argument:
        return False
    if type_to_check.type == "array":
        return True
    elif type_to_check.type == "keymap":
        if len(type_to_check.arguments) != 2:
            error_logger.add(
                type_to_check.location,
                f"Keymap type requires exactly two arguments, got {len(type_to_check.arguments)}"
            )
            return False
        return validate_type(type_to_check.arguments[1])
    elif type_to_check.type in ("set", "list"):
        if len(type_to_check.arguments) != 1:
            error_logger.add(
                type_to_check.location,
                f"Keymap {type_to_check.type} requires only one argument, got {len(type_to_check.arguments)}"
            )
            return False
        return True
    else:
        error_logger.add(type_to_check.location, f"Unknown type: {type_to_check.type}")
        return False


def _validate_non_generic_class_or_generic(
    type_to_check: TypeNode,
    generic_parameters_context: list[GenericParameterNode] | None,
) -> bool:
    if generic_parameters_context and type_to_check.represents_generic_param is None:
        generic_node = None
        for parameter in generic_parameters_context:
            if parameter.name == type_to_check.name:
                generic_node = parameter
                break
        if generic_node:
            type_to_check.represents_generic_param = True
            return True
        else:
            type_to_check.represents_generic_param = False
    else:
        type_to_check.represents_generic_param = False

    class_name = type_to_check.name
    class_instance = get_class_by_name(
        class_name
    )
    if not isinstance(class_instance, ClassDefinitionNode):
        error_logger.add(type_to_check.location, f"Unknown class definition: {class_name}")
        return False
    if class_instance.generic_params:
        error_logger.add(type_to_check.location, f"Class {class_name} requires generic parameters to instantiate")
        return False
    return True


def _validate_generic_class(type_to_check: TypeNode) -> bool:
    class_name = type_to_check.name
    class_instance = get_class_by_name(
        class_name
    )
    if not isinstance(class_instance, ClassDefinitionNode):
        error_logger.add(type_to_check.location, f"Unknown class definition: {class_name}")
        return False
    if not class_instance.generic_params:
        error_logger.add(type_to_check.location,
                         f"Class {class_name} doesn't require generic parameters to instantiate")
        return False
    if len(type_to_check.arguments) > len(class_instance.generic_params):
        error_logger.add(type_to_check.location, f"Too many arguments for class {class_name}")
        return False
    if len(type_to_check.arguments) < len(class_instance.generic_params):
        error_logger.add(type_to_check.location, f"Not enough arguments for class {class_name}")
        return False

    return all((validate_type(x) for x in type_to_check.arguments))
