"""
Module containing token class and token types
(some kind of enum) used in the frontend part of translator
for building tokens during lexing and recognition when parsing AST tree.
"""
# NOTE for developing:
# 1. use uppercase for constants (new token types)
# 2. don't import anything except standard lib
# 3. TokenType class is not Enum just because to not spoil regex for the lexer
# 4. Values of constants doesn't even matter, just be sure to not repeat them


class TokenType:
    END_OF_STATEMENT = "END_OF_STATEMENT"
    COMMA = "COMMA"
    COLON = "COLON"

    BEGIN_OF_CODE = "BEGIN_CODE"
    END_OF_CODE = "END_CODE"

    BEGIN_OF_SCOPE = "BEGIN_OF_SCOPE"
    END_OF_SCOPE = "END_OF_SCOPE"

    OPENING_PARENTHESIS = "OPENING_BRACKET"
    CLOSING_PARENTHESIS = "CLOSING_BRACKET"

    OPENING_SQUARE_BRACKET = "OPENING_SQUARE_BRACKET"
    CLOSING_SQUARE_BRACKET = "CLOSING_SQUARE_BRACKET"

    DECIMAL_INTEGER_LITERAL = "DECIMAL_INTEGER_LITERAL"
    HEXADECIMAL_INTEGER_LITERAL = "HEXADECIMAL_INTEGER_LITERAL"
    OCTAL_INTEGER_LITERAL = "OCTAL_INTEGER_LITERAL"
    BINARY_INTEGER_LITERAL = "BINARY_INTEGER_LITERAL"

    FLOAT_LITERAL = "FLOAT_LITERAL"
    IMAGINARY_FLOAT_LITERAL = "IMAGINARY_FLOAT_LITERAL"

    STRING_LITERAL = "STRING_LITERAL"
    CHAR_LITERAL = "CHAR_LITERAL"
    # BYTE_LITERAL = "BYTE_LITERAL"
    BYTE_STRING_LITERAL = "BYTE_STRING"
    BOOLEAN_LITERAL = "BOOLEAN_LITERAL"
    NULL_LITERAL = "NULL_LITERAL"
    UNDEFINED_LITERAL = "UNDEFINED_LITERAL"

    SIMPLE_TYPE = "SIMPLE_TYPE"
    COMPOUND_TYPE = "COMPOUND_TYPE"
    TYPE_MODIFIER = "TYPE_MODIFIER"
    IDENTIFIER = "IDENTIFIER"

    GENERIC_ASSIGNMENT = "GENERIC_ASSIGNMENT"
    OPERATOR = "OPERATOR"
    OPERAND = "OPERAND"

    COMMENT = "COMMENT"

    KEYWORD = "KEYWORDS"
    CLASS_KEYWORD = "CLASS_KEYWORDS"


class Token:
    def __init__(self, token_type: str, token_value: str, line_number: int, column_position: int):
        self._token_type = token_type
        self._token_value = token_value

        self._line_number = line_number
        self._column_position = column_position

    def __str__(self) -> str:
        return f"{str(self._token_type)}, {self._token_value}"

    @property
    def type(self) -> str:
        return self._token_type

    @property
    def value(self) -> str:
        return self._token_value

    @property
    def line_number(self) -> int:
        return self._line_number

    @property
    def position(self) -> int:
        return self._column_position
