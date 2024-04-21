from ..abstract_syntax_tree import *

from .shared import error_logger

from ._type_get import check_arithmetic_expression
from ._type_match import match_types
from ._type_validate import validate_type
from ..semantics import TypeEnum, Assignment


def validate_scope(
    scope: ScopeNode | ProgramNode,
    environment: dict[str, TypeNode],
    is_loop: bool = False,
    is_function: bool = False,
    is_class: bool = False,
    expected_return_type:  TypeNode | None = None,
    current_class: ClassDefinitionNode | None = None,
    is_class_nonstatic_method: bool = False,
    outermost_function_scope: bool = False
):
    own_environment = environment.copy()

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
            own_environment,
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
    current_class: ClassDefinitionNode | None = None,
    is_class_nonstatic_method: bool = False
):
    if isinstance(expression, IfElseNode):
        valid_if_cond, if_cond_type = check_arithmetic_expression(
            expression.condition,
            environment,
            outermost=False,
            context_class=current_class,
            is_nonstatic_method=is_class_nonstatic_method
        )
        valid_if_scope = validate_scope(
            expression.if_scope,
            environment,
            is_loop,
            is_function,
            is_class,
            expected_return_type,
            current_class,
            is_class_nonstatic_method,
            False,
        )
        valid_else_scope = True
        if expression.else_scope:
            valid_else_scope = validate_scope(
                expression.else_scope,
                environment,
                is_loop,
                is_function,
                is_class,
                expected_return_type,
                current_class,
                is_class_nonstatic_method,
                False,
            )

        return all((
            valid_if_cond,
            if_cond_type is not None and if_cond_type.name == TypeEnum.BOOLEAN,
            valid_if_scope,
            valid_else_scope
        ))

    elif isinstance(expression, WhileNode):
        valid_while_cond, while_cond_type = check_arithmetic_expression(
            expression.condition,
            environment,
            outermost=False,
            context_class=current_class,
            is_nonstatic_method=is_class_nonstatic_method
        )
        valid_while_scope = validate_scope(
            expression.while_scope,
            environment,
            True,
            is_function,
            is_class,
            expected_return_type,
            current_class,
            is_class_nonstatic_method,
            False,
        )
        return all((
            valid_while_cond,
            while_cond_type is not None and while_cond_type.name == TypeEnum.BOOLEAN,
            valid_while_scope,
        ))

    elif isinstance(expression, ScopeNode):
        return validate_scope(
            expression,
            environment,
            is_loop,
            is_function,
            is_class,
            expected_return_type,
            current_class,
            is_class_nonstatic_method,
            False,
        )

    elif isinstance(expression, VariableDeclarationNode):

        if expression.name in environment:
            error_logger.add(
                expression.location,
                "Variable is already defined in current context"
            )
            expression.valid = False
            return False

        # TODO: generic typed name aren't allowed outside class declaration context
        if not validate_type(expression.type, []):
            return False

        if expression.value:
            valid_expr, expr_type = check_arithmetic_expression(
                expression.value,
                environment,
                outermost=False,
                context_class=current_class,
                is_nonstatic_method=is_class_nonstatic_method
            )
            if not valid_expr or not expr_type:
                expression.valid = False
                return False

            match expression.operator:
                case Assignment.VALUE_ASSIGNMENT:
                    if expr_type.is_reference:
                        error_logger.add(
                            expression.location,
                            f"Use '=' assignment operator for references!"
                        )
                        expression.valid = False
                        return False
                case Assignment.REFERENCE_ASSIGNMENT:
                    if not expr_type.is_reference:
                        error_logger.add(
                            expression.location,
                            f"Use ':=' assignment operator for values!"
                        )
                        expression.valid = False
                        return False
                case _:
                    error_logger.add(
                        expression.location,
                        f"Invalid assignment operator for variable initialization: {expression.operator}"
                    )
                    expression.valid = False
                    return False

            if not match_types(expr_type, expression.type):
                error_logger.add(
                    expression.location,
                    f"Type mismatch for assignment operator: {expr_type.name} and {expression.type.name}"
                )
                expression.valid = False
                return False

        # Validation end: VariableDeclarationNode
        environment[expression.name] = expression.type
        expression.valid = True
        return True

    elif isinstance(expression, ReturnNode):
        if not is_function:
            error_logger.add(
                expression.location,
                f"Invalid usage of return keyword: non-function/method context"
            )
            return False

        if expression.value is None and expected_return_type is not None:
            error_logger.add(
                expression.location,
                f"Expected some value of type {expected_return_type.name} to return"
            )
            return False

        if expression.value is not None and expected_return_type is None:
            error_logger.add(
                expression.location,
                f"Expected no return value for procedure"
            )
            return False

        if expression.value is None and expected_return_type is None:
            return True

        is_valid_expr, expr_type = check_arithmetic_expression(
            expression.value, environment,
            outermost=False,
            context_class=current_class,
            is_nonstatic_method=is_class_nonstatic_method
        )

        if not is_valid_expr:
            # error is already logged
            return False

        if not match_types(expr_type, expected_return_type):
            error_logger.add(
                expression.location,
                f"Expected {expected_return_type}, but got {expr_type}"
            )
            return False

        return True

    elif isinstance(expression, ContinueNode):
        if not is_loop:
            error_logger.add(
                expression.location,
                f"Break keyword cannot be used outside of loop"
            )
            return False
        return True

    elif isinstance(expression, BreakNode):
        if not is_loop:
            error_logger.add(
                expression.location,
                f"Continue keyword cannot be used outside of loop"
            )
            return False
        return True

    else:
        return check_arithmetic_expression(
            expression,
            environment,
            outermost=True,
            context_class=current_class,
            is_nonstatic_method=is_class_nonstatic_method
        )[0]
