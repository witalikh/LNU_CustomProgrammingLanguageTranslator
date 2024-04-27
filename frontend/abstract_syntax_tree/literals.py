from abc import ABC
from typing import TextIO
from .ast_node import ASTNode


class CalculationNode(ASTNode, ABC):
    pass


class LiteralNode(CalculationNode, ABC):

    def is_valid(self) -> bool:
        return self.valid

    def __print_tree__(self) -> str:
        formatted_name = self.__class__.__name__.replace("LiteralNode", "")
        if hasattr(self, "value"):
            return f"{formatted_name}({self.value})"
        return formatted_name


class StringLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int) -> None:
        super().__init__(line=line, position=position)
        self.value = value

    def translate(self, file: TextIO) -> None:
        file.write(self.value)


class ByteLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int) -> None:
        super().__init__(line=line, position=position)
        self.value = value

    def translate(self, file: TextIO) -> None:
        file.write(self.value)


class ByteStringLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int) -> None:
        super().__init__(line=line, position=position)
        self.value = value

    def translate(self, file: TextIO) -> None:
        file.write(self.value)


class CharLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int) -> None:
        super().__init__(line=line, position=position)
        self.value = value

    def translate(self, file: TextIO) -> None:
        file.write(self.value)


class BooleanLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value

    def translate(self, file: TextIO) -> None:
        file.write(self.value)


class NullLiteralNode(LiteralNode):
    def translate(self, file: TextIO) -> None:
        file.write('NULL')


class UndefinedLiteralNode(LiteralNode):
    def translate(self, file: TextIO) -> None:
        file.write('UNDEFINED')


class ListLiteralNode(LiteralNode):
    def __init__(self, elements: list[ASTNode], line: int, position: int):
        super().__init__(line, position)
        self.elements = elements

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((e.is_valid() for e in self.elements))
        ))

    def translate(self, file: TextIO) -> None:
        self.write_instruction(['ARRAY', ' ', len(self.elements)])
        for value in self.elements:
            value.translate(file)
            file.write(' ')
        file.write('\n')


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

    def translate(self, file: TextIO) -> None:
        # TODO: normal hash set
        self.left.translate(file)
        file.write(' : ')
        self.right.translate(file)


class KeymapLiteralNode(LiteralNode):
    def __init__(self, elements: list[KeymapElementNode], line: int, position: int):
        super().__init__(line, position)
        self.elements = elements

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((e.is_valid() for e in self.elements))
        ))

    def translate(self, file: TextIO) -> None:
        self.write_instruction(['KEYMAP', ' ', len(self.elements)])
        for value in self.elements:
            value.translate(file)
            file.write('\n')


class EmptyLiteralNode(LiteralNode):
    def __init__(self, line: int, position: int):
        super().__init__(line, position)

    def translate(self, file: TextIO) -> None:
        raise NotImplementedError
