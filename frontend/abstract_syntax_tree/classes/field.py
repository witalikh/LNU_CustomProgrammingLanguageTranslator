from ..ast_node import ASTNode
from ..ast_mixins import Usable
from ..typing import TypeNode
from .common import AccessTypeMixin


class ClassFieldDeclarationNode(ASTNode, AccessTypeMixin, Usable):
    def __init__(
        self,
        _type: TypeNode,
        name: str,
        operator: str | None,
        value: ASTNode | None,
        access_type: str,
        static: bool,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.type = _type
        self.name = name
        self.operator = operator
        self.value = value

        self._access_type = access_type
        self.is_static = static

        # Type checking
        self._usages = 0

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.type.is_valid(),
            self.value.is_valid() if self.value else True
        ))
