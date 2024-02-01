from ..abstract_syntax_tree import *

from .shared import error_logger, class_definitions, function_definitions
from ..abstract_syntax_tree.unary_node import ReferenceOperatorNode

from enum import StrEnum

class TypeEnum(StrEnum):
    NULL = "null"
    UNDEFINED = "undefined"

    BOOLEAN = "boolean"
    INTEGER = "integer"
    LONG_INTEGER = "long integer"
    FLOAT = "float"
    LONG_FLOAT = "long float"

    BYTE = "byte"

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


def match_types(
    current_type: TypeNode,
    target_type: TypeNode,
):
    # absolute equal
    if current_type == target_type:
        return True

    if not current_type.is_constant and target_type.is_constant:
        return False

    # cannot assign reference into non-reference and vise versa
    if current_type.is_reference != target_type.is_reference:
        return False

    # if null, check if nullable
    if current_type.type == TypeEnum.NULL:
        return target_type.is_nullable
