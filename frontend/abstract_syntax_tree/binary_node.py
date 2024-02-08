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
    """
    a = b = c
    """

    def __init__(self, left: IdentifierNode, operator: str, right: ASTNode, line: int, position: int):
        super().__init__(left, operator, right, line, position)


class LogicalOperatorNode(BinaryOperatorNode):
    """
    Accepts booleans, return booleans
    """
    pass


class ComparisonNode(BinaryOperatorNode):
    """
    Accepts expressions, returns boolean
    """
    pass


class ArithmeticOperatorNode(BinaryOperatorNode):
    """
    Accepts expressions, return expressions
    """
    pass


class MemberOperatorNode(BinaryOperatorNode):
    """
    Class.member()
    ref class->member()
    """
    pass


class KeymapOperatorNode(BinaryOperatorNode):
    pass


class CastOperatorNode(BinaryOperatorNode):
    pass


class CoalesceOperatorNode(BinaryOperatorNode):
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
