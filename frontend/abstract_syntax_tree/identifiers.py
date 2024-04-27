from typing import TextIO

from .ast_node import ASTNode


class IdentifierNode(ASTNode):
    def __init__(self, name: str, line: int, position: int) -> None:
        super().__init__(line=line, position=position)
        self.name = name

    def is_valid(self) -> bool:
        return self.valid

    def __print_tree__(self) -> str:
        return f"Identifier({self.name})"

    def translate(self, file: TextIO) -> None:
        file.write('ID')
        file.write(' ')
        file.write(self.name)
