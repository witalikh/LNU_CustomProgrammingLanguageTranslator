from typing import Union, TextIO

from frontend._syntax.operators import OperatorMethods
from ..literals import CalculationNode
from .indexation import IndexNode, IdentifierNode
from ..functions import FunctionCallNode


class MemberOperatorNode(CalculationNode):
    """
    Class.member()
    ref class->member()
    """

    def __init__(
        self,
        class_object: Union[IdentifierNode, "IndexNode", FunctionCallNode],
        operator: str,
        member: IdentifierNode,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.left = class_object
        self.operator = operator
        self.right = member

        from frontend.abstract_syntax_tree import TypeNode
        self.associated_class: TypeNode | None = None

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.associated_class is not None,
            self.left.is_valid(),
            self.right.is_valid()
        ))

    def translate(self, file: TextIO, **kwargs) -> None:
        file.write(OperatorMethods.translate(self.operator, 2))
        file.write(' ')
        self.left.translate(file, **kwargs)
        file.write(' ')
        self.right.translate(file, **kwargs)

