from ._helpers_function import match_signatures
from ..abstract_syntax_tree import FunctionDeclarationNode, ClassMethodDeclarationNode

from .shared import error_logger


def validate_overloaded_function_definitions(
    definitions: list[FunctionDeclarationNode | ClassMethodDeclarationNode]
) -> bool:

    unique_functions_names = set()
    distinct_functions_names = set()

    for function in definitions:
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
        _validate_overloaded_function_name(definitions, function_name)
        for function_name in overloads
    ]
    return all(overload_validations)


def _validate_overloaded_function_name(
    definitions: list[FunctionDeclarationNode | ClassMethodDeclarationNode],
    function_name: str
):
    overloaded_functions = []

    for function in definitions:
        if function.function_name != function_name:
            continue

        overloaded_functions.append(function)

    has_no_duplicate_definitions = True
    for i in range(len(overloaded_functions)):
        for j in range(i + 1, len(overloaded_functions)):
            if match_signatures(
                overloaded_functions[i].parameters_signature,
                overloaded_functions[j].parameters_signature
            ):
                has_no_duplicate_definitions = False
                error_logger.add(
                    overloaded_functions[i],
                    f"Multiple overloads for function {function_name} with same signature"
                    f"{overloaded_functions[i].parameters_signature} found"
                )

    return has_no_duplicate_definitions
