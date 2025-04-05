import logging
from itertools import repeat

from .tokens import Token
from .syntax import TokenType, KEYWORDS, Operator, Assignment, Comparison
from typing import Optional

numeric_bases = {
    'x': 16,
    'o': 8,
    'q': 4,
    'b': 2,
}

base_digits = {
    2: '01',
    4: '0123',
    8: '01234567',
    10: '0123456789',
    16: '0123456789ABCDEF',
}

base_literal = {
    2: TokenType.BINARY_INTEGER_LITERAL,
    4: TokenType.QUATERNARY_INTEGER_LITERAL,
    8: TokenType.OCTAL_INTEGER_LITERAL,
    10: TokenType.DECIMAL_INTEGER_LITERAL,
    16: TokenType.HEXADECIMAL_INTEGER_LITERAL,
}

class Scanner:
    """
    An iterator that yields tokens from a source code
    """

    def __init__(self, input_string: str):
        self.source_code = input_string

        self.start = 0
        self.current = 0

        self.position = 1
        self.line_number = 1

        self.tokens = []
        self.errors = []

    def is_eof(self) -> bool:
        return self.current >= len(self.source_code)

    def peek(self, offset=0) -> Optional[str]:
        if self.current + offset < len(self.source_code):
            return self.source_code[self.current + offset]
        else:
            return None

    def move(self, steps: int = 1):
        for _ in repeat(None, steps):
            self.current += 1
            if self.peek() == '\n':
                self.line_number += 1
                self.position = 1
            else:
                self.position += 1

    def add_token(self, token_type, value=None):
        token = Token(token_type, value, self.line_number, self.position)
        self.tokens.append(token)

    def add_error(self, msg):
        err_string = f"[Line {self.line_number}, at {self.position}] {msg}"
        logging.log(logging.ERROR, err_string)
        self.errors.append(err_string)

    def lex_all(self):
        while not self.is_eof():
            self.start = self.current
            self.lex_token()

        self.add_token(TokenType.END_OF_CODE)
        return self.tokens, self.errors


    def lex_token(self):
        self.lex_comments_and_whitespaces()
        char = self.peek()
        if char is None:
            return

        if char == '(':
            self.add_token(TokenType.OPENING_PARENTHESIS)
            self.move()

        elif char == ')':
            self.add_token(TokenType.CLOSING_PARENTHESIS)
            self.move()

        elif char == '[':
            self.add_token(TokenType.OPENING_SQUARE_BRACKET)
            self.move()

        elif char == ']':
            self.add_token(TokenType.CLOSING_SQUARE_BRACKET)
            self.move()

        elif char == '{':
            self.add_token(TokenType.BEGIN_OF_SCOPE)
            self.move()

        elif char == '}':
            self.add_token(TokenType.END_OF_SCOPE)
            self.move()

        elif char == ',':
            self.add_token(TokenType.COMMA)
            self.move()

        elif char == ';':
            self.add_token(TokenType.END_OF_STATEMENT)
            self.move()

        elif char.isdigit() or char == '.' and self.peek(+1).isdigit():
            self.lex_number()

        elif char in ':+-*/%=<>!@#.?$':
            self.lex_operator()
            self.move()

        # keywords and identifiers
        elif char.isalpha() or char == '_':
            self.lex_word()

        elif char == "\"":
            self.lex_string()

        elif char == ' ' or char == '\n':
            self.move()

        else:
            self.add_error(f"Invalid expression: {char}")
            self.move()



    def lex_comments_and_whitespaces(self):
        while not self.is_eof():
            if self.peek() == '\\' and self.peek(+1) == '*':
                while self.peek() != '*' or self.peek(+1) != '\\':
                    self.move()
                else:
                    self.move(2)
            if self.peek() == '#':
                while self.peek() != '\n':
                    self.move()
                else:
                    self.move()
            if self.peek() == '\n':
                self.move()
            if self.peek() == ' ':
                self.move()

            self.start = self.current
            return

    def lex_number(self):

        base = 10

        maybe_float = True
        is_complex = False
        first_dot_met = False

        while self.peek() not in ' \n':
            if self.current == self.start and self.peek() == '0':
                if self.peek(+1) in numeric_bases:
                    base = numeric_bases[self.peek(1)]
                    maybe_float = False
                    self.move(2)
                else:
                    self.move()

            if maybe_float:
                if self.peek().isdigit():
                    self.move()

                elif self.peek() in 'ij':
                    is_complex = True
                    self.move()

                elif self.peek() == '.':
                    if first_dot_met:
                        self.add_error("Invalid float literal: two dots at the same time")

                    first_dot_met = True
                    self.move()

                elif self.peek() in 'eE':
                    next_char = self.peek(+1)
                    if not (next_char.isdigit() or next_char in '+-'):
                        self.add_error("Invalid float literal: two dots at the same time")

                    self.move()
                    if self.peek() in '+-':
                        self.move()

                elif self.peek() == '_':
                    self.move()

                # elif self.peek() in " +-*/%@&|^<>=!?:;\\\n#,":
                #     break

                else:
                    break
                    # print(self.peek())
                    # self.add_error("Invalid float literal:")
                    # self.move()

            # handle integers in different bases
            else:
                if self.peek() in base_digits[base]:
                    self.move()
                elif self.peek() in " +-*/%@&|^<>=!?:;\\\n#,":
                    break
                elif self.peek() == "_":
                    self.move()
                elif self.peek():
                    self.add_error(f"Invalid integer literal for base {base}")

        # extract whole numeric
        num = self.source_code[self.start:self.current].replace('_', '')

        # convert into standard numeric
        try:
            if not first_dot_met:
                self.add_token(base_literal[base], num)
            else:
                if is_complex:
                    self.add_token(TokenType.IMAGINARY_FLOAT_LITERAL, complex(num))
                else:
                    self.add_token(TokenType.FLOAT_LITERAL, float(num))

        except ValueError:
            pass

    def lex_operator(self):

        # :+-*/%=<>!@#.?$

        char = self.peek()
        next_char = self.peek(+1)

        # '+', '+='
        if char == '+':
            if next_char == '=':
                self.move()
                self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_PLUS)
            else:
                self.add_token(TokenType.OPERATOR, Operator.PLUS)

        # '-', '-='
        elif char == '-':
            if next_char == '=':
                self.move()
                self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_MINUS)
            elif next_char == '>':
                self.move()
                self.add_token(TokenType.OPERATOR, Operator.REFERENCE_MEMBER_ACCESS)
            else:
                self.add_token(TokenType.OPERATOR, Operator.MINUS)

        # '&&', '&&=', '&=', '&'
        elif char == '&':
            if next_char == '&':
                if self.peek(+2) == '=':
                    self.move(2)
                    self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_FULL_AND)
                else:
                    self.move()
                    self.add_token(TokenType.OPERATOR, Operator.FULL_AND)
            elif next_char == '=':
                self.move()
                self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_BITWISE_AND)
            else:
                self.add_token(TokenType.OPERATOR, Operator.BITWISE_AND)

        # '^^', '^^=', '^=', '^'
        elif char == '^':
            if next_char == '^':
                if self.peek(+2) == '=':
                    self.move(2)
                    self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_FULL_XOR)
                else:
                    self.move()
                    self.add_token(TokenType.OPERATOR, Operator.FULL_XOR)
            elif next_char == '=':
                self.move()
                self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_BITWISE_XOR)
            else:
                self.add_token(TokenType.OPERATOR, Operator.BITWISE_XOR)

        # '||', '||=', '|=', '|'
        elif char == '|':
            if next_char == '|':
                if self.peek(+2) == '=':
                    self.move(2)
                    self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_FULL_OR)
                else:
                    self.move()
                    self.add_token(TokenType.OPERATOR, Operator.FULL_OR)
            elif next_char == '=':
                self.move()
                self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_BITWISE_OR)
            else:
                self.add_token(TokenType.OPERATOR, Operator.BITWISE_OR)

        # '~'
        elif char == '~':
            self.add_token(TokenType.OPERATOR, Operator.BITWISE_INVERSE)

        # '*', '**', '*=', '**='
        elif char == '*':
            if next_char == '*':
                if self.peek(+2) == '=':
                    self.move(2)
                    self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_POWER)
                else:
                    self.move()
                    self.add_token(TokenType.OPERATOR, Operator.POWER)
            else:
                if next_char == '=':
                    self.move()
                    self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_MULTIPLY)
                else:
                    self.add_token(TokenType.OPERATOR, Operator.MULTIPLY)

         # '/', '//', '/=', '//='
        elif char == '/':
            if next_char == '/':
                if self.peek(+2) == '=':
                    self.move(2)
                    self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_FLOOR_DIVIDE)
                else:
                    self.move()
                    self.add_token(TokenType.OPERATOR, Operator.FLOOR_DIVIDE)
            else:
                if next_char == '=':
                    self.move()
                    self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_DIVIDE)
                else:
                    self.add_token(TokenType.OPERATOR, Operator.DIVIDE)

        # '%', '%='
        elif char == '%':
            if next_char == '=':
                self.move()
                self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_MODULO)
            else:
                self.add_token(TokenType.OPERATOR, Operator.MODULO)

        # '@', '@='
        elif char == '@':
            if next_char == '=':
                self.move()
                self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_MATMUL)
            else:
                self.add_token(TokenType.OPERATOR, Operator.MATMUL)

        # '<=' '<' '<<' '<<='
        elif char == "<":
            if next_char == '=':
                self.move()
                self.add_token(TokenType.COMPARISON, Comparison.LESSER_OR_EQUAL)
            elif char == next_char:
                if self.peek(+2) == '=':
                    self.move(2)
                    self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_BITWISE_LSHIFT)
                else:
                    self.move()
                    self.add_token(TokenType.OPERATOR, Operator.BITWISE_LSHIFT)
            else:
                self.add_token(TokenType.COMPARISON, Comparison.LESSER)

        # '>=' '>' '>>' '>>='
        elif char == ">":
            if next_char == '=':
                self.move()
                self.add_token(TokenType.COMPARISON, Comparison.GREATER_OR_EQUAL)
            elif char == next_char:
                if self.peek(+2) == '=':
                    self.move(2)
                    self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_BITWISE_RSHIFT)
                else:
                    self.move()
                    self.add_token(TokenType.OPERATOR, Operator.BITWISE_RSHIFT)
            else:
                self.add_token(TokenType.COMPARISON, Comparison.GREATER)

        # '!=', '!=='
        elif char == "!" and next_char == "=":
            if self.peek(2) == '=':
                self.move(2)
                self.add_token(TokenType.COMPARISON, Comparison.NOT_STRICT_EQUAL)
            else:
                self.move()
                self.add_token(TokenType.COMPARISON, Comparison.NOT_EQUAL)

        # '==', '==='
        elif char == next_char == "=":
            if self.peek(2) == '=':
                self.move(2)
                self.add_token(TokenType.COMPARISON, Comparison.STRICT_EQUAL)
            else:
                self.move()
                self.add_token(TokenType.COMPARISON, Comparison.EQUAL)

        # ':='
        elif char == ":" and next_char == "=":
            self.move()
            self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.VALUE_ASSIGNMENT)

        # '=:'
        elif char == "=" and next_char == ":":
            self.move()
            self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.REVERSE_VALUE_ASSIGNMENT)

        # '=>'
        elif char == "=" and next_char == ">":
            self.move()
            self.add_token(TokenType.OPERATOR, Operator.IMPLY)

        # '='
        elif char == "=":
            self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.REFERENCE_ASSIGNMENT)

        # '::'
        elif char == next_char == ":":
            self.move()
            self.add_token(TokenType.OPERATOR, Operator.SCOPE_RESOLUTION)

        # ':'
        elif char == ":":
            self.add_token(TokenType.OPERATOR, Operator.KEYMAP_LITERAL)

        elif char == "?":
            if next_char == '=':
                self.move()
                self.add_token(TokenType.GENERIC_ASSIGNMENT, Assignment.COMPOUND_NULL_COALESCE)
            else:
                self.add_token(TokenType.OPERATOR, Operator.NULL_COALESCE)

        elif char == "$":
            self.add_token(TokenType.OPERATOR, Operator.INTERPOLATION)

        elif char == ".":
            if char == next_char == self.peek(+2) == ".":
                self.move(2)
                self.add_token(TokenType.OPERATOR, Operator.ELLIPSIS)
            else:
                self.add_token(TokenType.OPERATOR, Operator.OBJECT_MEMBER_ACCESS)

        else:
            self.add_error("Invalid operator")

    def lex_word(self):

        while (char := self.peek()) and (
                char.isalpha() or char == '_' or (self.current != self.start and char.isdigit())):
            self.move()

        name = self.source_code[self.start:self.current]
        print(name)
        if name in KEYWORDS:
            self.add_token(*KEYWORDS.get(name))
        else:
            self.add_token(TokenType.IDENTIFIER, name)

    def lex_string(self):

        self.move()

        escaped_backslash = False
        while self.peek() and (escaped_backslash or self.peek() != '"') and self.peek() != '\n':
            if self.peek() == '\\':
                escaped_backslash = not escaped_backslash
            if escaped_backslash and self.peek() != '\\':
                escaped_backslash = False
            self.move()
        else:
            if self.peek() != '"' or escaped_backslash:
                self.add_error("Invalid string literal")
            self.move()

        # omit quotes
        string = self.source_code[self.start:self.current]
        self.add_token(TokenType.STRING_LITERAL, string)

