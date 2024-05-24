from .shared import class_definitions
from ..abstract_syntax_tree import TypeNode, ClassDefNode, ClassFieldDeclarationNode, ClassMethodDeclarationNode


from ._helpers_function import match_signatures


def get_class_by_name(
    class_name: str,
    multiple: bool = False,
) -> None | ClassDefNode | list[ClassDefNode]:
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
    _class: str | ClassDefNode,
    method_name: str,
    type_signature: list[TypeNode],
    is_static: bool = False,
) -> ClassMethodDeclarationNode | None:
    if isinstance(_class, str):
        class_instance = get_class_by_name(class_name=_class)
        if class_instance is None:
            return None
    elif isinstance(_class, ClassDefNode):
        class_instance = _class
    else:
        return None

    look_methods_in = class_instance.methods_defs if not is_static else class_instance.static_methods_defs
    for class_method in look_methods_in:
        if class_method.function_name != method_name:
            continue

        if match_signatures(args_signature=type_signature, function_signature=class_method.parameters_signature):
            return class_method
    return None


def get_class_field(
    _class: str | ClassDefNode,
    field_name: str,
) -> ClassFieldDeclarationNode | None:

    if isinstance(_class, str):
        class_instance = get_class_by_name(_class)
        if class_instance is None:
            return None

    elif isinstance(_class, ClassDefNode):
        class_instance = _class

    else:
        return None

    for field in class_instance.all_fields_definitions:
        if field.name == field_name:
            return field

    return None


def instantiate_generic_type(
    possibly_generic_type: TypeNode,
    class_instance: ClassDefNode,
    generic_args: list[TypeNode] | None = None,
) -> tuple[bool, TypeNode | None]:
    if possibly_generic_type.represents_generic_param:
        for generic, actual in zip(class_instance.generic_params, generic_args):
            if generic.name == possibly_generic_type.name:
                return True, actual
        else:
            return False, None
    else:
        return True, possibly_generic_type
