from ..abstract_syntax_tree import *

from .shared import error_logger, class_definitions, function_definitions
from ._environment import get_variable_type_from_environment

def validate_expression(
    expression: ASTNode,
    environment: dict[str, TypeNode]
) -> bool:
    if isinstance(expression, VariableDeclarationNode):
        return _validate_variable_declaration(expression, environment)
        # expression.type
        # expression.name
        # expression.value
        # expression.operator

    if isinstance(expression, AssignmentNode):
        return _validate_assignment_expression(expression.left, expression.operator, expression.right, environment)

    elif isinstance(expression, IfElseNode):
        pass

    elif isinstance(expression, WhileNode):
        pass

    elif isinstance(expression, FunctionCallNode):
        pass

def _validate_variable_declaration(
    expression: VariableDeclarationNode,
    environment: dict[str, TypeNode]
) -> bool:
    variable_name = expression.name
    if variable_name in environment:
        error_logger.add(expression.location, f"Name {variable_name} already exists in this context")
        return False


def _validate_assignment_expression(
    left: IndexNode | IdentifierNode,
    operator: str,
    right: ASTNode,
    environment: dict[str, TypeNode]
) -> bool:
    valid_left, expression_type = _check_identifier_assignable(left, environment)

    variable_type = get_variable_type_from_environment( environment)


def _check_identifier_assignable(
    identifier: IdentifierNode | IndexNode | ASTNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    if isinstance(identifier, IdentifierNode):
        variable_type = get_variable_type_from_environment(identifier.name, environment, identifier.location)
        if variable_type is None:
            return False, None
        return True, variable_type
    elif isinstance(identifier, IndexNode):
        valid_indexation, expression_type = _check_indexation(identifier, environment)
    else:
        error_logger.add(identifier.location, f"Invalid expression type on assignment lhs: {type(identifier)}")
        return False, None

def validate_scope_expressions(
    scope: ScopeNode,
    environment: dict[str, TypeNode]
) -> bool:

    location = scope.location
    expressions = scope.statements

    if not check_no_duplicate_variable_declarations_in_block(error_logger, expressions, location):
        return False

    if not expressions:
        return True

    else:

        current_environment = environment.copy()
        for expression in expressions:
            result = check_expression(
                expression,
                current_environment,

            )

    pass