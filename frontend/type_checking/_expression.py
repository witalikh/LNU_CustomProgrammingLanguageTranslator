from ..abstract_syntax_tree import *

from .shared import error_logger, class_definitions, function_definitions
from ..abstract_syntax_tree.unary_node import ReferenceOperatorNode


from ._overloads import match_signatures

# TODO: implement this all
# TODO: describe modules
def check_arithmetic_expression(
    expression: ASTNode,
    environment: dict[str, TypeNode]
):
    if isinstance(expression, IdentifierNode):
        return check_identifier(expression, environment)
    elif isinstance(expression, FunctionCallNode):
        return check_function_call(expression, environment)
    elif isinstance(expression, IndexNode):
        return check_indexation_call(expression, environment)
    elif isinstance(expression, MemberOperatorNode):
        return check_member_access(expression, environment)
    elif isinstance(expression, AllocationOperatorNode):
        return check_allocation_expression(expression, environment)
    elif isinstance(expression, ReferenceOperatorNode):
        return check_referencing_expression(expression, environment)

    elif isinstance(expression, ArithmeticOperatorNode):
        return check_arithmetic_binary_operation(expression, environment)
    elif isinstance(expression, LogicalOperatorNode):
        return check_logical_binary_operation(expression, environment)
    elif isinstance(expression, ComparisonNode):
        return check_comparison_binary_operation(expression, environment)
    elif isinstance(expression, KeymapOperatorNode):
        raise NotImplemented
    elif isinstance(expression, UnaryOperatorNode):
        return check_unary_arithmetic_operation(expression, environment)

    elif isinstance(expression, DeductionNode):
        return True, None
    elif isinstance(expression, LiteralNode):
        return check_literal(expression)
    else:
        error_logger.add(expression.location, f"Unsupported expression {type(expression)}")
        return False, None


def check_identifier(
    identifier: IdentifierNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    if identifier.name in environment:
        return True, environment[identifier.name]
    error_logger.add(identifier.location, f"Variable '{identifier.name}' is not defined in this context")
    return False, None


def check_function_call(
    function_node: FunctionCallNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    # assumes that function definitions are proper
    potential_functions = [
        func for func in function_definitions
        if func.function_name == function_node.identifier
    ]

    if not potential_functions:
        error_logger.add(function_node.location, f"Function with name {function_node.identifier} does not exist")
        return False, None

    all_valid = True
    args_type = []
    for expr in function_node.arguments:
        valid, type_ = check_arithmetic_expression(expr, environment)
        args_type.append(type_)
        if not valid:
            error_logger.add(expr.location, "Invalid argument expression")
            all_valid = False

    if not all_valid:
        return False, None

    # assume validated and the first guess is right
    found_match = False
    matched_function = None
    for potential_function in potential_functions:
        matched_signature = match_signatures(args_type, potential_function.parameters_signature)
        if matched_signature:
            matched_function = potential_function
            found_match = True
            break

    if not found_match:
        error_logger.add(
            function_node.location,
            f"Function with name {function_node} and given signature {str(args_type)} doesn't exist"
        )
        return False, None
    else:
        return True, matched_function.return_type


# TODO: finish indexation
def check_indexation_call(
    identifier: IndexNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    if not isinstance(identifier, IndexNode):
        return False, None

    indexable = identifier.variable
    valid, return_type = check_arithmetic_expression(indexable, environment)

    if not isinstance(return_type, TypeNode):
        error_logger.add(f"Invalid expression type on index: {type(return_type)}")
        return False, None


def check_member_access(
    identifier: MemberOperatorNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    # TODO: implement
    pass


def check_allocation_expression(
    identifier: AllocationOperatorNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    # TODO: implement
    pass


def check_referencing_expression(
    identifier: ReferenceOperatorNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    # TODO: implement
    pass


def check_arithmetic_binary_operation(
    identifier: ArithmeticOperatorNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    # TODO: implement
    pass


def check_logical_binary_operation(
    identifier: LogicalOperatorNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    # TODO: implement
    pass


def check_comparison_binary_operation(
    identifier: ComparisonNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    # TODO: implement
    pass


def check_unary_arithmetic_operation(
    identifier: UnaryOperatorNode,
    environment: dict[str, TypeNode]
) -> tuple[bool, TypeNode | None]:
    # TODO: implement
    pass


def check_literal(
    identifier: LiteralNode,
) -> tuple[bool, TypeNode | None]:
    # TODO: implement
    pass
