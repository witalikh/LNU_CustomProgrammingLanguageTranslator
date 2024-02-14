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
        _literal: bool = False,
        _const: bool = False,
        _reference: bool = False,
        _nullable: bool = False
    ):
        super().__init__(line, position)
        self.category = category
        self.type = type_node
        self.arguments = args
        self._modifiers = 0

        self._literal = _literal
        if _const:
            self._add_flag(TypeModifierFlag.CONSTANT)
        if _reference:
            self._add_flag(TypeModifierFlag.REFERENCE)
        if _nullable:
            self._add_flag(TypeModifierFlag.NULLABLE)

        # Type-check specific fields
        self.represents_generic_param = False if self.category != TypeCategory.CLASS else None
        self._class = None

    def __eq__(self, other):
        return all((
            isinstance(other, TypeNode),
            other.category == self.category,
            self.type == other.type,
            self.modifiers == other.modifiers
        ))

    def _add_flag(self, flag: TypeModifierFlag):
        if self._modifiers & flag:
            raise AssertionError(f"Flag {flag} already present")
        self._modifiers |= flag

    def _remove_flag(self, flag: TypeModifierFlag):
        if not (self._modifiers & flag):
            raise AssertionError(f"Flag {flag} already absent")
        self._modifiers &= ~flag

    @property
    def name(self) -> str:
        return self.type.name

    @property
    def is_literal(self) -> bool:
        return self._literal

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

    def set_constant(self):
        self._add_flag(TypeModifierFlag.CONSTANT)

    def unset_constant(self):
        self._remove_flag(TypeModifierFlag.CONSTANT)

    @property
    def is_reference(self):
        return self._modifiers & TypeModifierFlag.REFERENCE

    def set_reference(self):
        self._add_flag(TypeModifierFlag.REFERENCE)

    def unset_reference(self):
        self._remove_flag(TypeModifierFlag.REFERENCE)

    @property
    def is_nullable(self):
        return self._modifiers & TypeModifierFlag.NULLABLE

    def set_nullable(self):
        self._add_flag(TypeModifierFlag.NULLABLE)

    def unset_nullable(self):
        self._remove_flag(TypeModifierFlag.NULLABLE)

    @property
    def class_node(self):
        if self.category == TypeCategory.PRIMITIVE or TypeCategory.COLLECTION:
            raise AttributeError(f"Type {self.category} cannot have class instance")
        elif self._class is None:
            raise AttributeError(f"Uninstantiated class node here")
        else:
            return self._class

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

    # noinspection PyUnresolvedReferences
    def set_class(self, cls: "ClassDefinitionNode"):
        if self.category not in (TypeCategory.CLASS, TypeCategory.GENERIC_CLASS):
            raise ValueError("Cannot assign class node to this")
        self._class = cls

    def shallow_copy(self) -> "TypeNode":
        copy = TypeNode(
            self.category,
            self.type,
            self.arguments,
            self.line,
            self.position,
        )

        copy._modifiers = self._modifiers

        copy._literal = self._literal
        copy.represents_generic_param = self.represents_generic_param
        copy._class = self._class

        return copy
