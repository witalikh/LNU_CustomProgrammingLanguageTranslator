from syntax import Operator
from enum import IntEnum, auto

# proxy for imports
from abstract_syntax_tree.typing import TypeModifierFlag


class Property(IntEnum):
    LOGICAL = auto()
    NUMERIC = auto()
    PRESERVING_INTEGERS = auto()  # if two operands are integers, the result is also integer


OPERATOR_PROPERTIES = {
    Operator.PLUS: {
        Property.NUMERIC,
        Property.PRESERVING_INTEGERS,
    },
    Operator.MINUS: {
        Property.NUMERIC,
        Property.PRESERVING_INTEGERS,
    },
    Operator.POWER: {
        Property.NUMERIC,
        Property.PRESERVING_INTEGERS,
    },
    Operator.MULTIPLY: {
        Property.NUMERIC,
        Property.PRESERVING_INTEGERS,
    },
    Operator.FLOOR_DIVIDE: {
        Property.NUMERIC,
        Property.PRESERVING_INTEGERS,
    },
    Operator.DIVIDE: {
        Property.NUMERIC,

    },
    Operator.MODULO: {
        Property.NUMERIC,
        Property.PRESERVING_INTEGERS,
    },

    # logical (short-circuit)
    Operator.AND: {},
    Operator.OR: {},
    Operator.XOR: {},
    Operator.NOT: {},

    # logical (full check)
    Operator.FULL_AND: {},
    Operator.FULL_OR: {},
    Operator.FULL_XOR: {},

    # bitwise
    Operator.BITWISE_XOR: {},
    Operator.BITWISE_AND: {},
    Operator.BITWISE_OR: {},
    Operator.BITWISE_RSHIFT: {},
    Operator.BITWISE_LSHIFT: {},
    Operator.BITWISE_INVERSE: {},

    # comparison
    Operator.LESSER_OR_EQUAL: {},
    Operator.GREATER_OR_EQUAL: {},
    Operator.NOT_EQUAL: {},
    Operator.GREATER: {},
    Operator.LESSER: {},
    Operator.EQUAL: {},
    Operator.STRICT_EQUAL: {},
    Operator.NOT_STRICT_EQUAL: {},

    # member access
    Operator.OBJECT_MEMBER_ACCESS: {},
    Operator.REFERENCE_MEMBER_ACCESS: {},
    Operator.SCOPE_RESOLUTION: {},

    # syntax sugar
    Operator.FUNCTIONAL: {},

    # literals
    Operator.KEYMAP_LITERAL: {},
    Operator.DEDUCTION: {},
    Operator.TERMINATION: {},

    # unary
    Operator.INTERPOLATION: {},

    # pointers
    Operator.REFERENCE: {},
    Operator.DEREFERENCE: {},

    # type casting
    Operator.TYPE_CAST: {},
    Operator.NULL_COALESCE: {},
    Operator.NEW_INSTANCE: {},
    Operator.DELETE_INSTANCE: {},

    Operator.MEMBERSHIP_OPERATOR: {},
}