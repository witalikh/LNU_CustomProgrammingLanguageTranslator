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
