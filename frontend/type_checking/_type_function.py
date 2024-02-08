from ..abstract_syntax_tree import TypeNode
from ._type_match import match_types, strict_match_types


def match_signatures(args_signature: list[TypeNode], function_signature: list[TypeNode]) -> bool:

    # TODO: (in future) variadic args
    # something like that
    # if None in function_signature:
    #     index_of_variadic = function_signature.index(None)
    #     if index_of_variadic != len(function_signature) - 1:
    #         return
    #     else:
    #         variadic = True

    if len(args_signature) != len(function_signature):
        return False

    for arg, param in zip(args_signature, function_signature):
        if not match_types(arg, param):
            return False
    return True


def strict_match_signatures(args_signature: list[TypeNode], function_signature: list[TypeNode]) -> bool:
    if len(args_signature) != len(function_signature):
        return False

    for arg, param in zip(args_signature, function_signature):
        if not strict_match_types(arg, param):
            return False
    return True
