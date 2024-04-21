from abc import ABC
from .ast_node import ASTNode


class CalculationNode(ASTNode, ABC):
    pass


class LiteralNode(CalculationNode):

    def is_valid(self) -> bool:
        return self.valid

    def __print_tree__(self):
        formatted_name = self.__class__.__name__.replace("LiteralNode", "")
        if hasattr(self, "value"):
            return f"{formatted_name}({self.value})"
        return formatted_name


class StringLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class ByteLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class ByteStringLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class CharLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class BooleanLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class NullLiteralNode(LiteralNode):
    pass


class UndefinedLiteralNode(LiteralNode):
    pass


class ListLiteralNode(LiteralNode):
    def __init__(self, elements: list[ASTNode], line: int, position: int):
        super().__init__(line, position)
        self.elements = elements

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((e.is_valid() for e in self.elements))
        ))


class KeymapElementNode(LiteralNode):
    def __init__(
            self,
            left: ASTNode,
            right: ASTNode,
            line: int,
            position: int
    ):
        super().__init__(line, position)
        self.left = left
        self.right = right

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.left.is_valid(),
            self.right.is_valid()
        ))


class KeymapLiteralNode(LiteralNode):
    def __init__(self, elements: list[KeymapElementNode], line: int, position: int):
        super().__init__(line, position)
        self.elements = elements

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((e.is_valid() for e in self.elements))
        ))


class EmptyLiteralNode(LiteralNode):
    def __init__(self, line: int, position: int):
        super().__init__(line, position)
