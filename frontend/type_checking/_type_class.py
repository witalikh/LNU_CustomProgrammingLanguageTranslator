from ..abstract_syntax_tree import *
from .shared import class_definitions


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
