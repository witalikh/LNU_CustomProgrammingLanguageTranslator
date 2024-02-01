from .ast_node import ASTNode
from .literals import CalculationNode


class UnaryOperatorNode(CalculationNode):
    def __init__(self, operator: str, expression: ASTNode, line: int, position: int):
        super().__init__(line, position)
        self.operator = operator
        self.expression = expression


class AllocationOperatorNode(UnaryOperatorNode):
    pass


class ReferenceOperatorNode(UnaryOperatorNode):
    pass
