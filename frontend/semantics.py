from enum import StrEnum
from .syntax import Operator, Assignment


class TypeEnum(StrEnum):
    NULL = "null"
    UNDEFINED = "undefined"

    BOOLEAN = "boolean"

    BYTE = "byte"
    SHORT_INTEGER = "short integer"
    INTEGER = "integer"
    LONG_INTEGER = "long integer"
    EXTENDED_INTEGER = "extended integer"

    FLOAT = "float"
    DOUBLE = "double"

    COMPLEX = "complex"

    CHAR = "char"
    STRING = "string"

    BYTESTRING = "bytestring"
    STREAM = "stream"

    ARRAY = "array"
    LIST = "list"
    KEYMAP = "keymap"
    SET = "set"

    CLASS = "class"
    GENERIC_CLASS = "generic"


POSSIBLE_OVERLOAD_OPERATORS = [
    Operator.PLUS,
    Operator.MINUS,
    Operator.MULTIPLY,
    Operator.DIVIDE,
    Operator.MODULO,
    Operator.FLOOR_DIVIDE,
    Operator.POWER,

    Operator.LESSER_OR_EQUAL,
    Operator.GREATER_OR_EQUAL,
    Operator.NOT_EQUAL,
    Operator.GREATER,
    Operator.LESSER,
    Operator.EQUAL,

    Operator.BITWISE_XOR,
    Operator.BITWISE_AND,
    Operator.BITWISE_OR,
    Operator.BITWISE_RSHIFT,
    Operator.BITWISE_LSHIFT,
    Operator.BITWISE_INVERSE,

    Operator.MEMBERSHIP_OPERATOR,
]


OPERATOR_NAMES = {
    Operator.PLUS: "plus",
    Operator.MINUS: "minus",
    Operator.MULTIPLY: "mult",
    Operator.DIVIDE: "div",
    Operator.MODULO: "mod",
    Operator.FLOOR_DIVIDE: "fdiv",
    Operator.POWER: "pow",

    Operator.LESSER_OR_EQUAL: "lte",
    Operator.GREATER_OR_EQUAL: "gte",
    Operator.NOT_EQUAL: "ne",
    Operator.GREATER: "gt",
    Operator.LESSER: "lt",
    Operator.EQUAL: "eq",

    Operator.BITWISE_XOR: "bxor",
    Operator.BITWISE_AND: "band",
    Operator.BITWISE_OR: "bor",
    Operator.BITWISE_RSHIFT: "brshift",
    Operator.BITWISE_LSHIFT: "blshift",
    Operator.BITWISE_INVERSE: "binv",

    Operator.MEMBERSHIP_OPERATOR: "lookup",
}