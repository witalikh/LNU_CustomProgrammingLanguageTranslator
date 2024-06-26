from ._helpers_function import match_signatures
from ..abstract_syntax_tree import FunctionDefNode, ClassMethodDeclarationNode

from .shared import error_logger


def validate_overloaded_function_definitions(
    definitions: list[FunctionDefNode | ClassMethodDeclarationNode]
) -> bool:

    not_overloaded_function_names = set()
    distinct_functions_names = set()

    for function in definitions:
        name = function.function_name
        if name in distinct_functions_names:
            not_overloaded_function_names.discard(name)
        else:
            not_overloaded_function_names.add(name)
            distinct_functions_names.add(name)

    overloads = distinct_functions_names.difference(not_overloaded_function_names)
    if not overloads:
        return True

    # denoting different overloads for desugaring stage
    counter = {name: 0 for name in overloads}
    for function in definitions:
        if (name := function.function_name) in overloads:
            function.has_overloads = True
            function.overload_number = counter[name]
            counter[name] += 1

    overload_validations = [
        _validate_overloaded_function_name(definitions=definitions, function_name=function_name)
        for function_name in overloads
    ]
    return all(overload_validations)


def _validate_overloaded_function_name(
    definitions: list[FunctionDefNode | ClassMethodDeclarationNode],
    function_name: str
) -> bool:
    overloaded_functions: list[FunctionDefNode] = []

    for function in definitions:
        if function.function_name != function_name:
            continue

        overloaded_functions.append(function)

    has_no_duplicate_definitions = True
    for i in range(len(overloaded_functions)):
        for j in range(i + 1, len(overloaded_functions)):
            if match_signatures(
                args_signature=overloaded_functions[i].parameters_signature,
                function_signature=overloaded_functions[j].parameters_signature
            ):
                has_no_duplicate_definitions = False
                error_logger.add(
                    location=overloaded_functions[i],
                    reason=f"Multiple overloads for function {function_name} with same signature"
                    f"{overloaded_functions[i].parameters_signature} found"
                )

    return has_no_duplicate_definitions
