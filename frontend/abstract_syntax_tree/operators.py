from .ast_node import ASTNode
from .literals import CalculationNode
from .functions import FunctionCallNode
from .identifiers import IdentifierNode


from abc import ABC
from typing import Union
from enum import StrEnum


class OperatorCategory(StrEnum):
    Arithmetic = "Arithmetic"
    Logical = "Logical"
    Comparison = "Comparison"
    Allocation = "Allocation"
    Reference = "Reference"
    Casting = "Casting"
    Coalesce = "Coalesce"


class Operator(CalculationNode, ABC):
    def __init__(
        self,
        category: OperatorCategory,
        line: int,
        position: int
    ):
        self.category = category
        super().__init__(line, position)

    @property
    def is_arithmetic(self) -> bool:
        return self.category == OperatorCategory.Arithmetic

    @property
    def is_logical(self) -> bool:
        return self.category == OperatorCategory.Logical

    @property
    def is_comparison(self) -> bool:
        return self.category == OperatorCategory.Comparison

    @property
    def is_allocation(self) -> bool:
        return self.category == OperatorCategory.Allocation

    @property
    def is_reference(self) -> bool:
        return self.category == OperatorCategory.Reference

    @property
    def is_casting(self) -> bool:
        return self.category == OperatorCategory.Casting

    @property
    def is_coalesce(self) -> bool:
        return self.category == OperatorCategory.Coalesce


class BinaryOperatorNode(Operator):
    def __init__(
        self,
        category: OperatorCategory,
        left: ASTNode,
        operator: str,
        right: ASTNode,
        line: int,
        position: int
    ):
        super().__init__(category, line, position)

        self.left = left
        self.operator = operator
        self.right = right

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.left.is_valid(),
            self.right.is_valid()
        ))


class UnaryOperatorNode(Operator):
    def __init__(
        self,
        category: OperatorCategory,
        operator: str,
        expression: ASTNode,
        line: int,
        position: int
    ):
        super().__init__(category, line, position)

        self.operator = operator
        self.expression = expression

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.expression.is_valid(),
        ))


class AssignmentNode(CalculationNode):
    """
    a = b = c
    """

    def __init__(
        self,
        left: ASTNode,
        operator: str,
        right: ASTNode,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.left = left
        self.operator = operator
        self.right = right

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.left.is_valid(),
            self.right.is_valid()
        ))


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

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.left.is_valid(),
            self.right.is_valid()
        ))


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

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.variable.is_valid(),
            all((a.is_valid() for a in self.arguments))
        ))
