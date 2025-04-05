from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag
import frontend.abstract_syntax_tree as AST

from frontend.syntax import TokenType, Operator, Comparison
import frontend.parser.parse_primary as primary
import frontend.parser.parse_type as types
import frontend.parser.parse_literal as literals

from typing import Union, TypeVar, TypeAlias


X = TypeVar('X')
T: TypeAlias = Union[X, AST.ASTNode]
BinOpT: TypeAlias = T[AST.BinaryOperatorABCNode]


def parse_arithmetic_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    return parse_assignment_expression(parser, context)

def parse_assignment_expression(parser: Parser, context: ContextFlag) -> T[AST.AssignmentNode]:
    left_expr = parse_logical_or_expression(parser, context)

    while parser.match(TokenType.GENERIC_ASSIGNMENT):

        operator = parser.consume(TokenType.GENERIC_ASSIGNMENT)
        line, position = parser.line_and_position_of_consumed_token()

        right_expr = parse_logical_or_expression(parser, context)
        left_expr = AST.AssignmentNode(
            left=left_expr, operator=operator, right=right_expr, line=line, position=position
        )

    return left_expr

def parse_logical_or_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_logical_xor_expression(parser, context)

    while parser.match(TokenType.OPERATOR, (Operator.OR, Operator.FULL_OR)):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_logical_xor_expression(parser, context)
        left = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Logical,
            left=left, operator=operator, right=right, line=line, position=position
        )

    return left

def parse_logical_xor_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_logical_and_expression(parser, context)

    while parser.match(TokenType.OPERATOR, (Operator.XOR, Operator.FULL_XOR)):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_logical_and_expression(parser, context)
        left = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Logical,
            left=left, operator=operator, right=right, line=line, position=position
        )

    return left

def parse_logical_and_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_bitwise_or_expression(parser, context)

    while parser.match(TokenType.OPERATOR, (Operator.AND, Operator.FULL_AND)):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_bitwise_or_expression(parser, context)
        left = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Logical,
            left=left, operator=operator, right=right, line=line, position=position
        )

    return left

def parse_bitwise_or_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_bitwise_xor_expression(parser, context)

    while parser.match(TokenType.OPERATOR, Operator.BITWISE_OR):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_bitwise_xor_expression(parser, context)
        left = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Arithmetic,
            left=left, operator=operator, right=right, line=line, position=position
        )

    return left

def parse_bitwise_xor_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_bitwise_and_expression(parser, context)

    while parser.match(TokenType.OPERATOR, Operator.BITWISE_XOR):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_bitwise_and_expression(parser, context)
        left = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Arithmetic,
            left=left, operator=operator, right=right, line=line, position=position
        )

    return left

def parse_bitwise_and_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_equality_expression(parser, context)

    while parser.match(TokenType.OPERATOR, Operator.BITWISE_AND):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_equality_expression(parser, context)
        left = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Arithmetic,
            left=left, operator=operator, right=right, line=line, position=position
        )

    return left

def parse_equality_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_comparison_expression(parser, context)

    statements = []
    while parser.match(TokenType.COMPARISON, (
        Comparison.EQUAL,
        Comparison.NOT_EQUAL,
        Comparison.STRICT_EQUAL,
        Comparison.NOT_STRICT_EQUAL,
    )):
        operator = parser.consume(TokenType.COMPARISON)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_comparison_expression(parser, context)

        statements.append(AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Comparison,
            left=left, operator=operator, right=right, line=line, position=position
        ))
        left = right

    if not statements:
        return left
    return __parse_chained_comparisons(statements=statements)

def parse_comparison_expression(parser: Parser, context: ContextFlag) -> BinOpT:

    statements = []
    left = parse_membership_operator_expression(parser, context)

    while parser.match(TokenType.COMPARISON, (
        Comparison.LESSER_OR_EQUAL,
        Comparison.GREATER_OR_EQUAL,
        Comparison.LESSER,
        Comparison.GREATER,
    )):
        operator = parser.consume(TokenType.COMPARISON)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_membership_operator_expression(parser, context)

        statements.append(AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Comparison,
            left=left, operator=operator, right=right, line=line, position=position
        ))
        left = right

    if not statements:
        return left
    return __parse_chained_comparisons(statements=statements)

def __parse_chained_comparisons(statements: list[AST.BinaryOperatorABCNode]) -> BinOpT:
    if len(statements) == 1:
        return statements[0]

    statements_count = len(statements)
    root = AST.BinaryOperatorABCNode(
        category=AST.OperatorCategory.Logical,
        left=statements[0], operator=Operator.AND, right=None)  # type: ignore
    curr = root
    for index, statement in enumerate(statements):
        if index == 0:
            continue
        elif index != statements_count - 1:
            new_node = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Logical,
                left=statement, operator=Operator.AND, right=None)  # type: ignore
            curr.right = new_node
            curr = new_node
        else:
            curr.right = statement
    return root

def parse_membership_operator_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_bitwise_shift_expression(parser, context)

    if parser.match(TokenType.COMPARISON, Comparison.MEMBERSHIP_OPERATOR):
        operator = parser.consume(TokenType.COMPARISON, Comparison.MEMBERSHIP_OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_bitwise_shift_expression(parser, context)
        left = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Comparison,
            left=left, operator=operator, right=right, line=line, position=position
        )

    return left

def parse_bitwise_shift_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_additive_expression(parser, context)

    while parser.match(TokenType.OPERATOR, (
        Operator.BITWISE_LSHIFT,
        Operator.BITWISE_RSHIFT
    )):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_additive_expression(parser, context)
        left = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Comparison,
            left=left, operator=operator, right=right, line=line, position=position
        )

    return left

def parse_additive_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_multiplicative_expression(parser, context)

    while parser.match(TokenType.OPERATOR, (Operator.PLUS, Operator.MINUS)):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_multiplicative_expression(parser, context)
        left = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Arithmetic,
            left=left, operator=operator, right=right, line=line, position=position
        )

    return left

def parse_multiplicative_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_arithmetic_unary_expression(parser, context)

    while parser.match(TokenType.OPERATOR, (
        Operator.MULTIPLY,
        Operator.DIVIDE,
        Operator.FLOOR_DIVIDE,
        Operator.MODULO,
    )):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_arithmetic_unary_expression(parser, context)
        left = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Arithmetic,
            left=left, operator=operator, right=right, line=line, position=position
        )

    return left

def parse_arithmetic_unary_expression(
        parser: Parser, context: ContextFlag
        ) -> T[Union[AST.UnaryOperatorABCNode, AST.BinaryOperatorABCNode]]:
    if parser.match(TokenType.OPERATOR, (
        Operator.PLUS,
        Operator.MINUS,
        Operator.BITWISE_INVERSE,
    )):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_power_expression(parser, context)
        return AST.UnaryOperatorABCNode(
            category=AST.OperatorCategory.Arithmetic,
            operator=operator, expression=right, line=line, position=position
        )
    else:
        return parse_power_expression(parser, context)

def parse_power_expression(parser: Parser, context: ContextFlag) -> BinOpT:
    left = parse_other_unary_expression(parser, context)
    right_expressions = [left]
    operators_positions = []

    while parser.match(TokenType.OPERATOR, Operator.POWER):
        _ = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_other_unary_expression(parser, context)
        right_expressions.append(right)
        operators_positions.append((line, position))

    if len(right_expressions) == 1:
        return left

    result = AST.BinaryOperatorABCNode(
        category=AST.OperatorCategory.Arithmetic,
        left=right_expressions[-2], operator=Operator.POWER, right=right_expressions[-1],
        line=operators_positions[-1][0], position=operators_positions[-1][1]
    )
    for _left, (_line, _position) in reversed(list(zip(right_expressions[:-2], operators_positions[:-1]))):
        result = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Arithmetic,
            left=_left, operator=Operator.POWER, right=result,
            line=_line, position=_position
        )

    return result

# TODO: reference/dereference
def parse_other_unary_expression(
        parser: Parser, context: ContextFlag
        ) -> T[Union[AST.UnaryOperatorABCNode, AST.MemberOperatorNode]]:
    if parser.match(TokenType.OPERATOR, (Operator.NOT,)):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_dynamic_memory_allocation(parser, context)
        return AST.UnaryOperatorABCNode(
            category=AST.OperatorCategory.Logical,
            operator=operator, expression=right, line=line, position=position
        )
    elif parser.match(TokenType.OPERATOR, (Operator.REFERENCE, Operator.DEREFERENCE)):
        operator = parser.consume(TokenType.OPERATOR)
        line, position = parser.line_and_position_of_consumed_token()
        right = parse_dynamic_memory_allocation(parser, context)
        return AST.UnaryOperatorABCNode(
            category=AST.OperatorCategory.Reference,
            operator=operator, expression=right, line=line, position=position
        )
    else:
        return parse_dynamic_memory_allocation(parser, context)

def parse_dynamic_memory_allocation(
        parser: Parser, context: ContextFlag
        ) -> T[Union[AST.UnaryOperatorABCNode, AST.MemberOperatorNode]]:

    if parser.match(TokenType.OPERATOR, Operator.NEW_INSTANCE):
        operator = parser.consume(TokenType.OPERATOR, Operator.NEW_INSTANCE)
        line, position = parser.line_and_position_of_consumed_token()
        right = types.parse_base_type(parser, context, as_constructor=True)
        return AST.UnaryOperatorABCNode(
            category=AST.OperatorCategory.Allocation,
            operator=operator, expression=right, line=line, position=position
        )
    elif parser.match(TokenType.OPERATOR, Operator.DELETE_INSTANCE):
        operator = parser.consume(TokenType.OPERATOR, Operator.DELETE_INSTANCE)
        line, position = parser.line_and_position_of_consumed_token()
        right = literals.parse_identifier(parser)
        return AST.UnaryOperatorABCNode(
            category=AST.OperatorCategory.Allocation,
            operator=operator, expression=right, line=line, position=position
        )
    else:
        return parse_function_call(parser, context) # primary.parse_primary_expression(parser, context)

def parse_function_call(parser: Parser, context: ContextFlag) -> T[AST.FunctionCallNode]:
    left = parse_indexation_call(parser, context)

    while parser.match(TokenType.OPENING_PARENTHESIS):
        parser.consume(TokenType.OPENING_PARENTHESIS)
        line, position = parser.line_and_position_of_consumed_token()

        arguments = []

        while parser.current_token.type != TokenType.CLOSING_PARENTHESIS:
            argument = parse_arithmetic_expression(parser, context=context)
            arguments.append(argument)

            if parser.match(TokenType.CLOSING_PARENTHESIS):
                break
            parser.consume(TokenType.COMMA)

        parser.consume(TokenType.CLOSING_PARENTHESIS)

        left = AST.FunctionCallNode(
            identifier=left, arguments=arguments, line=line, position=position
        )

    return left


def parse_indexation_call(parser: Parser, context: ContextFlag):
    left = parse_member(parser, context)

    while parser.match(TokenType.OPENING_SQUARE_BRACKET):
        parser.consume(TokenType.OPENING_SQUARE_BRACKET)
        line, position = parser.line_and_position_of_consumed_token()

        arguments = []

        while parser.current_token.type != TokenType.CLOSING_SQUARE_BRACKET:
            argument = parse_arithmetic_expression(parser, context=context)
            arguments.append(argument)

            if parser.match(TokenType.CLOSING_SQUARE_BRACKET):
                break
            parser.consume(TokenType.COMMA)

        parser.consume(TokenType.CLOSING_SQUARE_BRACKET)
        left = AST.IndexNode(variable=left, arguments=arguments, line=line, position=position)

    return left


def parse_member(parser: Parser, context: ContextFlag):
    operators = (Operator.OBJECT_MEMBER_ACCESS, Operator.REFERENCE_MEMBER_ACCESS)

    left = primary.parse_primary_expression(parser, context)

    while parser.match(TokenType.OPERATOR, operators):
        op = parser.consume(TokenType.OPERATOR, operators)
        line, position = parser.line_and_position_of_consumed_token()
        identifier = parse_function_call(parser, context)
        left = AST.MemberOperatorNode(left, op, identifier, line=line, position=position)
    return left
