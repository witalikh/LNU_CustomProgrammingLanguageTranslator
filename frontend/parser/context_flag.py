from enum import IntFlag


class ContextFlag(IntFlag):
    """
    Class indicating scope context.
    Useful when parsing keywords or statements that are exclusive to some kind of scope.
    """
    GLOBAL = 0b0
    LOCAL = 0b1
    CLASS = 0b11
    FUNCTION = 0b101
    LOOP = 0b1001

    @staticmethod
    def match(current_context: "ContextFlag", flag: "ContextFlag") -> bool:
        """
        Check if the context has the given flag.
        E.g. if the keyword should be exclusively in the loop, but the loop itself can be in the function or method
        :param current_context: the context to check
        :param flag: the flag that should be contained in the context
        :return: boolean indicating if the flag is contained in the current context
        """
        if flag == ContextFlag.GLOBAL:
            return current_context == ContextFlag.GLOBAL
        else:
            return (current_context & flag) == flag

    @staticmethod
    def strict_match(current_context: "ContextFlag", flag: "ContextFlag") -> bool:
        """
        Check if the current context is strictly equal the given flag.
        E.g. if keyword should be in class scope, but not inside method
        :param current_context: the context to check
        :param flag: the flag the context should equal
        :return: boolean indicating whether context and flag are equal
        """
        return current_context == flag

    @staticmethod
    def add(current_context: "ContextFlag", flag: "ContextFlag") -> "ContextFlag":
        """
        Add the given flag to the scope context
        :param current_context: current scope context
        :param flag: flag to add
        :return: modified scope context
        """
        return current_context | flag
