"""
Module containing token class and token types
(some kind of enum) used in the frontend part of translator
for building tokens during lexing and recognition when parsing AST tree.
"""
from frontend.syntax import TokenType


# NOTE for developing:
# 1. use uppercase for constants (new token types)
# 2. don't import anything except standard lib
# 3. TokenType class is not Enum just because to not spoil regex for the lexer
# 4. Values of constants doesn't even matter, just be sure to not repeat them



class Token:
    def __init__(self, token_type: TokenType, token_value: str, line_number: int, column_position: int):
        self._token_type = token_type
        self._token_value = token_value

        self._line_number = line_number
        self._column_position = column_position

    def __str__(self) -> str:
        return f"[{self._token_type.name}, {self._token_value}]"

    def __repr__(self) -> str:
        return f"[{self._token_type.name}, {self._token_value}]"

    @property
    def type(self) -> "TokenType":
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
