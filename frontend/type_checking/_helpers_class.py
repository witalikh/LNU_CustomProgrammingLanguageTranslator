from .shared import class_definitions
from ..abstract_syntax_tree import *
from ..abstract_syntax_tree import ClassDefinitionNode


from ._helpers_function import match_signatures


def get_class_by_name(
    class_name: str,
    multiple: bool = False,
) -> None | ClassDefinitionNode | list[ClassDefinitionNode]:
    matching_class_definitions = [
        class_definition
        for class_definition in class_definitions
        if class_definition.name == class_name
    ]
    if multiple:
        return matching_class_definitions
    elif len(matching_class_definitions) == 1:
        return matching_class_definitions[0]
    else:
        return None


def get_class_method(
    class_name: str,
    method_name: str,
    type_signature: list[TypeNode],
    is_static: bool = False,
) -> ClassMethodDeclarationNode | None:
    class_instance = get_class_by_name(class_name)
    if class_instance is None:
        return None

    look_methods_in = class_instance.methods_definitions if not is_static else class_instance.static_methods_definitions
    for class_method in look_methods_in:
        if class_method.function_name != method_name:
            continue

        if match_signatures(type_signature, class_method.parameters_signature):
            return class_method
    return None


def get_class_field(
    class_name: str,
    field_name: str,
) -> ClassFieldDeclarationNode | None:
    class_instance = get_class_by_name(class_name)
    if class_instance is None:
        return None

    for field in class_instance.all_fields_definitions:
        if field.name == field_name:
            return field

    return None


def get_class_method_type(
    class_name: str,
    method_name: str,
    type_signature: list[TypeNode],
    generic_args: list[TypeNode] | None = None,
    is_static: bool = False,
) -> tuple[bool, TypeNode | None]:
    class_instance = get_class_by_name(class_name)
    if class_instance is None:
        return False, None

    look_methods_in = class_instance.methods_definitions if not is_static else class_instance.static_methods_definitions
    method = None
    for class_method in look_methods_in:
        if class_method.function_name != method_name:
            continue

        if match_signatures(type_signature, class_method.parameters_signature):
            method = class_method
            break
    if method is None:
        return False, None

    ret_type = method.return_type
    if ret_type.represents_generic_param:
        for generic, actual in zip(class_instance.generic_params, generic_args):
            if generic.name == ret_type.name:
                return True, actual
        else:
            return False, None
    else:
        return True, ret_type
