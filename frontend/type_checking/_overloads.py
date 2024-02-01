from ..abstract_syntax_tree import *

from .shared import error_logger, class_definitions, function_definitions


def validate_overloaded_function_definitions() -> bool:

    unique_functions_names = set()
    distinct_functions_names = set()

    for function in function_definitions:
        name = function.function_name
        if name in distinct_functions_names:
            unique_functions_names.discard(name)
        else:
            unique_functions_names.add(name)
        distinct_functions_names.add(name)

    overloads = distinct_functions_names.difference(unique_functions_names)
    if not overloads:
        return True

    overload_validations = [
        validate_overloaded_function_name(function_name)
        for function_name in overloads
    ]
    return all(overload_validations)


def validate_overloaded_function_name(
    function_name: str
):
    overloaded_function_parameters = {}

    for function in function_definitions:
        if function.function_name != function_name:
            continue

        parameters = get_parameters_signature(function.parameters)
        if parameters not in overloaded_function_parameters:
            overloaded_function_parameters[parameters] = [function]
        else:
            overloaded_function_parameters[parameters].append(function)

    has_no_duplicate_definitions = True
    for signature, overloads in overloaded_function_parameters.items():
        if len(overloads) == 1:
            continue
        has_no_duplicate_definitions = False
        for function_node in overloads:
            error_logger.add(
                function_node,
                f"Multiple overloads for function {function_name} with same signature {signature} found"
            )

    return has_no_duplicate_definitions
