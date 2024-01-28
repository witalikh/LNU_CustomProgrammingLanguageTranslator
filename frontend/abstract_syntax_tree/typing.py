from .identifiers import IdentifierNode
from .ast_node import ASTNode
from enum import IntFlag


class TypeModifierFlag(IntFlag):
    NULLABLE = 1
    REFERENCE = 2
    CONSTANT = 4


class TypeNode(ASTNode):
    def __init__(self, type_name: str | ASTNode, line: int, position: int):
        super().__init__(line, position)
        self.type_name = type_name
        self._modifiers = 0

    def add_flag(self, flag: TypeModifierFlag):
        self._modifiers |= flag

    def remove_flag(self, flag: TypeModifierFlag):
        self._modifiers &= ~flag

    @property
    def modifiers(self) -> str:
        result = []
        if self._modifiers & TypeModifierFlag.CONSTANT:
            result.append("const")
        if self._modifiers & TypeModifierFlag.REFERENCE:
            result.append("reference")
        if self._modifiers & TypeModifierFlag.NULLABLE:
            result.append("nullable")
        return " ".join(result)

    @property
    def is_constant(self):
        return self._modifiers & TypeModifierFlag.CONSTANT

    @property
    def is_reference(self):
        return self._modifiers & TypeModifierFlag.REFERENCE

    @property
    def is_nullable(self):
        return self._modifiers & TypeModifierFlag.NULLABLE

    def __tree_dict__(self):
        return {
            "type_name": self.type_name,
            "modifiers": self.modifiers
        }


class SimpleTypeNode(TypeNode):
    def __print_tree__(self):
        return f"SimpleType({self.type_name})"


class UserDefinedTypeNode(TypeNode):
    def __print_tree__(self):
        return f"Class / struct identifier({self.type_name})"


class CompoundTypeNode(TypeNode):
    def __init__(self, type_name: str, args: list[ASTNode], line: int, position: int):
        super().__init__(type_name, line, position)
        self.args = args

    def __tree_dict__(self):
        return {
            "type_name": self.type_name,
            "args": self.args,
            "modifiers": self.modifiers,
        }


class GenericClassTypeNode(TypeNode):
    def __init__(self, type_name: UserDefinedTypeNode, generic_arguments: list[TypeNode], line: int, position: int):
        super().__init__(type_name, line, position)
        self.generic_arguments = generic_arguments

    def __tree_dict__(self):
        return {
            "type_name": self.type_name,
            "generic_arguments": self.generic_arguments,
            "modifiers": self.modifiers,
        }
