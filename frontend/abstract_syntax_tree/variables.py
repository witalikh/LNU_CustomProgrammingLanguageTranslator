from typing import TextIO

from .ast_node import ASTNode
from .._syntax.operators import Assignment


class VariableDeclarationNode(ASTNode):

    def __init__(
        self,
        _type: ASTNode,
        name: str,
        operator: str | None,
        value: ASTNode | None,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.type = _type
        self.name = name
        self.operator = operator
        self.value = value

    def is_valid(self) -> bool:
        return (
            self.valid
            and self.type.is_valid()
            and self.value.is_valid() if self.value is not None else True
        )

    def translate(self, file: TextIO, **kwargs) -> None:
        file.write('SET')
        file.write(' ')
        self.type.translate(file, **kwargs)
        file.write(' ')
        file.write(self.name)
        if self.value is not None:
            file.write('\n')
            file.write(Assignment.translate(self.operator))
            file.write(' ')
            file.write('ID')
            file.write(' ')
            file.write(self.name)
            file.write(' ')
            self.value.translate(file, **kwargs)
