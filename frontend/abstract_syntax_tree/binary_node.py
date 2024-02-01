from .ast_node import ASTNode
from .literals import CalculationNode
from .functions import FunctionCallNode
from .identifiers import IdentifierNode


from typing import Union


class BinaryOperatorNode(CalculationNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode, line: int, position: int):
        super().__init__(line, position)
        self.left = left
        self.operator = operator
        self.right = right


class AssignmentNode(BinaryOperatorNode):
    pass


class LogicalOperatorNode(BinaryOperatorNode):
    pass


class ComparisonNode(BinaryOperatorNode):
    pass


class ArithmeticOperatorNode(BinaryOperatorNode):
    pass


class MemberOperatorNode(BinaryOperatorNode):
    pass


class KeymapOperatorNode(BinaryOperatorNode):
    pass


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
