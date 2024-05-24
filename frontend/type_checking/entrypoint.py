from ..abstract_syntax_tree import ProgramNode
from .shared import error_logger, class_definitions, function_definitions

from .classes.entrypoint import validate_all_class_definitions
from .functions.entrypoint import validate_all_function_definitions
from ._scope import validate_scope

import sys


def type_check_program(program: ProgramNode) -> bool:
    """
    Check entire program for type errors
    :param program: parsed AST tree root
    :return: true if program is valid else false
    """
    # init global variables
    class_definitions.extend(program.class_definitions)
    function_definitions.extend(program.function_definitions)

    valid_program = _check_program(program)
    if not valid_program:
        for error in error_logger:
            print(error, file=sys.stderr)
    return valid_program


def _check_program(program: ProgramNode) -> bool:
    valid_class_defs = validate_all_class_definitions()
    valid_function_defs = validate_all_function_definitions()

    valid_main_statements = validate_scope(
        scope=program,
        environment={},
        is_loop=False,
        is_function=False,
        is_class=False,
        expected_return_type=None,
        current_class=None,
        is_class_nonstatic_method=False,
        outermost_function_scope=False
    )

    valid = all([valid_class_defs, valid_function_defs, valid_main_statements])
    program.valid = valid
    return valid
