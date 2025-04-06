from frontend.exceptions import ParsingException
from frontend.syntax import TokenType
from frontend.tokens import Token
from typing import Iterator, KeysView, ValuesView, NoReturn, Optional, Union


# TODO: inherited generics should equal base


class Parser(object):
    """
    Class for generating an AST tree from a stream of lexical tokens
    """
    def __init__(self, tokens: Iterator[Token]):
        """
        Initialize the AST parser
        :param tokens: Iterator or generator providing lexical tokens
        """
        self._tokens = tokens

        # we store only prev, current and next tokens
        # as it's enough to make sensible predictions
        self._prev_token: Token | None = None
        self._curr_token: Token | None = next(self._tokens)
        self._next_token: Token | None = next(self._tokens, None)

    @property
    def prev_token(self) -> Token | None:
        """
        Returns the previous token that was previously consumed by the parser
        or None if no token was consumed yet
        """
        return self._prev_token

    @property
    def current_token(self) -> Token | None:
        """
        Returns the current token the parser is pointing at, and it's not consumed yet
        or None if the last token is recently consumed
        """
        return self._curr_token

    @property
    def next_token(self) -> Token | None:
        """ Returns the next token that is next to the current token
        or None if the parser is at the end of the token stream
        """
        return self._next_token

    def __next__(self) -> None:
        """
        Iterate through the token stream and update the previous, current and next tokens
        """
        self._prev_token = self._curr_token
        self._curr_token = self._next_token
        self._next_token = next(self._tokens, None)

    def consume(self, expected_type: TokenType, expected_value: Optional[str] = None) -> str:
        """
        Process current token and return the value of it,
        and set the next token as current one.
        It's important to provide the expected type of token that will be consumed,
        and in case of type mismatch, the ParsingException is raised.
        Also, an expected value or list/tuple/set of expected values can be provided
        to check if the consumed token matches the expected value, or if not, the ParsingException is raised.
        :param expected_type: expected token type to match against actual one
        :param expected_value: (optional) expected value or list/tuple/set of expected values
        :return: the value of consumed token
        """
        # store the copy of current token
        token = self._curr_token

        # token is passed when
        # 1. expected type matches
        # 2. if expected value or collection of values provided, check the value
        if token.type == expected_type and (
            expected_value is None or expected_value == token.value or (
            isinstance(expected_value, tuple) and token.value in expected_value
        )
        ):
            self.__next__()
            return token.value

        # token type mismatch => error
        if token.type != expected_type:
            msg = (f"Expected token of type {expected_type.name}, "
                   f"but got {token.type.name} ({token.value})")

        # only one token value is expected, but got different => error
        else:
            msg = (f"Expected token is {expected_value}, "
                   f"but got {token.value} (Token type {token.type.name})")
        self.error(msg)

    def match(self, expected_type, expected_value: Optional[Union[str, tuple]]= None) -> bool:
        """
        Checks if the current token might be consumed without raising an exception.
        :param expected_type: TokenType or collection of TokenTypes to match within them
        :param expected_value: (optional) possible token value or collection of values to match within them
        :return: boolean indicating if current token might be consumed
        """
        if isinstance(expected_type, TokenType):
            suitable_type = self._curr_token.type == expected_type
        elif isinstance(expected_type, (list, tuple, set, ValuesView, KeysView)):
            suitable_type = self._curr_token.type in expected_type
        else:
            return False

        if not suitable_type:
            return False

        if expected_value is None:
            return True
        elif isinstance(expected_value, str):
            return self._curr_token.value == expected_value
        elif isinstance(expected_value, (tuple, list, set, ValuesView, KeysView)):
            return self._curr_token.value in expected_value
        else:
            return False

    def line_and_position_of_consumed_token(self) -> tuple[int, int]:
        """
        Returns the line and position of the recently consumed token.
        Useful for debugging purposes.
        :return: line and position of the recently consumed token
        """
        return self._prev_token.line_number, self._prev_token.position

    def error(self, msg: str) -> NoReturn:
        """
        Raise an error message, with sufficient information to user
        which token (line and position in the code) is invalid.
        Presumes that the current token is the reason of error.
        :param msg: reason why the error occurred
        :raises: ParsingException
        """
        raise ParsingException(msg, self.current_token.line_number, self.current_token.position)
