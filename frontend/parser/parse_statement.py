from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag
import frontend.abstract_syntax_tree as AST

from frontend.syntax import Keyword, TokenType

import frontend.parser.parse_scope as scope
import frontend.parser.parse_condition as ifs
import frontend.parser.parse_function as func
import frontend.parser.parse_loop as loops
import frontend.parser.parse_class as classes
import frontend.parser.parse_type as types


def parse_statement(parser: Parser, context: ContextFlag) -> AST.ASTNode:
    if not parser.match(TokenType.KEYWORD):
        pass

    if parser.match(TokenType.BEGIN_OF_SCOPE):
        return scope.parse_scope(parser, context)

    if parser.match(TokenType.KEYWORD, Keyword.IF):
        return ifs.parse_full_if_else_statement(parser, context)

    if parser.match(TokenType.KEYWORD, Keyword.WHILE):
        return loops.parse_full_while_statement(parser, context)

    if parser.match(TokenType.KEYWORD, Keyword.CLASS):
        return classes.parse_full_class_definition(parser, context)

    if parser.match(TokenType.KEYWORD, Keyword.FUNCTION):
        return func.parse_full_function_definition(parser, context)

    # return statement
    if parser.match(TokenType.KEYWORD, Keyword.RETURN):
        return func.parse_full_return_statement(parser, context)

    # break
    if parser.match(TokenType.KEYWORD, Keyword.BREAK):
        return loops.parse_full_break_statement(parser, context)

    # continue
    if parser.match(TokenType.KEYWORD, Keyword.CONTINUE):
        return loops.parse_full_continue_statement(parser, context)

    if parser.match(TokenType.CLASS_KEYWORD):
        return classes.parse_full_class_keywords(parser, context)

    if parser.match((TokenType.SIMPLE_TYPE, TokenType.COMPOUND_TYPE, TokenType.TYPE_MODIFIER)):
        return types.parse_full_variable_declaration(parser, context)

    return types.parse_full_expression(parser, context)