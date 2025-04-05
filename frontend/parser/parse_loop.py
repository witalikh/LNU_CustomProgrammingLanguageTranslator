import frontend.abstract_syntax_tree as AST
from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag

from frontend.syntax import TokenType, Keyword

import frontend.parser.parse_scope as scope
import frontend.parser.parse_operators as arith


def _parse_condition(parser: Parser, context: ContextFlag) -> AST.ASTNode:
    parser.consume(TokenType.OPENING_PARENTHESIS)
    condition = arith.parse_arithmetic_expression(parser, context)
    parser.consume(TokenType.CLOSING_PARENTHESIS)
    return condition


def parse_full_while_statement(parser: Parser, context: ContextFlag) -> AST.WhileNode:

    # validate scope: it shouldn't be directly in the class (but can be in class method)
    if ContextFlag.strict_match(context, flag=ContextFlag.CLASS):
        parser.error(
            "Loops are not allowed inside class definition outside of method or constructor."
        )

    # modify context to allow BREAK and CONTINUE expressions
    current_context = ContextFlag.add(context, flag=ContextFlag.LOOP)

    parser.consume(TokenType.KEYWORD, Keyword.WHILE)
    line, position = parser.line_and_position_of_consumed_token()

    condition = _parse_condition(parser, current_context)
    while_scope = scope.parse_scope(parser, current_context)
    if parser.match(TokenType.END_OF_STATEMENT):
        parser.consume(TokenType.END_OF_STATEMENT)
    return AST.WhileNode(condition=condition, while_scope=while_scope, line=line, position=position)

def parse_full_break_statement(parser: Parser, context: ContextFlag, **kwargs) -> AST.BreakNode:

    parser.consume(TokenType.KEYWORD, Keyword.BREAK)
    line, position = parser.line_and_position_of_consumed_token()

    expression = None
    if not parser.match(TokenType.END_OF_STATEMENT):
        expression = arith.parse_arithmetic_expression(parser, context)
    parser.consume(TokenType.END_OF_STATEMENT)

    # scope check: needs loop
    if expression is None:
        if not ContextFlag.match(context, flag=ContextFlag.LOOP):
            parser.error(msg=f"Unexpected token {parser.prev_token.value} out of loop.")

        loop = kwargs.get('loop')
        if not loop:
            raise NotImplementedError

        return AST.BreakNode(loop=loop, line=line, position=position)
    else:
        return AST.BreakNode(error=expression, line=line, position=position)

def parse_full_continue_statement(parser: Parser, context: ContextFlag, **kwargs) -> AST.ContinueNode:

    parser.consume(TokenType.KEYWORD, Keyword.CONTINUE)
    line, position = parser.line_and_position_of_consumed_token()

    expression = None
    if not parser.match(TokenType.END_OF_STATEMENT):
        expression = arith.parse_arithmetic_expression(parser, context)
    parser.consume(TokenType.END_OF_STATEMENT)

    if not expression:
        # scope check: needs loop
        if not ContextFlag.match(context, flag=ContextFlag.LOOP):
            parser.error(msg=f"Unexpected token {parser.current_token.value} out of loop.")

        loop = kwargs.get('loop')
        if not loop:
            raise NotImplementedError

        return AST.ContinueNode(loop=loop, line=line, position=position)
    else:
        return AST.ContinueNode(error=expression, line=line, position=position)
