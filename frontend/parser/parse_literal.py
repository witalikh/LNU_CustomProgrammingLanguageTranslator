import frontend.abstract_syntax_tree as AST
from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag

from frontend.syntax import Keyword, TokenType

import frontend.parser.parse_operators as arith

from typing import Literal, Union



def parse_integer(parser: Parser) -> AST.IntegerLiteralNode:
    token_type = parser.current_token.type

    base: Literal[10, 16, 8, 2] = 10
    if token_type == TokenType.DECIMAL_INTEGER_LITERAL:
        base = 10
    elif token_type == TokenType.HEXADECIMAL_INTEGER_LITERAL:
        base = 16
    elif token_type == TokenType.OCTAL_INTEGER_LITERAL:
        base = 8
    elif token_type == TokenType.BINARY_INTEGER_LITERAL:
        base = 2
    else:
        parser.error(msg=f"Unexpected token {token_type}")

    value = parser.consume(token_type)
    line, position = parser.line_and_position_of_consumed_token()
    return AST.IntegerLiteralNode(value=value, base=base, line=line, position=position)


def parse_string(parser: Parser) -> AST.StringLiteralNode:
    value = parser.consume(TokenType.STRING_LITERAL)
    line, position = parser.line_and_position_of_consumed_token()
    return AST.StringLiteralNode(value=value, line=line, position=position)


def parse_this_keyword(parser: Parser, context: ContextFlag) -> Union[AST.ThisNode, AST.IdentifierNode]:
    _ = parser.consume(TokenType.KEYWORD, Keyword.THIS)
    line, position = parser.line_and_position_of_consumed_token()

    if not ContextFlag.match(context, flag=ContextFlag.CLASS & ContextFlag.FUNCTION):
        return AST.ThisNode(line=line, position=position)
    else:
        return AST.IdentifierNode(name="$this", line=line, position=position)


def parse_identifier(
    parser: Parser
) -> AST.IdentifierNode:
    identifier = parser.consume(TokenType.IDENTIFIER)
    line, position = parser.line_and_position_of_consumed_token()
    return AST.IdentifierNode(name=identifier, line=line, position=position)


def parse_list_or_keymap(
    parser: Parser,
    context: ContextFlag
) -> AST.ListLiteralNode | AST.KeymapLiteralNode | AST.EmptyLiteralNode:
    parser.consume(TokenType.OPENING_SQUARE_BRACKET)
    line, position = parser.line_and_position_of_consumed_token()

    arguments = []

    while parser.current_token.type != TokenType.CLOSING_SQUARE_BRACKET:
        argument = arith.parse_arithmetic_expression(parser, context=context)
        arguments.append(argument)

        if parser.match(TokenType.CLOSING_SQUARE_BRACKET):
            break
        parser.consume(TokenType.COMMA)

    parser.consume(TokenType.CLOSING_SQUARE_BRACKET)
    # line, position = parser.line_and_position_of_consumed_token()

    keymap_literals_count = sum(map(lambda x: isinstance(x, AST.KeymapElementNode), arguments))
    if keymap_literals_count == 0:
        if arguments:
            return AST.ListLiteralNode(elements=arguments, line=line, position=position)
        else:
            return AST.EmptyLiteralNode(line=line, position=position)
    elif keymap_literals_count == len(arguments):
        return AST.KeymapLiteralNode(elements=arguments, line=line, position=position)
    else:
        parser.error(msg="List/keymap literal cannot have both keymap and non-keymap expressions")

# def parse_arithmetic_expression_with_keymaps(parser: Parser, context: ContextFlag)
# -> AST.KeymapElementNode | AST.BinaryOperatorABCNode:
#     # absent associativity
#     left = parse_arithmetic_expression(parser, context)
#
#     if parser.match(TokenType.OPERATOR, Operator.KEYMAP_LITERAL):
#         parser.consume(TokenType.OPERATOR)
#         line, position = parser.line_and_position_of_consumed_token()
#         right = parse_arithmetic_expression(parser, context)
#         return AST.KeymapElementNode(
#             left=left, right=right,
#             line=line, position=position
#         )
#     else:
#         return left
