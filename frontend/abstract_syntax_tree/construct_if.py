from typing import TextIO, Union

from .ast_node import ASTNode
from .scope import ScopeNode


class IfElseNode(ASTNode):

    INSTANCES = 0

    def __init__(
        self,
        condition: ASTNode,
        if_scope: ScopeNode,
        else_scope: Union[ScopeNode, "IfElseNode", None],
        line: int,
        position: int,
    ) -> None:
        super().__init__(line=line, position=position)
        self.condition = condition
        self.if_scope = if_scope
        self.else_scope = else_scope

        self._curr_instance = self.INSTANCES
        self.INSTANCES += 1

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.condition.is_valid(),
            self.if_scope.is_valid(),
            self.else_scope.is_valid() if self.else_scope else True
        ))

    def translate(self, file: TextIO) -> None:
        if_label = 'IF' + str(self._curr_instance)
        else_label = 'ELSE' + str(self._curr_instance)
        endif_label = 'ENDIF' + str(self._curr_instance)

        file.write('COND')
        file.write(' ')
        file.write(if_label)
        file.write(' ')
        if self.else_scope:
            file.write(else_label)
        else:
            file.write(endif_label)
        file.write(' ')
        self.condition.translate(file)
        file.write('\n')

        self.write_instruction(file, ['LABEL', ' ', if_label])
        self.if_scope.translate(file)
        if self.else_scope:
            self.write_instruction(file, ['JUMP', ' ', endif_label])
            self.write_instruction(file, ['LABEL', ' ', else_label])
            self.else_scope.translate(file)
        self.write_instruction(file, ['LABEL', ' ', endif_label])

