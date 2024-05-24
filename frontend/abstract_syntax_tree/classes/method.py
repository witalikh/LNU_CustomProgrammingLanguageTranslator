from ..ast_node import ASTNode
from ..ast_mixins import Usable
from ..typing import TypeNode
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

        # Type checker
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
