from ..etc import CustomEnum


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
