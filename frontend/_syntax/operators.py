from ..etc import CustomEnum


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

    @staticmethod
    def translate(op: str):
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

            Operator.STRICT_EQUAL: 'eq!',
            Operator.NOT_STRICT_EQUAL: 'ne!',

            Operator.BITWISE_XOR: "bxor",
            Operator.BITWISE_AND: "band",
            Operator.BITWISE_OR: "bor",
            Operator.BITWISE_RSHIFT: "brshift",
            Operator.BITWISE_LSHIFT: "blshift",
            Operator.BITWISE_INVERSE: "binv",

            Operator.MEMBERSHIP_OPERATOR: "lookup",
        }

        return OPERATOR_NAMES[op].upper()

    @staticmethod
    def overloadable(op: str):
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
        return op in POSSIBLE_OVERLOAD_OPERATORS



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
