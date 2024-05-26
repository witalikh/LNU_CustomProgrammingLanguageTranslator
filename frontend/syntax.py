from ._syntax.keywords import Keyword, ClassModifierKeyword
from ._syntax.operators import Operator, Assignment, Comparison
from ._syntax.types_compound import CompoundType
from ._syntax.types_modifier import TypeModifier
from ._syntax.types_simple import SimpleType
from .etc import (
    CustomEnum,
    join_bounded_keywords_as_regex,
    bounded,
    join_partially_bounded_keywords_as_regex,
    join_unbounded_keywords_as_regex
)
from .tokens import TokenType


class Operands(CustomEnum):
    DEDUCTION = "?"
    TERMINATION = "!"


COMPARISON_REGEX = join_unbounded_keywords_as_regex(Comparison.values())
ASSIGNMENTS_REGEX = join_unbounded_keywords_as_regex(Assignment.values())
OPERATORS_REGEX = join_partially_bounded_keywords_as_regex(Operator.values())
OPERANDS_REGEX = join_partially_bounded_keywords_as_regex(Operands.values())

# LITERALS
# INTEGERS & FLOATS
DECIMAL_INTEGER_REGEX = r'(0|[1-9]\d*)'
HEXADECIMAL_INTEGER_REGEX = r'0[xX][0-9a-fA-F]+'
OCTAL_INTEGER_REGEX = r'0[oO]?[0-7]+'
BINARY_INTEGER_REGEX = r'0[bB][01]+'

FLOAT_REGEX = r'(?<!\d)(\d*\.\d+|\.\d+|\d+[eE][-+]?\d+)(?!\d)'  # r'(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'
IMAGINARY_FLOAT_REGEX = r'\d+(\.\d*)?[jJ]'


# REST LITERALS
STRING_REGEX = r'"([^"\\]*(\\.[^"\\]*)*)"'
CHAR_REGEX = r"^'.'$"
BYTESTRING_REGEX = r"`\\x[0-9a-fA-F]{2}(\\x[0-9a-fA-F]{2})*`"
BOOLEAN_REGEX = join_bounded_keywords_as_regex(('true', 'false'))
NULL_REGEX = bounded('null')
UNDEFINED_REGEX = bounded('undefined')

# TYPES REGEX
SIMPLE_TYPES_REGEX = join_bounded_keywords_as_regex(SimpleType.values())
COMPOUND_TYPES_REGEX = join_bounded_keywords_as_regex(CompoundType.values())
TYPES_MODIFIER_REGEX = join_bounded_keywords_as_regex(TypeModifier.values())

# KEYWORDS, IDENTIFIERS AND COMMENTS
KEYWORDS_REGEX = join_bounded_keywords_as_regex(Keyword.values())
CLASS_KEYWORDS_REGEX = join_bounded_keywords_as_regex(ClassModifierKeyword.values())
IDENTIFIER_REGEX = r"[a-zA-Z_][a-zA-Z0-9_]*"
COMMENT_REGEX = r"#.*$"

# DELIMITERS
DELIMITERS = {
    TokenType.BEGIN_OF_SCOPE: r"\{",
    TokenType.END_OF_SCOPE: r"\}",

    TokenType.END_OF_STATEMENT: ";",
    TokenType.COMMA: ",",

    TokenType.OPENING_SQUARE_BRACKET: r"\[",
    TokenType.CLOSING_SQUARE_BRACKET: r"\]",
    TokenType.OPENING_PARENTHESIS: r"\(",
    TokenType.CLOSING_PARENTHESIS: r"\)",

    TokenType.END_OF_CODE: "$",
    TokenType.COLON: ":"
}
RULES = (
    [
        (TokenType.SIMPLE_TYPE, SIMPLE_TYPES_REGEX),
        (TokenType.COMPOUND_TYPE, COMPOUND_TYPES_REGEX),
        (TokenType.TYPE_MODIFIER, TYPES_MODIFIER_REGEX),
        (TokenType.KEYWORD, KEYWORDS_REGEX),

        (TokenType.CLASS_KEYWORD, CLASS_KEYWORDS_REGEX),

        (TokenType.IMAGINARY_FLOAT_LITERAL, IMAGINARY_FLOAT_REGEX),
        (TokenType.FLOAT_LITERAL, FLOAT_REGEX),


        (TokenType.HEXADECIMAL_INTEGER_LITERAL, HEXADECIMAL_INTEGER_REGEX),
        (TokenType.OCTAL_INTEGER_LITERAL, OCTAL_INTEGER_REGEX),
        (TokenType.BINARY_INTEGER_LITERAL, BINARY_INTEGER_REGEX),
        (TokenType.DECIMAL_INTEGER_LITERAL, DECIMAL_INTEGER_REGEX),

        (TokenType.STRING_LITERAL, STRING_REGEX),
        (TokenType.CHAR_LITERAL, CHAR_REGEX),
        (TokenType.BYTE_STRING_LITERAL, BYTESTRING_REGEX),
        (TokenType.NULL_LITERAL, NULL_REGEX),
        (TokenType.UNDEFINED_LITERAL, UNDEFINED_REGEX),
        (TokenType.BOOLEAN_LITERAL, BOOLEAN_REGEX),

        (TokenType.COMPARISON, COMPARISON_REGEX),
        (TokenType.GENERIC_ASSIGNMENT, ASSIGNMENTS_REGEX),
        (TokenType.OPERATOR, OPERATORS_REGEX),
        (TokenType.OPERAND, OPERANDS_REGEX),

        (TokenType.IDENTIFIER, IDENTIFIER_REGEX),

        (TokenType.COMMENT, COMMENT_REGEX),
    ] + [
        (name, symbol) for name, symbol in DELIMITERS.items()
    ]
)
