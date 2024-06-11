from typing import Union, TextIO

from ..ast_node import ASTNode
from ..literals import CalculationNode
from ..identifiers import IdentifierNode
from ..functions import FunctionCallNode


class IndexNode(CalculationNode):
    def __init__(
        self,
        variable: Union[IdentifierNode, "IndexNode", FunctionCallNode],
        arguments: list[ASTNode],
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.variable = variable
        self.arguments = arguments

        self.is_overload = False
        self.overload_number = 0

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.variable.is_valid(),
            all((a.is_valid() for a in self.arguments))
        ))

    def translate(self, file: TextIO, **kwargs) -> None:
        if self.is_overload:
            file.write('CALL')

            file.write(' ')
            file.write(str(len(self.arguments) + 2))
            file.write(' ')
            file.write('ID')
            file.write(' ')
            if self.overload_number != 0:
                file.write(f"$operator_index$_{self.overload_number}")
            else:
                file.write("$operator_index")
        else:
            file.write('INDEX')
            file.write(' ')
            file.write(str(len(self.arguments) + 1))
        file.write(' ')
        self.variable.translate(file, **kwargs)
        for arg in self.arguments:
            file.write(' ')
            arg.translate(file, **kwargs)
