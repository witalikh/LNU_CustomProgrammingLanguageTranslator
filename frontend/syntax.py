from etc import (
    CustomEnum,
    join_bounded_keywords_as_regex,
    bounded,
    join_partially_bounded_keywords_as_regex,
    join_unbounded_keywords_as_regex
)
from tokens import TokenType


class SimpleType(CustomEnum):

    BOOLEAN = "boolean"  # BIT
    BYTE = "byte"  # 8 bits int
    SHORT_INTEGER = "short integer"  # 16-bit integer
    INTEGER = "integer"  # 32-bit integer
    LONG_INTEGER = "long integer"  # 64-bit integer
    EXTENDED_INTEGER = "extended integer"

    FLOAT = "float"
    DOUBLE = "double"

    COMPLEX = "complex"

    CHAR = "char"
    STRING = "string"
    BYTESTRING = "bytestring"
    STREAM = "stream"


class CompoundType(CustomEnum):
    ARRAY = "array"
    LIST = "list"
    KEYMAP = "keymap"
    SET = "set"


class TypeModifier(CustomEnum):
    CONST = "const"
    NULLABLE = "nullable"
    REFERENCE = "reference"


class ClassModifierKeyword(CustomEnum):
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"

    VIRTUAL = "virtual"
    OVERRIDE = "override"

    STATIC = "static"


class Keyword(CustomEnum):
    IF = "if"
    ELSE = "else"
    FOR = "for"
    WHILE = "while"
    FUNCTION = "function"
    BREAK = "break"
    CONTINUE = "continue"
    RETURN = "return"
    TRY = "try"
    CATCH = "catch"
    FINALLY = "finally"
    STRUCT = "struct"

    # OOP
    CLASS = "class"
    THIS = "this"
    OPERATOR = "operator"
    TYPE = "type"  # considered as keyword for generic params

    FROM = "from"


class Operator(CustomEnum):
    # member access
    OBJECT_MEMBER_ACCESS = "."
    REFERENCE_MEMBER_ACCESS = "->"
    SCOPE_RESOLUTION = "::"

    # arithmetic
    PLUS = "+"
    MINUS = "-"
    POWER = "**"
    MULTIPLY = "*"
    FLOOR_DIVIDE = "//"
    DIVIDE = "/"
    MODULO = "%"

    # logical (short-circuit)
    AND = "and"
    OR = "or"
    XOR = "xor"
    NOT = "not"

    # logical (full check)
    FULL_AND = "&&"
    FULL_OR = "||"
    FULL_XOR = "^^"

    # bitwise
    BITWISE_XOR = "^"
    BITWISE_AND = "&"
    BITWISE_OR = "|"
    BITWISE_RSHIFT = ">>"
    BITWISE_LSHIFT = "<<"
    BITWISE_INVERSE = "~"

    # comparison
    LESSER_OR_EQUAL = "<="
    GREATER_OR_EQUAL = ">="
    NOT_EQUAL = "!="
    GREATER = ">"
    LESSER = "<"
    EQUAL = "=="
    STRICT_EQUAL = "==="
    NOT_STRICT_EQUAL = "!=="

    MEMBERSHIP_OPERATOR = "in"

    # syntax sugar
    FUNCTIONAL = "@"

    # literals
    KEYMAP_LITERAL = ":"

    # unary
    INTERPOLATION = "$"

    # pointers
    REFERENCE = "ref"
    DEREFERENCE = "deref"

    # type casting
    TYPE_CAST = "as"
    NULL_COALESCE = "??"
    NEW_INSTANCE = "new"
    DELETE_INSTANCE = "delete"


class Operands(CustomEnum):
    DEDUCTION = "?"
    TERMINATION = "!"


class Assignment(CustomEnum):
    VALUE_ASSIGNMENT = ":="
    REFERENCE_ASSIGNMENT = "="

    COMPOUND_PLUS = "+="
    COMPOUND_MINUS = "-="
    COMPOUND_MULTIPLY = "*="
    COMPOUND_DIVIDE = "/="
    COMPOUND_POWER = "**="
    COMPOUND_MODULO = "%="
    COMPOUND_FLOOR_DIVIDE = "//="

    # compound bitwise
    COMPOUND_BITWISE_XOR = "^="
    COMPOUND_BITWISE_AND = "&="
    COMPOUND_BITWISE_OR = "|="
    COMPOUND_BITWISE_RSHIFT = ">>="
    COMPOUND_BITWISE_LSHIFT = "<<="


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

        (TokenType.GENERIC_ASSIGNMENT, ASSIGNMENTS_REGEX),
        (TokenType.OPERATOR, OPERATORS_REGEX),
        (TokenType.OPERAND, OPERANDS_REGEX),

        (TokenType.IDENTIFIER, IDENTIFIER_REGEX),

        (TokenType.COMMENT, COMMENT_REGEX),
    ] + [
        (name, symbol) for name, symbol in DELIMITERS.items()
    ]
)
