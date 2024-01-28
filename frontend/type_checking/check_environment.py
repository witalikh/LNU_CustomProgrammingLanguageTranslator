from ..abstract_syntax_tree import *
from .core import collect_error

# TODO: everything in type checker!!!

def get_class_definition(class_name: str, class_definitions: list) -> list:
    pass


def validate_class_definition(class_name: str, class_definitions:list[ClassDefinitionNode]) -> tuple[bool, list]:
    matching_class_definitions = []


def validate_type(type_to_check: TypeNode, class_definitions: list[ClassDefinitionNode]) -> tuple[bool, list]:
    if isinstance(type_to_check, SimpleTypeNode):
        return True, []
    elif isinstance(type_to_check, UserDefinedTypeNode):
        return validate_class_definition(type_to_check, class_definitions)