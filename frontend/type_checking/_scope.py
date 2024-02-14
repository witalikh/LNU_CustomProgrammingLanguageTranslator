from ..abstract_syntax_tree import *

from .shared import error_logger, class_definitions, function_definitions
from ._environment import get_variable_type_from_environment


def validate_scope(
    scope: ScopeNode,
    environment: dict[str, TypeNode],
    is_loop: bool = False,
    is_function: bool = False,
    is_class: bool = False,
    expected_return_type: ClassDefinitionNode | TypeNode | None = None,
    current_class: TypeNode | None = None,
    is_class_nonstatic_method: bool = False,
    outermost_function_scope: bool = False
):
    # if empty
    if not scope.statements:
        if is_loop:
            error_logger.add(
                scope.statements,
                "Loop requires at least one statement in the scope"
            )
            scope.valid = False
            return False

        if is_function and expected_return_type is not None:
            error_logger.add(
                scope.statements,
                "Function requires at least one return statement in the scope"
            )
            scope.valid = False
            return False

    # validate every expression
    valid_expression = [
        _validate_expression(
            expr,
            environment,
            is_loop,
            is_function,
            is_class,
            expected_return_type,
            current_class,
            is_class_nonstatic_method,
        )
        for expr in scope.statements
    ]

    scope.valid = all(valid_expression)
    return scope.valid

    # last_expression = scope.statements[-1]
    # if isinstance(last_expression, ReturnNode):
    #     scope.all_paths_return = True
    #
    # elif isinstance(last_expression, (WhileNode, IfElseNode, ScopeNode)):
    #     scope.all_paths_return = last_expression.all_paths_return
    #
    # else:
    #     scope.all_paths_return = False
    #
    #
    # # TODO: all paths return
    # if is_function and outermost_function_scope and expected_return_type is not None:
    #     if not scope.all_paths_return:
    #         error_logger.add(
    #             scope.location,
    #             f"Not all paths return value in this scope"
    #         )
    #         return False


def _validate_expression(
    expression: ASTNode,
    environment: dict[str, TypeNode],
    is_loop: bool = False,
    is_function: bool = False,
    is_class: bool = False,
    expected_return_type: TypeNode | None = None,
    current_class: ClassDefinitionNode | TypeNode | None = None,
    is_class_nonstatic_method: bool = False
):
    if isinstance(expression, IfElseNode):
        pass

    elif isinstance(expression, WhileNode):
        pass

    elif isinstance(expression, ScopeNode):
        pass

    elif isinstance(expression, AssignmentNode):
        pass

    elif isinstance(expression, VariableDeclarationNode):
        pass

    elif isinstance(expression, ReturnNode):
        pass

    elif isinstance(expression, ContinueNode):
        pass

    elif isinstance(expression, BreakNode):
        pass
