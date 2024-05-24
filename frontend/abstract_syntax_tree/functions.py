from typing import TextIO
from .ast_node import ASTNode
from .ast_mixins import Usable
from .literals import CalculationNode
from .scope import ScopeNode
from .typing import TypeNode


class FunctionDefNode(ASTNode, Usable):
    def __init__(
        self,
        return_type: TypeNode,
        function_name: str,
        parameters: list["FunctionParameter"],
        function_body: ScopeNode,
        line: int,
        position: int
    ) -> None:
        super().__init__(line=line, position=position)
        self.return_type = return_type
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body

        # makes sense to operators overload
        self.external_to = None

        # Type checker meta info
        self.has_overloads = False
        self._usages: int = 0

    @property
    def parameters_signature(self) -> list[TypeNode]:
        return list(
            map(lambda p: p.type, self.parameters)
        )

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.return_type.is_valid() if self.return_type else True,
            all((p.is_valid() for p in self.parameters)),
            self.function_body.is_valid(),
            self.external_to.is_valid() if self.external_to else True
        ))

    def translate(self, file: TextIO) -> None:
        self.write_instruction(file, ['FUNCTION', ' ', self.function_name])
        for arg in self.parameters:
            arg.translate(file)
            file.write('\n')
        self.function_body.translate(file)
        self.write_instruction(file, ['ENDFUNCTION', ' ', self.function_name])


class FunctionParameter(ASTNode, Usable):
    def __init__(
        self,
        type_: TypeNode,
        parameter_name: str,
        line: int,
        position: int,
    ) -> None:
        super().__init__(line=line, position=position)
        self.type = type_
        self.name = parameter_name

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.type.is_valid(),
        ))

    def translate(self, file: TextIO) -> None:
        file.write('PARAM')
        file.write(' ')
        self.type.translate(file)
        file.write(' ')
        file.write(self.name)

class FunctionCallNode(CalculationNode):
    def __init__(
        self,
        identifier: ASTNode,
        arguments: list[ASTNode],
        line: int,
        position: int,
        is_constructor: bool = False,
    ) -> None:
        super().__init__(line=line, position=position)
        self.identifier = identifier
        self.arguments = arguments

        self.is_constructor = is_constructor

        # Type checking
        self.function = None

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((a.is_valid() for a in self.arguments))
        ))

    def translate(self, file: TextIO) -> None:
        if self.is_constructor:
            file.write('CONSTRUCT')
        else:
            file.write('CALL')

        file.write(' ')
        file.write(str(len(self.arguments) + 1))
        file.write(' ')
        self.identifier.translate(file)
        file.write(' ')

        for argument in self.arguments:
            argument.translate(file)
            file.write(' ')
        file.write('\n')
