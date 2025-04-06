import frontend.abstract_syntax_tree as AST
from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag

from frontend.syntax import TokenType, Keyword

import frontend.parser.parse_operators as arith
import frontend.parser.parse_literal as literals
import frontend.parser.parse_type as types


# TODO: string adequate parser, comments, refactor it into methods ...
def parse_primary_expression(parser: Parser, context: ContextFlag) -> AST.ASTNode:
    if parser.match((
        TokenType.DECIMAL_INTEGER_LITERAL,
        TokenType.HEXADECIMAL_INTEGER_LITERAL,
        TokenType.OCTAL_INTEGER_LITERAL,
        TokenType.BINARY_INTEGER_LITERAL
    )):
        return literals.parse_integer(parser)

    if parser.match(TokenType.IMAGINARY_FLOAT_LITERAL):
        value = parser.consume(TokenType.IMAGINARY_FLOAT_LITERAL)
        line, position = parser.line_and_position_of_consumed_token()
        return AST.ImaginaryFloatLiteralNode(value=value, line=line, position=position)

    if parser.match(TokenType.FLOAT_LITERAL):
        value = parser.consume(TokenType.FLOAT_LITERAL)
        line, position = parser.line_and_position_of_consumed_token()
        return AST.FloatLiteralNode(value=value, line=line, position=position)

    if parser.match(TokenType.IDENTIFIER):
        return literals.parse_identifier(parser)

    if parser.match(TokenType.STRING_LITERAL):
        return literals.parse_string(parser)

    if parser.match(TokenType.CHAR_LITERAL):
        value = parser.consume(TokenType.CHAR_LITERAL)
        line, position = parser.line_and_position_of_consumed_token()
        return AST.CharLiteralNode(value=value, line=line, position=position)

    if parser.match(TokenType.BOOLEAN_LITERAL):
        value = parser.consume(TokenType.BOOLEAN_LITERAL)
        line, position = parser.line_and_position_of_consumed_token()
        return AST.BooleanLiteralNode(value=value, line=line, position=position)

    if parser.match(TokenType.NULL_LITERAL):
        _ = parser.consume(TokenType.NULL_LITERAL)
        line, position = parser.line_and_position_of_consumed_token()
        return AST.NullLiteralNode(line=line, position=position)

    if parser.match(TokenType.UNDEFINED_LITERAL):
        _ = parser.consume(TokenType.UNDEFINED_LITERAL)
        line, position = parser.line_and_position_of_consumed_token()
        return AST.UndefinedLiteralNode(line=line, position=position)

    if parser.match(TokenType.BYTE_STRING_LITERAL):
        value = parser.consume(TokenType.BYTE_STRING_LITERAL)
        line, position = parser.line_and_position_of_consumed_token()
        return AST.ByteStringLiteralNode(value=value, line=line, position=position)

    if parser.match(TokenType.KEYWORD, Keyword.THIS):
        return literals.parse_this_keyword(parser, context)

    if parser.match(TokenType.OPENING_PARENTHESIS):
        parser.consume(TokenType.OPENING_PARENTHESIS)
        node = arith.parse_arithmetic_expression(parser, context)
        parser.consume(TokenType.CLOSING_PARENTHESIS)
        return node
    if parser.match(TokenType.OPENING_SQUARE_BRACKET):
        return literals.parse_list_or_keymap(parser, context)

    if parser.match((TokenType.SIMPLE_TYPE, TokenType.COMPOUND_TYPE, TokenType.TYPE_MODIFIER)):
        return types.parse_type_declaration(parser, context)

    parser.error(msg=f"Unexpected token {parser.current_token.value}")