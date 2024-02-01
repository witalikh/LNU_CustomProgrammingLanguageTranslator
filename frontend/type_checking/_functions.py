from ..abstract_syntax_tree import *
from .shared import error_logger, class_definitions, function_definitions

from ._overloads import validate_overloaded_function_definitions


def validate_all_function_definitions() -> bool:
    """
    Validate all global function definitions, including
    return type, parameters and statements typing
    :return: true if all function definitions are valid, otherwise false
    """
    valid_overloads = validate_overloaded_function_definitions()

    valid_functions = [
        _validate_function_definition(_function)
        for _function in function_definitions
    ]

    return valid_overloads and all(valid_functions)


def get_parameters_signature(parameters: list[FunctionParameter]) -> tuple[str]:
    pass


def _validate_function_definition(
    function_node: FunctionDeclarationNode
) -> bool:
    """
    Validate a concrete function

    :param function_node: function to be validated
    :return: true if entire function is valid, otherwise false
    """
    valid_signature = _validate_function_signature(function_node)

    # TODO: function generics
    # valid_generics = validate_generics(function_node)

    # valid_block,

    return_type = function_node.return_type


def _validate_function_signature(
    function_node: FunctionDeclarationNode
) -> bool:
    pass
