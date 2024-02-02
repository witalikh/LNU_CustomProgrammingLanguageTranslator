from enum import StrEnum


class TypeEnum(StrEnum):
    NULL = "null"
    UNDEFINED = "undefined"

    BOOLEAN = "boolean"

    BYTE = "byte"
    INTEGER = "integer"
    LONG_INTEGER = "long integer"
    FLOAT = "float"
    LONG_FLOAT = "long float"

    COMPLEX = "complex"
    STRING = "string"

    BYTESTRING = "bytestring"
    STREAM = "stream"

    ARRAY = "array"
    LIST = "list"
    KEYMAP = "keymap"
    SET = "set"

    CLASS = "class"
    GENERIC_CLASS = "generic"
