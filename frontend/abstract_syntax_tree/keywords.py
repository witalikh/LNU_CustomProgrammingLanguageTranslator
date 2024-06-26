from abc import ABC
from typing import TextIO

from .._syntax.operators import OperatorMethods, Assignment, Operator
from .ast_node import ASTNode


class KeywordNode(ASTNode, ABC):
    def is_valid(self) -> bool:
        return self.valid


class BreakNode(KeywordNode):
    def __init__(self, line, position, loop=None, error=None):
        super().__init__(line, position)
        self.loop_instance = loop
        self.thrown_error = error

    def translate(self, file: TextIO, **kwargs) -> None:
        if self.loop_instance is not None:
            endwhile_label = 'ENDWHILE' + str(self.loop_instance)
            self.write_instruction(file, ['JUMP', ' ', endwhile_label])
        elif self.thrown_error is not None:
            file.write(Assignment.translate(Assignment.VALUE_ASSIGNMENT))
            file.write(' ')
            file.write('$ERROR')
            file.write(' ')
            file.write(OperatorMethods.translate(Operator.BITWISE_OR, 2))
            file.write(' ')
            file.write('$ERROR')
            file.write(' ')
            self.thrown_error.translate(file)
        else:
            raise NotImplementedError


class ThisNode(KeywordNode):
    def translate(self, file: TextIO, **kwargs) -> None:
        file.write('THIS')


class ContinueNode(KeywordNode):
    def __init__(self, line, position, loop=None, error=None):
        super().__init__(line, position)
        self.loop_instance = loop
        self.catched_error = error

    def translate(self, file: TextIO, **kwargs) -> None:
        if self.loop_instance is not None:
            while_label = 'WHILE' + str(self.loop_instance)
            self.write_instruction(file, ['JUMP', ' ', while_label])
        elif self.catched_error is not None:
            file.write(Assignment.translate(Assignment.VALUE_ASSIGNMENT))
            file.write(' ')
            file.write('$ERROR')
            file.write(' ')
            file.write(OperatorMethods.translate(Operator.BITWISE_XOR, 2))
            file.write(' ')
            file.write('$ERROR')
            file.write(' ')
            file.write(OperatorMethods.translate(Operator.BITWISE_AND, 2))
            file.write(' ')
            file.write('$ERROR')
            file.write(' ')
            self.catched_error.translate(file)
        else:
            raise NotImplementedError


class ReturnNode(KeywordNode):
    def __init__(self, value: ASTNode, line: int, position: int) -> None:
        super().__init__(line=line, position=position)
        self.value = value

    def translate(self, file: TextIO, **kwargs) -> None:
        file.write('RETURN')
        file.write(' ')
        if self.value is not None:
            self.value.translate(file, **kwargs)
        else:
            file.write('NOTHING')
