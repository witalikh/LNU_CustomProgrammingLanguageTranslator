from .abstract_syntax_tree import TemporaryIdentifierNode
from .ast_node import ASTNode
from enum import IntFlag


class TypeModifierFlag(IntFlag):
    NULLABLE = 1
    REFERENCE = 2
    CONSTANT = 4


class TypeNode(ASTNode):
    def __init__(self, type_name):
        self.type_name = type_name
        self._modifiers = 0

    def add_flag(self, flag):
        self._modifiers |= flag

    def remove_flag(self, flag):
        self._modifiers &= ~flag

    @property
    def modifiers(self):
        result = []
        if self._modifiers & TypeModifierFlag.CONSTANT:
            result.append("const")
        if self._modifiers & TypeModifierFlag.REFERENCE:
            result.append("reference")
        if self._modifiers & TypeModifierFlag.NULLABLE:
            result.append("nullable")
        return " ".join(result)

    def __tree_dict__(self):
        return {
            "type_name": self.type_name,
            "modifiers": self.modifiers
        }

class SimpleTypeNode(TypeNode):
    def __print_tree__(self):
        return f"SimpleType({self.type_name})"


class UserDefinedTypeNode(TypeNode):
    @staticmethod
    def from_temporary(temporary_identifier: "TemporaryIdentifierNode") -> "UserDefinedTypeNode":
        result = UserDefinedTypeNode(type_name=temporary_identifier.name)
        result._modifiers = temporary_identifier.modifiers
        return result

    def __print_tree__(self):
        return f"Class / struct identifier({self.type_name})"


class CompoundTypeNode(TypeNode):
    def __init__(self, type_name, args):
        super().__init__(type_name)
        self.args = args

    def __tree_dict__(self):
        return {
            "type_name": self.type_name,
            "args": self.args,
            "modifiers": self.modifiers,
        }