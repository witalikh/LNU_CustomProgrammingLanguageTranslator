from .ast_node import ASTNode
from .abstract_syntax_tree import CalculationNode


class BinaryOperatorNode(CalculationNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
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
