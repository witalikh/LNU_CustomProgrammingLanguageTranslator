from ..abstract_syntax_tree import *
from .shared import function_definitions, error_logger

from ._overloads import validate_overloaded_function_definitions
from ._scope import validate_scope

from ._helpers_function import instantiate_environment_from_function_parameters
from ._type_get import check_arithmetic_expression, match_types
from ._type_validate import validate_type


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
    valid_parameters_declaration = _validate_function_parameters(function_node)

    if function_node.external_to:
        concrete_class = function_node.external_to
        valid_return_type = validate_type(function_node.return_type, concrete_class.generic_params)
        valid_implementation = validate_scope(
            scope=function_node.function_body,
            environment=instantiate_environment_from_function_parameters(function_node.parameters),
            is_loop=False,
            is_function=True,
            is_class=False,
            expected_return_type=function_node.return_type,
            current_class=concrete_class,
            is_class_nonstatic_method=False,
            outermost_function_scope=True,
        )
    else:
        valid_return_type = validate_type(function_node.return_type)
        valid_implementation = validate_scope(
            scope=function_node.function_body,
            environment=instantiate_environment_from_function_parameters(function_node.parameters),
            is_loop=False,
            is_function=True,
            is_class=False,
            expected_return_type=function_node.return_type,
            current_class=None,
            is_class_nonstatic_method=False,
            outermost_function_scope=True,
        )

    # Validation end: FunctionDeclarationNode
    valid_function = all((
        valid_return_type,
        valid_signature,
        valid_parameters_declaration,
        valid_implementation
    ))
    function_node.valid = valid_function
    return valid_function


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


def _validate_function_parameters(
    function_node: FunctionDeclarationNode
) -> bool:
    # Validation end: FunctionParameter
    valid = True
    for p in function_node.parameters:
        if p.default_value is not None:
            # TODO: for defaults, no other variable is used
            is_valid, expr_type = check_arithmetic_expression(p.default_value, {})
            if not is_valid:
                valid = False
                p.valid = False

            if not match_types(expr_type, p.type_node):
                valid = False
                p.valid = False
                error_logger.add(
                    p.location,
                    f"Default field value type mismatch: {expr_type.name} detected instead of {f.type.name}"
                )

        else:
            p.valid = True

    return valid
