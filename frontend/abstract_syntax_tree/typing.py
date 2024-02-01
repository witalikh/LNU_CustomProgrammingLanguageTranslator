from typing import List, Union

from .identifiers import IdentifierNode
from .ast_node import ASTNode
from enum import IntFlag


class TypeCategory(IntFlag):
    PRIMITIVE = 1
    COLLECTION = 2
    CLASS = 3
    GENERIC_CLASS = 4


class TypeModifierFlag(IntFlag):
    NULLABLE = 1
    REFERENCE = 2
    CONSTANT = 4


class TypeLiteral(ASTNode):
    def __init__(self, name: str, line: int, location: int):
        super().__init__(line, location)
        self.name = name

    def __print_tree__(self):
        return f"TypeLiteral({self.name})"


class TypeNode(ASTNode):
    def __init__(
        self,
        category: TypeCategory,
        type_name: TypeLiteral | IdentifierNode,
        args: List[Union["TypeNode", ASTNode]] | None,
        line: int,
        position: int,
    ):
        super().__init__(line, position)
        self.category = category
        self.type_name = type_name
        self.arguments = args
        self._modifiers = 0

    def __eq__(self, other):
        return isinstance(other, TypeNode) and self.type_name == other.type_name and self.modifiers == other.modifiers

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
        if self.category not in (TypeCategory.COLLECTION, TypeCategory.GENERIC_CLASS):
            return {
                "type_name": self.type_name,
                "modifiers": self.modifiers
            }
        else:
            return {
                "type_name": self.type_name,
                "arguments": self.arguments,
                "modifiers": self.modifiers,
            }
