import re
import logging

from .exceptions import UnknownTokenError
from .tokens import TokenType, Token
from typing import Sequence, Iterator, Self


class TokenScannerIterator:
    """
    An iterator that yields tokens from a source code
    """

    def __init__(self, lexer, input_string: str):
        self.position = 0

        self.line_number = 0
        self._current_relative_position = 0
        self._next_relative_position = 0

        self.lexer: Lexer = lexer
        self.input_string = input_string

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Token:
        """
        Iterate through the text.
        Returns next non-comment token
        :return:
        """
        # if finished scanning
        if self.done_scanning():
            logging.log(logging.INFO, "Finished scanning tokens successfully!")
            raise StopIteration

        # iterate through all comment tokens
        token_type, token_value = self.scan_next_token()
        while token_type == TokenType.COMMENT:
            token_type, token_value = self.scan_next_token()

        return Token(token_type, token_value, self.line_number, self._current_relative_position)

    def error(self):
        err = UnknownTokenError(self.input_string[self.position], self.line_number, self._current_relative_position)
        logging.log(logging.ERROR, str(err))
        raise err

    def done_scanning(self) -> bool:
        return self.position >= len(self.input_string)

    def scan_next_token(self) -> tuple[str, str] | None:
        if self.done_scanning():
            return None

        self._current_relative_position = self._next_relative_position

        whitespace_match = self.lexer.whitespace_regex.match(self.input_string, self.position)
        if whitespace_match:
            if self.input_string[self.position] == "\n":
                self.line_number += whitespace_match.group().count("\n")
                self._current_relative_position = len(whitespace_match.group()[whitespace_match.group().rfind('\n'):])
                self._next_relative_position = self._current_relative_position
            else:
                self._current_relative_position += whitespace_match.end() - self.position
                self._next_relative_position += whitespace_match.end() - self.position
            self.position = whitespace_match.end()

        match = self.lexer.regex.match(self.input_string, self.position)
        if match is None:
            self.error()

        self._next_relative_position += (match.end() - self.position)
        self.position = match.end()

        value = match.group(match.lastgroup)
        if match.lastgroup in self.lexer.callbacks:
            value = self.lexer.callbacks[match.lastgroup](self, value)
        return match.lastgroup, value


class Lexer:
    """
    A lexical scanner. It takes in an input and a set of rules based
    on regular expressions. It then scans the input and returns the
    tokens one-by-one. It is meant to be used through iterating.
    """

    def __init__(
        self,
        rules: list[tuple[str, str]],
        case_sensitive: bool = True
    ):
        self.callbacks = {}
        self.case_sensitive = case_sensitive

        if self.case_sensitive:
            flags = re.M
        else:
            flags = re.M | re.I

        self._join_rules(rules, flags)

    def _join_rules(self, rules: Sequence[tuple[str, str]], flags: re.RegexFlag) -> None:
        parts = []
        for name, rule in rules:
            if not isinstance(name, str):
                name = str(name)
            if not isinstance(rule, str):
                rule, callback = rule
                self.callbacks[name] = callback
            parts.append(f"(?P<{name}>{rule})")

        self.regex = re.compile("|".join(parts), flags)
        self.whitespace_regex = re.compile(r"\s*", re.MULTILINE)

    def scan(self, _input) -> Iterator[Token]:
        return TokenScannerIterator(self, _input)
