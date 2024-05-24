from ..etc import CustomEnum


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


class ClassModifierKeyword(CustomEnum):
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"

    VIRTUAL = "virtual"
    OVERRIDE = "override"

    STATIC = "static"
