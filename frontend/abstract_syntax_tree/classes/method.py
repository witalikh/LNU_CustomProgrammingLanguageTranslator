from ..ast_node import ASTNode
from ..ast_mixins import Usable
from ..typing import TypeNode, TextIO
from ..functions import FunctionParameter
from ..scope import ScopeNode
from .common import AccessTypeMixin


class ClassMethodDeclarationNode(ASTNode, AccessTypeMixin, Usable):
    def __init__(
        self,
        return_type: TypeNode,
        function_name: str,
        parameters: list["FunctionParameter"],
        function_body: ScopeNode,
        is_constructor: bool,
        is_destructor: bool,
        access_type: str,
        static: bool,
        virtual: bool,
        overload: bool,
        line: int,
        position: int
    ) -> None:
        super().__init__(line=line, position=position)
        self.return_type = return_type
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body

        self._access_type = access_type
        self.is_static = static
        self.is_virtual = virtual
        self.is_overload = overload

        self.is_constructor = is_constructor
        self.is_destructor = is_destructor

        # Type checker
        self.overload_number = 0
        self.has_overloads = False
        self._usages = 0

        # META INFO:
        self.translatable = False

    @property
    def parameters_signature(self) -> list[TypeNode]:
        return list(
            map(lambda p: p.type, self.parameters)
        )

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.return_type.is_valid() if self.return_type else True,
            all((x.is_valid() for x in self.parameters)),
            self.function_body.is_valid(),
        ))

    def translate(self, file: TextIO, **kwargs) -> None:
        # # TODO: normal constructors
        # self.write_instruction(file, ['METHOD', ' ', self.function_name])
        # for arg in self.parameters:
        #     arg.translate(file, **kwargs)
        #     file.write('\n')
        # self.function_body.translate(file, **kwargs)
        # self.write_instruction(file, ['ENDMETHOD', ' ', self.function_name])

        class_name = kwargs.pop("class_name")
        function_name = class_name + '$' + self.function_name

        if self.has_overloads and self.overload_number != 0:
            function_name += f'$_{self.overload_number}'

        self.write_instruction(file, ['METHOD', ' ', function_name])
        self.write_instruction(file, ['PARAMS_COUNT', ' ', str(len(self.parameters) + 1)])

        file.write('PARAM')
        file.write(' ')
        file.write('CLASSID')
        file.write(' ')
        file.write(class_name)
        file.write(' ')
        file.write('this')

        for arg in self.parameters:
            arg.translate(file, **kwargs)
            file.write('\n')
        file.write('\n')
        self.function_body.translate(file, **kwargs)
        self.write_instruction(file, ['ENDMETHOD', ' ', function_name])
