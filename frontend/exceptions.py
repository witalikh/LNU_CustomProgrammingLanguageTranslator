"""
Module containing exceptions during front-end part of the programming Language translation
"""
# NOTE for developing:
# Here and only here should be declared any Exception class, and nothing else!


class UnknownTokenError(Exception):
    """
    This exception is for use to be thrown in the lexing process
    when an unknown token is encountered in the token stream.
    It holds the line number, position and the offending token string.
    """

    def __init__(self, token: str, line: int, position: int):
        self.token = token
        self.line = line
        self.position = position

    def __str__(self):
        return f"Line {self.line}, position {self.position}, found invalid token: {self.token}"


class ParsingException(Exception):
    """
    This exception is for use to be thrown in the parsing process
    when syntactically or semantically wrong tokens are encountered in the
    token stream when parsing the specific part of AST tree.
    It holds the line number, position and the reason token is invalid here.
    """
    def __init__(self, message: str, line: int, position: int):
        self.message = message
        self.line = line
        self.position = position

    def __str__(self) -> str:
        return f"Occurred parsing error at line {self.line}, position {self.position}: \n{self.message}"


class SemanticException(Exception):
    """
    This exception is for use to be thrown in the type-checking or desugaring process
    when semantically wrong tokens (mainly typization) are encountered in the AST tree.
    It holds the line number, position and the reason token is invalid here.
    Note: This exception is collected into a list, and then raised
    """
    def __init__(self, message: str, line: int, position: int):
        self.message = message
        self.line = line
        self.position = position

    def __str__(self) -> str:
        return f"Occurred parsing error at line {self.line}, position {self.position}: \n{self.message}"
