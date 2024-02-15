from ..abstract_syntax_tree import *
from .shared import error_logger, class_definitions, function_definitions

from ._overloads import validate_overloaded_function_definitions


from ._type_validate import validate_type


def initialize_variables_environment_from_parameters(
    parameters: list[FunctionParameter]
) -> dict[str, TypeNode]:
    pass


def validate_all_function_definitions() -> bool:
    """
    Validate all global function definitions, including
    return type, parameters and statements typing
    :return: true if all function definitions are valid, otherwise false
    """
    valid_overloads = validate_overloaded_function_definitions(function_definitions)

    valid_functions = [
        _validate_function_definition(_function)
        for _function in function_definitions
    ]

    return valid_overloads and all(valid_functions)


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
    generics_context = None
    if isinstance(function_node.external_to, ClassDefinitionNode):
        generics_context = function_node.external_to.generic_params
    return all((
        validate_type(function_node.return_type),
        all((validate_type(x, generics_context) for x in function_node.parameters_signature)),
    ))
