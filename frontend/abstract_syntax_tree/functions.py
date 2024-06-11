from typing import TextIO

from .identifiers import IdentifierNode
from .ast_node import ASTNode
from .ast_mixins import Usable
from .literals import CalculationNode
from .scope import ScopeNode
from .typing import TypeNode
# from .operators.membership import MemberOperatorNode


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
        self.overload_number = 0
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

    def translate(self, file: TextIO, **kwargs) -> None:
        function_name = self.function_name

        if self.has_overloads and self.overload_number != 0:
            function_name += f'$_{self.overload_number}'

        self.write_instruction(file, ['FUNCTION', ' ', function_name])
        self.write_instruction(file, ['PARAMS_COUNT', ' ', str(len(self.parameters))])
        for arg in self.parameters:
            arg.translate(file, **kwargs)
            file.write('\n')
        file.write('\n')
        self.function_body.translate(file, **kwargs)
        self.write_instruction(file, ['ENDFUNCTION', ' ', function_name])


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

    def translate(self, file: TextIO, **kwargs) -> None:
        file.write('PARAM')
        file.write(' ')
        self.type.translate(file, **kwargs)
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
        self.is_overload = False
        self.overload_number = 0

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((a.is_valid() for a in self.arguments))
        ))

    def translate(self, file: TextIO, **kwargs) -> None:
        if self.is_constructor:
            file.write('CONSTRUCT')
        else:
            file.write('CALL')



        if is_pure_func := isinstance(self.identifier, IdentifierNode):
            # TODO: constructor like CONSTRUCT CLASS
            name = ''.join([
                self.identifier.name,
                f"$_{self.overload_number}" if self.is_overload and self.overload_number != 0 else '',
            ])
            count = len(self.arguments) + 1
        elif is_static_func := isinstance(self.identifier, TypeNode):
            name = 'pass'
            count = len(self.arguments) + 1
        else:
            name = ''.join([
                self.identifier.associated_class.name,
                '$',
                self.identifier.right.name,
                f"$_{self.overload_number}" if self.is_overload and self.overload_number != 0 else '',
            ])
            count = len(self.arguments) + 2

        file.write(' ')
        file.write(str(count))
        file.write(' ')

        file.write(name)

        if not is_pure_func and not is_static_func:
            file.write(' ')
            self.identifier.left.translate(file, **kwargs)

        for argument in self.arguments:
            file.write(' ')
            argument.translate(file, **kwargs)
