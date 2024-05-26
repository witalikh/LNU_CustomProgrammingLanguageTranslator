from typing import TextIO
from .ast_node import ASTNode
from .variables import VariableDeclarationNode


class ScopeNode(ASTNode):
    def __init__(
        self,
        statements: list[ASTNode],
        local_variables: list[VariableDeclarationNode],
        line: int,
        position: int,
    ) -> None:
        super().__init__(line, position)
        self.statements = statements
        self.local_variables = local_variables or []

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((s.is_valid() for s in self.statements)),
            all((v.is_valid() for v in self.local_variables))
        ))

    def translate(self, file: TextIO, **kwargs) -> None:
        for statement in self.statements:
            statement.translate(file, **kwargs)
            file.write('\n')

        for local_variable in self.local_variables:
            self.write_instruction(file, ['UNSET', ' ', local_variable.name])
