from ..abstract_syntax_tree import *

from .shared import error_logger, class_definitions, function_definitions

from ._type_class import get_class_by_name
from typing import Literal


def get_variable_type_from_environment(
    variable_name: str,
    environment: dict[str, TypeNode],
    location: tuple[int, int]
) -> TypeNode | None:
    if variable_name in environment:
        return environment[variable_name]
    error_logger.add(location, f"Variable '{variable_name}' is not defined in this context.")
    return None


def get_class_definition(
    class_name: str,
    location: tuple[int, int]
) -> ClassDefinitionNode | None:
    matching_class_definitions = get_class_by_name(class_name, multiple=True)
    if not matching_class_definitions:
        error_logger.add(location, f"Class '{class_name}' not defined.")
        return None
    elif len(matching_class_definitions) == 1:
        return matching_class_definitions[0]
    else:
        error_logger.add(location, f"Class '{class_name}' defined multiple times.")
        return None


def get_instantiated_class_definition(
    class_: IdentifierNode,
    generic_parameters: list[TypeNode],
    location: tuple[int, int]
) -> ClassDefinitionNode | None:
    if isinstance(class_, IdentifierNode):
        class_name = class_.name
    else:
        error_logger.add(location, f"IdentifierNode '{class_}' cannot be interpreted as a class.")
        return None

    uninstantiated_class_definition = get_class_definition(
        class_name,
        location
    )
    if uninstantiated_class_definition is None:
        return None
    # TODO: generics
    # return instantiate
    return ...


def get_class_field(
    current_class_node: ClassDefinitionNode,
    generic_parameters: list[TypeNode],
    field_name: str,
    context: Literal["outer", "inner"],
    location: tuple[int, int],
) -> ClassFieldDeclarationNode | None:
    matching_field_definitions = [
        field
        for field in current_class_node.all_fields_definitions
        if field.name == field_name
    ]

    # multiple fields definitions found => error
    if len(matching_field_definitions) > 1:
        error_logger.add(location, f"Field '{field_name} has been defined multiple times in this class")
        return None

    # found one => check access type and context
    elif len(matching_field_definitions) == 1:
        field = matching_field_definitions[0]
        if field.access_type == AccessType.PUBLIC:
            return field
        elif context == "inner":
            return field
        else:
            error_logger.add(location, f"Field '{field_name} is {field.access_type} and cannot be accessed")
            return None

    # else: try lookup in inheritance tree
    # case 1: superclass exists
    # TODO: matching generics params
    superclass = current_class_node.superclass
    if isinstance(superclass, TypeNode):
        # TODO: check freaking inheritance, you fool
        if superclass.category not in (TypeCategory.CLASS, TypeCategory.COLLECTION):
            error_logger.add(superclass.location, f"Builtin type '{superclass.type}' is sealed for inheritance")
            return None

        # pseudo: match_generics(generic_parameters, superclass.generic_arguments)
        superclass_instance = get_instantiated_class_definition(
            superclass.type,
            generic_parameters, location
        )

        # error is already logged
        if superclass_instance is None:
            return None

        superclass_field = get_class_field(
            superclass_instance,
            generic_parameters,
            field_name,
            context,
            location,
        )

        # error is already logged
        if superclass_field is None:
            return None

        # got private field => invalidate
        elif superclass_field.access_type == AccessType.PRIVATE:
            error_logger.add(location, f"Field '{field_name} is private in superclass and cannot be accessed")
            return None

        else:
            return superclass_field

    # case 2. superclass doesn't exist
    else:
        error_logger.add(location, f"Field '{field_name} isn't defined in this class")
        return None


def get_class_methods(
    class_definition_node: ClassDefinitionNode,
    generic_parameters: list[TypeNode],
    context: Literal["inner", "outer"],
    location: tuple[int, int]
) -> list[ClassMethodDeclarationNode]:

    filtered_methods = [
        method
        for method in class_definition_node.methods_definitions
        if context == "inner" or method.access_type == AccessType.PUBLIC
    ]
    if class_definition_node.superclass is None:
        return filtered_methods

    # TODO: match generics
    superclass = class_definition_node.superclass
    superclass_instance = get_instantiated_class_definition(
        superclass.type,
        generic_parameters, location
    )
    if superclass_instance is None:
        return filtered_methods

    current_class_method_names = {
        method.function_name
        for method in filtered_methods
    }
    superclass_methods = [
        method
        for method in superclass_instance.methods_definitions
        if (method.access_type == AccessType.PUBLIC or
            (context == "inner" and method.access_type == AccessType.PROTECTED)) and
           (method.function_name not in current_class_method_names)
    ]

    return filtered_methods + superclass_methods


# def check_no_duplicate_variable_declarations(
#     error_logger: ErrorLogger,
#
# )
