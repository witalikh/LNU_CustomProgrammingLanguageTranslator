from enum import IntEnum, StrEnum, auto


class TokenType(IntEnum):
    END_OF_STATEMENT = auto()
    COMMA = auto()
    ELLIPSIS = auto()

    BEGIN_OF_CODE = auto()
    END_OF_CODE = auto()

    BEGIN_OF_SCOPE = auto()
    END_OF_SCOPE = auto()

    OPENING_PARENTHESIS = auto()
    CLOSING_PARENTHESIS = auto()

    OPENING_SQUARE_BRACKET = auto()
    CLOSING_SQUARE_BRACKET = auto()

    DECIMAL_INTEGER_LITERAL = auto()
    HEXADECIMAL_INTEGER_LITERAL = auto()
    OCTAL_INTEGER_LITERAL = auto()
    QUATERNARY_INTEGER_LITERAL = auto()
    BINARY_INTEGER_LITERAL = auto()

    FLOAT_LITERAL = auto()
    IMAGINARY_FLOAT_LITERAL = auto()

    STRING_LITERAL = auto()
    CHAR_LITERAL = auto()
    BYTE_LITERAL = auto()
    BYTE_STRING_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NULL_LITERAL = auto()
    UNDEFINED_LITERAL = auto()

    # blow
    SIMPLE_TYPE = auto()
    COMPOUND_TYPE = auto()
    TYPE_MODIFIER = auto()
    IDENTIFIER = auto()

    OPERATOR = auto()
    COMPARISON = auto()
    GENERIC_ASSIGNMENT = auto()
    KEYWORD = auto()
    CLASS_KEYWORD = auto()


    # OP_ASSIGN_REF = auto()  #
    # OP_ASSIGN_VAL = auto()  #
    # OP_ASSIGN_IVAL = auto()  #
    #
    # OP_PLUS = auto()  #
    # OP_MINUS = auto()  #
    # OP_STAR = auto()  #
    # OP_AT = auto()  #
    # OP_SLASH = auto()  #
    # OP_MODULO = auto()  #
    #
    # OP_POWER = auto()  #
    # OP_FLOORDIV = auto()  #
    #
    # OP_CMP_LT = auto()  #
    # OP_CMP_LTE = auto()  #
    # OP_CMP_GT = auto()  #
    # OP_CMP_GTE = auto()  #
    # OP_CMP_EQ = auto()  #
    # OP_CMP_NE = auto()  #
    # OP_CMP_IN = auto()  #
    # OP_CMP_EQS = auto()  #
    # OP_CMP_NES = auto()  #
    #
    # OP_BOOL_AND = auto()  #
    # OP_BOOL_OR = auto()  #
    # OP_BOOL_XOR = auto()  #
    # OP_BOOL_NOT = auto()  #
    #
    # OP_BOOL_FULL_OR = auto()  #
    # OP_BOOL_FULL_AND = auto()  #
    # OP_BOOL_FULL_XOR = auto()  #
    #
    # OP_BIT_AND = auto()  #
    # OP_BIT_OR = auto()  #
    # OP_BIT_XOR = auto()  #
    # OP_BIT_NOT = auto()  #
    #
    # OP_BIT_LSHIFT = auto()  #
    # OP_BIT_RSHIFT = auto()  #
    #
    # OP_COLON = auto()  #
    # OP_COALESCE = auto()  #
    #
    # OP_DOT = auto()  #
    # OP_REF_ACCESS = auto()  #
    #
    # OP_SCOPE = auto()  #
    #
    # OP_ALLOC_NEW = auto()  #
    # OP_ALLOC_DEL = auto()  #
    #
    # OP_REF = auto()  #
    # OP_DEREF = auto()  #
    #
    # OP_INTERPOLATE = auto()  #
    # OP_IMPLY = auto()  #
    #
    # OP_TYPECAST = auto()  #
    # OP_FALLBACK = auto()  #
    #
    # OP_IASSIGN_PLUS = auto()  #
    # OP_IASSIGN_MINUS = auto()  #
    # OP_IASSIGN_STAR = auto()  #
    # OP_IASSIGN_AT = auto()  #
    # OP_IASSIGN_SLASH = auto()  #
    # OP_IASSIGN_MODULO = auto()  #
    #
    # OP_IASSIGN_POWER = auto()  #
    # OP_IASSIGN_FLOORDIV = auto()  #
    #
    # OP_IASSIGN_BOOL_FULL_OR = auto()  #
    # OP_IASSIGN_BOOL_FULL_AND = auto()  #
    # OP_IASSIGN_BOOL_FULL_XOR = auto()  #
    #
    # OP_IASSIGN_BIT_AND = auto()  #
    # OP_IASSIGN_BIT_OR = auto()  #
    # OP_IASSIGN_BIT_XOR = auto()  #
    #
    # OP_IASSIGN_BIT_LSHIFT = auto()  #
    # OP_IASSIGN_BIT_RSHIFT = auto()  #

    # KEYWORD_IF = auto()
    # KEYWORD_ELSE = auto()
    # KEYWORD_FOR = auto()
    # KEYWORD_WHILE = auto()
    # KEYWORD_FUNCTION = auto()
    # KEYWORD_BREAK = auto()
    # KEYWORD_CONTINUE = auto()
    # KEYWORD_RETURN = auto()
    # KEYWORD_TRY = auto()
    # KEYWORD_CATCH = auto()
    # KEYWORD_FINALLY = auto()
    # KEYWORD_STRUCT = auto()
    #
    # # OOP
    # KEYWORD_CLASS = auto()
    # KEYWORD_THIS = auto()
    # KEYWORD_CONSTRUCTOR = auto()
    # KEYWORD_DESTRUCTOR = auto()
    #
    # KEYWORD_OPERATOR = auto()
    # KEYWORD_TYPE = auto()
    #
    # KEYWORD_FROM = auto()
    #
    # KEYWORD_PUBLIC = auto()
    # KEYWORD_PRIVATE = auto()
    # KEYWORD_PROTECTED = auto()
    #
    # KEYWORD_VIRTUAL = auto()
    # KEYWORD_OVERRIDE = auto()
    #
    # KEYWORD_STATIC = auto()



# KEYWORDS = {
#     'or': TokenType.OP_BOOL_OR,
#     'xor': TokenType.OP_BOOL_XOR,
#     'and': TokenType.OP_BOOL_AND,
#     'not': TokenType.OP_BOOL_NOT,
#     'in': TokenType.OP_CMP_IN,
#     'as': TokenType.OP_TYPECAST,
#     'ref': TokenType.OP_REF,
#     'deref': TokenType.OP_DEREF,
#     'new': TokenType.OP_ALLOC_NEW,
#     'delete': TokenType.OP_ALLOC_DEL,
#
#     'if': TokenType.KEYWORD_IF,
#     'else': TokenType.KEYWORD_ELSE,
#     'for': TokenType.KEYWORD_FOR,
#     'while': TokenType.KEYWORD_WHILE,
#     'function': TokenType.KEYWORD_FUNCTION,
#     'break': TokenType.KEYWORD_BREAK,
#     'continue': TokenType.KEYWORD_CONTINUE,
#     'return': TokenType.KEYWORD_RETURN,
#     'try': TokenType.KEYWORD_TRY,
#     'catch': TokenType.KEYWORD_CATCH,
#     'finally': TokenType.KEYWORD_FINALLY,
#     'struct': TokenType.KEYWORD_STRUCT,
#
#     # OOP
#     'class': TokenType.KEYWORD_CLASS,
#     'this': TokenType.KEYWORD_THIS,
#     'constructor': TokenType.KEYWORD_CONSTRUCTOR,
#     'destructor': TokenType.KEYWORD_DESTRUCTOR,
#
#     'operator': TokenType.KEYWORD_OPERATOR,
#     'type': TokenType.KEYWORD_TYPE,
#
#     'from': TokenType.KEYWORD_FROM,
#
#     'public': TokenType.KEYWORD_PUBLIC,
#     'private': TokenType.KEYWORD_PRIVATE,
#     'protected': TokenType.KEYWORD_PROTECTED,
#
#     'virtual': TokenType.KEYWORD_VIRTUAL,
#     'override': TokenType.KEYWORD_OVERRIDE,
#
#     'static': TokenType.KEYWORD_STATIC,
# }



class Keyword(StrEnum):
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
    CONSTRUCTOR = "constructor"
    DESTRUCTOR = "destructor"

    OPERATOR = "operator"
    TYPE = "type"  # considered as keyword for generic params

    FROM = "from"


class ClassModifierKeyword(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"

    VIRTUAL = "virtual"
    OVERRIDE = "override"

    STATIC = "static"

class Comparison(StrEnum):
    LESSER_OR_EQUAL = "<="
    GREATER_OR_EQUAL = ">="
    NOT_EQUAL = "!="
    GREATER = ">"
    LESSER = "<"
    EQUAL = "=="
    STRICT_EQUAL = "==="
    NOT_STRICT_EQUAL = "!=="

    MEMBERSHIP_OPERATOR = "in"


class Operator(StrEnum):
    # member access
    OBJECT_MEMBER_ACCESS = "."
    REFERENCE_MEMBER_ACCESS = "->"
    SCOPE_RESOLUTION = "::"

    # arithmetic
    PLUS = "+"
    MINUS = "-"
    POWER = "**"
    MULTIPLY = "*"
    MATMUL = "@"
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

    # syntax sugar
    IMPLY = "=>"
    ELLIPSIS = "..."

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


class OperatorMethods:
    @staticmethod
    def translate(op: str, n: int):
        binary_operator_names = {
            Operator.PLUS: "add",
            Operator.MINUS: "sub",
            Operator.MULTIPLY: "mul",
            Operator.DIVIDE: "div",
            Operator.MODULO: "mod",
            Operator.FLOOR_DIVIDE: "fdiv",
            Operator.POWER: "pow",

            Comparison.LESSER_OR_EQUAL: "lte",
            Comparison.GREATER_OR_EQUAL: "gte",
            Comparison.NOT_EQUAL: "ne",
            Comparison.GREATER: "gt",
            Comparison.LESSER: "lt",
            Comparison.EQUAL: "eq",

            Comparison.STRICT_EQUAL: 'eq!',
            Comparison.NOT_STRICT_EQUAL: 'ne!',

            Operator.BITWISE_XOR: "bxor",
            Operator.BITWISE_AND: "band",
            Operator.BITWISE_OR: "bor",
            Operator.BITWISE_RSHIFT: "brshift",
            Operator.BITWISE_LSHIFT: "blshift",

            Comparison.MEMBERSHIP_OPERATOR: "in",

            Operator.AND: "and",
            Operator.OR: "or",
            Operator.XOR: "xor",


            Operator.FULL_AND: "and!",
            Operator.FULL_OR: "or!",
            Operator.FULL_XOR: "xor",

            Operator.TYPE_CAST: "cast",
            Operator.NULL_COALESCE: "coalesce",

            Operator.OBJECT_MEMBER_ACCESS: "ACCESS",
            Operator.REFERENCE_MEMBER_ACCESS: "REFACCESS",
        }

        unary_operator_names = {
            Operator.PLUS: "idempotate",
            Operator.MINUS: "negate",

            Operator.NOT: "not",
            Operator.BITWISE_INVERSE: "binv",

            Operator.NEW_INSTANCE: "alloc",
            Operator.DELETE_INSTANCE: "free",

            Operator.REFERENCE: "addr",
            Operator.DEREFERENCE: "valof",
        }

        if n == 2:
            return binary_operator_names[op].upper()
        else:
            return unary_operator_names[op].upper()

    @staticmethod
    def overloadable(op: str):
        possible_overload_operators = [
            Operator.PLUS,
            Operator.MINUS,
            Operator.MULTIPLY,
            Operator.DIVIDE,
            Operator.MODULO,
            Operator.FLOOR_DIVIDE,
            Operator.POWER,

            Comparison.LESSER_OR_EQUAL,
            Comparison.GREATER_OR_EQUAL,
            Comparison.NOT_EQUAL,
            Comparison.GREATER,
            Comparison.LESSER,
            Comparison.EQUAL,

            Operator.BITWISE_XOR,
            Operator.BITWISE_AND,
            Operator.BITWISE_OR,
            Operator.BITWISE_RSHIFT,
            Operator.BITWISE_LSHIFT,
            Operator.BITWISE_INVERSE,

            Comparison.MEMBERSHIP_OPERATOR,
        ]
        return op in possible_overload_operators


class Assignment(StrEnum):
    VALUE_ASSIGNMENT = ":="
    REVERSE_VALUE_ASSIGNMENT = "=:"
    REFERENCE_ASSIGNMENT = "="

    COMPOUND_PLUS = "+="
    COMPOUND_MINUS = "-="
    COMPOUND_MULTIPLY = "*="
    COMPOUND_MATMUL = "@="
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

    COMPOUND_FULL_XOR = "^^="
    COMPOUND_FULL_OR = "||="
    COMPOUND_FULL_AND = "&&="

    COMPOUND_NULL_COALESCE = "?="
    ELLIPSIS = "..."

    @staticmethod
    def translate(op: str):
        if op == Assignment.VALUE_ASSIGNMENT:
            return 'VALCOPY'
        if op == Assignment.REFERENCE_ASSIGNMENT:
            return 'REFCOPY'

    @staticmethod
    def is_compound_assignment(op: str):
        return op not in (Assignment.VALUE_ASSIGNMENT, Assignment.REFERENCE_ASSIGNMENT)

    @staticmethod
    def decompose_compound(op: str):
        decomposition_map = {
            Assignment.COMPOUND_PLUS: Operator.PLUS,
            Assignment.COMPOUND_MINUS: Operator.MINUS,
            Assignment.COMPOUND_MULTIPLY: Operator.MULTIPLY,
            Assignment.COMPOUND_DIVIDE: Operator.DIVIDE,
            Assignment.COMPOUND_POWER: Operator.POWER,
            Assignment.COMPOUND_MODULO: Operator.MODULO,
            Assignment.COMPOUND_FLOOR_DIVIDE: Operator.FLOOR_DIVIDE,

            Assignment.COMPOUND_BITWISE_XOR: Operator.BITWISE_XOR,
            Assignment.COMPOUND_BITWISE_AND: Operator.BITWISE_AND,
            Assignment.COMPOUND_BITWISE_OR: Operator.BITWISE_OR,
            Assignment.COMPOUND_BITWISE_RSHIFT: Operator.BITWISE_RSHIFT,
            Assignment.COMPOUND_BITWISE_LSHIFT: Operator.BITWISE_LSHIFT,
        }

        return decomposition_map[op]

class TypeModifier(StrEnum):
    CONST = "const"
    NULLABLE = "nullable"
    REFERENCE = "reference"


class CompoundType(StrEnum):
    ARRAY = "array"
    KEYMAP = "keymap"

    @staticmethod
    def translate(s: str) -> str:
        dct = {
            CompoundType.ARRAY: "ARRAY",
            CompoundType.KEYMAP: "KEYMAP",
        }
        return dct[s]


class SimpleType(StrEnum):

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

    @staticmethod
    def translate(s: str) -> str:
        dct = {
            SimpleType.BOOLEAN: "BOOL",
            SimpleType.BYTE: "INT8",
            SimpleType.SHORT_INTEGER: "INT16",
            SimpleType.INTEGER: "INT32",
            SimpleType.LONG_INTEGER: "INT64",
            SimpleType.EXTENDED_INTEGER: "INTD",

            SimpleType.FLOAT: "FLOAT32",
            SimpleType.DOUBLE: "FLOAT64",

            SimpleType.COMPLEX: "COMPLEX128",

            SimpleType.CHAR: "CHAR",
            SimpleType.STRING: "STRING",
            SimpleType.BYTESTRING: "BYTESTRING",
            SimpleType.STREAM: "IOSTREAM",
        }
        return dct[s]

# COMPARISON_REGEX = join_unbounded_keywords_as_regex(Comparison.values())
# ASSIGNMENTS_REGEX = join_unbounded_keywords_as_regex(Assignment.values())
# OPERATORS_REGEX = join_partially_bounded_keywords_as_regex(Operator.values())
# OPERANDS_REGEX = join_partially_bounded_keywords_as_regex(Operands.values())

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

# BOOLEAN_REGEX = join_bounded_keywords_as_regex(('true', 'false'))
# NULL_REGEX = bounded('null')
# UNDEFINED_REGEX = bounded('undefined')

# TYPES REGEX
# SIMPLE_TYPES_REGEX = join_bounded_keywords_as_regex(SimpleType.values())
# COMPOUND_TYPES_REGEX = join_bounded_keywords_as_regex(CompoundType.values())
# TYPES_MODIFIER_REGEX = join_bounded_keywords_as_regex(TypeModifier.values())

# IDENTIFIER_REGEX = r"[a-zA-Z_][a-zA-Z0-9_]*"
# COMMENT_REGEX = r"#.*$"

KEYWORDS = {
    'or': (TokenType.OPERATOR, Operator.OR),
    'xor': (TokenType.OPERATOR, Operator.XOR),
    'and': (TokenType.OPERATOR, Operator.AND),
    'not': (TokenType.OPERATOR, Operator.NOT),
    'in': (TokenType.OPERATOR, Comparison.MEMBERSHIP_OPERATOR),
    'as': (TokenType.OPERATOR, Operator.TYPE_CAST),
    'ref': (TokenType.OPERATOR, Operator.REFERENCE),
    'deref': (TokenType.OPERATOR, Operator.DEREFERENCE),
    'new': (TokenType.OPERATOR, Operator.NEW_INSTANCE),
    'delete': (TokenType.OPERATOR, Operator.DELETE_INSTANCE),

    'if': (TokenType.KEYWORD, Keyword.IF),
    'else': (TokenType.KEYWORD, Keyword.ELSE),
    'for': (TokenType.KEYWORD, Keyword.FOR),
    'while': (TokenType.KEYWORD, Keyword.WHILE),
    'function': (TokenType.KEYWORD, Keyword.FUNCTION),
    'break': (TokenType.KEYWORD, Keyword.BREAK),
    'continue': (TokenType.KEYWORD, Keyword.CONTINUE),
    'return': (TokenType.KEYWORD, Keyword.RETURN),
    'try': (TokenType.KEYWORD, Keyword.TRY),
    'catch': (TokenType.KEYWORD, Keyword.CATCH),
    'finally': (TokenType.KEYWORD, Keyword.FINALLY),
    'struct': (TokenType.KEYWORD, Keyword.STRUCT),

    # OOP
    'class': (TokenType.KEYWORD, Keyword.CLASS),
    'this': (TokenType.KEYWORD, Keyword.THIS),
    'constructor': (TokenType.KEYWORD, Keyword.CONSTRUCTOR),
    'destructor': (TokenType.KEYWORD, Keyword.DESTRUCTOR),

    'operator': (TokenType.KEYWORD, Keyword.OPERATOR),
    'type': (TokenType.KEYWORD, Keyword.TYPE),

    'from': (TokenType.KEYWORD, Keyword.FROM),

    'public': (TokenType.CLASS_KEYWORD, ClassModifierKeyword.PUBLIC),
    'private': (TokenType.CLASS_KEYWORD, ClassModifierKeyword.PRIVATE),
    'protected': (TokenType.CLASS_KEYWORD, ClassModifierKeyword.PROTECTED),

    'virtual': (TokenType.CLASS_KEYWORD, ClassModifierKeyword.VIRTUAL),
    'override': (TokenType.CLASS_KEYWORD, ClassModifierKeyword.OVERRIDE),

    'static': (TokenType.CLASS_KEYWORD, ClassModifierKeyword.STATIC),

    'const': (TokenType.TYPE_MODIFIER, TypeModifier.CONST),
    'nullable': (TokenType.TYPE_MODIFIER, TypeModifier.NULLABLE),
    'reference': (TokenType.TYPE_MODIFIER, TypeModifier.REFERENCE),

    'array': (TokenType.COMPOUND_TYPE, CompoundType.ARRAY),
    'keymap': (TokenType.COMPOUND_TYPE, CompoundType.KEYMAP),

    "boolean": (TokenType.SIMPLE_TYPE, SimpleType.BOOLEAN),
    "byte": (TokenType.SIMPLE_TYPE, SimpleType.BYTE),
    "short integer": (TokenType.SIMPLE_TYPE, SimpleType.SHORT_INTEGER),
    "integer": (TokenType.SIMPLE_TYPE, SimpleType.INTEGER),
    "long integer": (TokenType.SIMPLE_TYPE, SimpleType.LONG_INTEGER),
    "extended integer": (TokenType.SIMPLE_TYPE, SimpleType.EXTENDED_INTEGER),

    "float": (TokenType.SIMPLE_TYPE, SimpleType.FLOAT),
    "double": (TokenType.SIMPLE_TYPE, SimpleType.DOUBLE),

    "complex": (TokenType.SIMPLE_TYPE, SimpleType.COMPLEX),

    "char": (TokenType.SIMPLE_TYPE, SimpleType.CHAR),
    "string": (TokenType.SIMPLE_TYPE, SimpleType.STRING),
    "bytestring": (TokenType.SIMPLE_TYPE, SimpleType.BYTESTRING),
    "stream": (TokenType.SIMPLE_TYPE, SimpleType.STREAM),

}