from frontend._syntax.operators import OperatorMethods, Assignment

from frontend.abstract_syntax_tree.ast_node import ASTNode
from frontend.abstract_syntax_tree.literals import CalculationNode

from typing import TextIO

from .abc import OperatorCategory, OperatorABC


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
        if Assignment.is_compound_assignment(self.operator):
            file.write(Assignment.translate(Assignment.VALUE_ASSIGNMENT))
            file.write(' ')
            self.left.translate(file, **kwargs)
            file.write(' ')
            file.write(OperatorMethods.translate(Assignment.decompose_compound(self.operator), 2))
            file.write(' ')
            self.left.translate(file, **kwargs)
            file.write(' ')
            self.right.translate(file, **kwargs)
        else:
            file.write(Assignment.translate(self.operator))
            file.write(' ')
            self.left.translate(file, **kwargs)
            file.write(' ')
            if isinstance(self.right, AssignmentNode):
                self.right.left.translate(file, **kwargs)
            else:
                self.right.translate(file, **kwargs)


