from .._syntax.operators import OperatorMethods, Assignment

from .ast_node import ASTNode
from .literals import CalculationNode
from .functions import FunctionCallNode
from .identifiers import IdentifierNode


from abc import ABC
from typing import Union, TextIO
from enum import StrEnum


class OperatorCategory(StrEnum):
    Arithmetic = "Arithmetic"
    Logical = "Logical"
    Comparison = "Comparison"
    Allocation = "Allocation"
    Reference = "Reference"
    Casting = "Casting"
    Coalesce = "Coalesce"


class OperatorABC(CalculationNode, ABC):
    def __init__(
        self,
        category: OperatorCategory,
        line: int,
        position: int
    ) -> None:
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


class BinaryOperatorABCNode(OperatorABC):
    def __init__(
        self,
        category: OperatorCategory,
        left: ASTNode,
        operator: str,
        right: ASTNode,
        line: int,
        position: int
    ) -> None:
        super().__init__(category, line, position)

        self.left = left
        self.operator = operator
        self.right = right

        self.is_overload = False
        self.overload_number = 0

    def translate(self, file: TextIO, **kwargs) -> None:
        if self.is_overload:
            file.write('CALL')

            file.write(' ')
            file.write(str(3))
            file.write(' ')
            file.write('ID')
            file.write(' ')
            if self.overload_number != 0:
                file.write(f"$operator_{OperatorMethods.translate(self.operator, 2)}$_{self.overload_number}")
            else:
                file.write(f"$operator_{OperatorMethods.translate(self.operator, 2)}")
        else:
            file.write(OperatorMethods.translate(self.operator, 2))
        file.write(' ')
        self.left.translate(file, **kwargs)
        file.write(' ')
        self.right.translate(file, **kwargs)

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.left.is_valid(),
            self.right.is_valid()
        ))


class UnaryOperatorABCNode(OperatorABC):
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

        self.is_overload = False
        self.overload_number = 0

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.expression.is_valid(),
        ))

    def translate(self, file: TextIO, **kwargs) -> None:
        if self.is_overload:
            file.write('CALL')

            file.write(' ')
            file.write(str(2))
            file.write(' ')
            file.write('ID')
            file.write(' ')
            if self.overload_number != 0:
                file.write(f"$operator_{OperatorMethods.translate(self.operator, 1)}$_{self.overload_number}")
            else:
                file.write(f"$operator_{OperatorMethods.translate(self.operator, 1)}")
        else:
            file.write(OperatorMethods.translate(self.operator, 1))
        file.write(' ')
        self.expression.translate(file, **kwargs)


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

    def translate(self, file: TextIO, **kwargs) -> None:
        if isinstance(self.right, AssignmentNode):
            self.right.translate(file, **kwargs)
            file.write('\n')
        file.write(Assignment.translate(self.operator))
        file.write(' ')
        self.left.translate(file, **kwargs)
        file.write(' ')
        if isinstance(self.right, AssignmentNode):
            self.right.left.translate(file, **kwargs)
        else:
            self.right.translate(file, **kwargs)


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

    def translate(self, file: TextIO, **kwargs) -> None:
        file.write(OperatorMethods.translate(self.operator, 2))
        file.write(' ')
        self.left.translate(file, **kwargs)
        file.write(' ')
        self.right.translate(file, **kwargs)


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

        self.is_overload = False
        self.overload_number = 0

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.variable.is_valid(),
            all((a.is_valid() for a in self.arguments))
        ))

    def translate(self, file: TextIO, **kwargs) -> None:
        if self.is_overload:
            file.write('CALL')

            file.write(' ')
            file.write(str(len(self.arguments) + 2))
            file.write(' ')
            file.write('ID')
            file.write(' ')
            if self.overload_number != 0:
                file.write(f"$operator_index$_{self.overload_number}")
            else:
                file.write(f"$operator_index")
        else:
            file.write('INDEX')
            file.write(' ')
            file.write(str(len(self.arguments) + 1))
        file.write(' ')
        self.variable.translate(file, **kwargs)
        for arg in self.arguments:
            file.write(' ')
            arg.translate(file, **kwargs)
