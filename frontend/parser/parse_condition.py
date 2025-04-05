from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag
import frontend.abstract_syntax_tree as AST

from frontend.syntax import Keyword, TokenType

import frontend.parser.parse_operators as arith
import frontend.parser.parse_scope as scope


def _parse_condition(parser: Parser, context: ContextFlag) -> AST.ASTNode:
    parser.consume(TokenType.OPENING_PARENTHESIS)
    condition = arith.parse_arithmetic_expression(parser, context)
    parser.consume(TokenType.CLOSING_PARENTHESIS)
    return condition


def parse_full_if_else_statement(parser: Parser, context: ContextFlag) -> AST.IfElseNode:

    # validate scope: it shouldn't be directly in the class (but can be in class method)
    if ContextFlag.strict_match(context, flag=ContextFlag.CLASS):
        parser.error(
            msg="If-else statements are not allowed inside class definition outside of method or constructor."
        )

    parser.consume(TokenType.KEYWORD, Keyword.IF)
    line, position = parser.line_and_position_of_consumed_token()

    condition = _parse_condition(parser, context)
    if_scope = scope.parse_scope(parser, context)

    root_node = AST.IfElseNode(condition=condition, if_scope=if_scope, else_scope=None, line=line, position=position)
    current_node: AST.IfElseNode = root_node

    # consume else ifs as much as possible.
    while parser.match(TokenType.KEYWORD, Keyword.ELSE):
        parser.consume(TokenType.KEYWORD, Keyword.ELSE)

        if parser.match(TokenType.KEYWORD, Keyword.IF):
            # Handle "else if" condition
            parser.consume(TokenType.KEYWORD, Keyword.IF)
            line, position = parser.line_and_position_of_consumed_token()

            elif_condition = _parse_condition(parser, context)
            elif_scope = scope.parse_scope(parser, context)

            obj = AST.IfElseNode(condition=elif_condition,
                                 if_scope=elif_scope, else_scope=None, line=line, position=position)
            current_node.else_node = obj
            current_node = obj
        else:
            # Handle last "else" block
            current_node.else_scope = scope.parse_scope(parser, context)

    # semicolon is not required here, but not redundant
    if parser.match(TokenType.END_OF_STATEMENT):
        parser.consume(TokenType.END_OF_STATEMENT)
    return root_node

