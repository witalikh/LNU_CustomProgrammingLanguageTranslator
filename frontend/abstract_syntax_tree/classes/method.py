from ..ast_node import ASTNode
from ..typing import TypeNode
from ..functions import FunctionParameter
from ..scope import ScopeNode
from .common import AccessTypeMixin


class ClassMethodDeclarationNode(ASTNode, AccessTypeMixin):
    def __init__(
        self,
        return_type: TypeNode,
        function_name: str,
        parameters: list["FunctionParameter"],
        function_body: ScopeNode,
        access_type: str,
        static: bool,
        virtual: bool,
        overload: bool,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.return_type = return_type
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body

        self._access_type = access_type
        self._static = static
        self._virtual = virtual
        self._overload = overload

        # Type checker
        self._usages = 0

    @property
    def is_static(self) -> bool:
        return self._static

    @is_static.setter
    def is_static(self, value: bool):
        self._static = value

    @property
    def is_virtual(self) -> bool:
        return self._virtual

    @is_virtual.setter
    def is_virtual(self, value: bool):
        self._static = value

    @property
    def is_overload(self) -> bool:
        return self._overload

    @is_overload.setter
    def is_overload(self, value: bool):
        self._overload = value

    @property
    def parameters_signature(self) -> list[TypeNode]:
        return list(
            map(lambda p: p.type_node, self.parameters)
        )

    @property
    def usages(self):
        return self._usages

    def is_validated(self) -> bool:
        return all((
            self.valid is not None,
            self.return_type.is_validated() if self.return_type else True,
            all((x.is_validated() for x in self.parameters)),
            self.function_body.is_validated(),
        ))

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.return_type.is_valid() if self.return_type else True,
            all((x.is_valid() for x in self.parameters)),
            self.function_body.is_valid(),
        ))

    def use(self):
        self._usages += 1
