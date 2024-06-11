from abc import ABC
from enum import StrEnum

from frontend.abstract_syntax_tree.literals import CalculationNode


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
