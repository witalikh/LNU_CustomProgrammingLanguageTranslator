from .ast_node import ASTNode
from .scope import ScopeNode
from typing import TextIO


class WhileNode(ASTNode):
    INSTANCES = 0

    def __init__(
        self,
        condition: ASTNode,
        while_scope: ScopeNode,
        line: int,
        position: int
    ) -> None:
        super().__init__(line=line, position=position)
        self.condition = condition
        self.while_scope = while_scope

        self._curr_instance = WhileNode.INSTANCES
        WhileNode.INSTANCES += 1

        # self.all_paths_return = None

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.condition.is_valid(),
            self.while_scope.is_valid(),
        ))

    def translate(self, file: TextIO, **kwargs) -> None:
        while_label = 'WHILE' + str(self._curr_instance)
        endwhile_label = 'ENDWHILE' + str(self._curr_instance)

        file.write('COND')
        file.write(' ')
        file.write(while_label)
        file.write(' ')
        file.write(endwhile_label)
        file.write(' ')
        self.condition.translate(file, **kwargs)
        file.write('\n')

        self.write_instruction(file, ['LABEL', ' ', while_label])
        self.while_scope.translate(file, **kwargs)

        file.write('COND')
        file.write(' ')
        file.write(while_label)
        file.write(' ')
        file.write(endwhile_label)
        file.write(' ')
        self.condition.translate(file, **kwargs)
        file.write('\n')

        self.write_instruction(file, ['LABEL', ' ', endwhile_label])
