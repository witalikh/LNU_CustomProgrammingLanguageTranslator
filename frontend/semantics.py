from enum import StrEnum


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
