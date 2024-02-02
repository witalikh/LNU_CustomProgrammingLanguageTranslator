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

    def __eq__(self, other: Union['TypeLiteral', str]) -> bool:
        if isinstance(other, TypeLiteral):
            return self.name == other.name
        return self.name == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __print_tree__(self):
        return f"TypeLiteral({self.name})"


class TypeNode(ASTNode):
    def __init__(
        self,
        category: TypeCategory,
        type_node: TypeLiteral | IdentifierNode,
        args: List[Union["TypeNode", ASTNode]] | None,
        line: int,
        position: int,
    ):
        super().__init__(line, position)
        self.category = category
        self.type = type_node
        self.arguments = args
        self._modifiers = 0

    def __eq__(self, other):
        return all((
            isinstance(other, TypeNode),
            other.category == self.category,
            self.type == other.type,
            self.modifiers == other.modifiers
        ))

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
                "type": self.type,
                "modifiers": self.modifiers
            }
        else:
            return {
                "type": self.type,
                "arguments": self.arguments,
                "modifiers": self.modifiers,
            }
