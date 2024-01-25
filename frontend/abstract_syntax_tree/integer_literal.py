from enum import IntEnum
from typing import Literal

from .abstract_syntax_tree import LiteralNode


# NOTE: it's here due to possible circular import
class IntegerSizes(IntEnum):
    BYTE = 0
    INTEGER = 1
    UNSIGNED = 2
    LONG = 3


class IntegerLiteralNode(LiteralNode):
    def __init__(self, value: str, base: Literal[10, 16, 8, 2]):
        self._value = int(value, base)
        self._size = None
        self.__init_size_()

    def __init_size_(self):
        if 0 <= self._value <= 255:
            self._size = IntegerSizes.BYTE
        elif -2147483648 <= self._value <= 2147483647:
            self._size = IntegerSizes.INTEGER
        elif 0 <= self._value <= 4294967295:
            self._size = IntegerSizes.UNSIGNED
        else:
            self._size = IntegerSizes.LONG

    @property
    def value(self) -> int:
        return self._value

    @property
    def size(self):
        return self._size

    @property
    def positive(self) -> bool:
        return self._value > 0

    @property
    def negative(self) -> bool:
        return self._value < 0

    @property
    def non_negative(self) -> bool:
        return self._value >= 0

    @property
    def non_positive(self) -> bool:
        return self._value <= 0

    @property
    def zero(self) -> bool:
        return self._value == 0

    @property
    def non_zero(self) -> bool:
        return self._value != 0

    def fits(self, size: IntegerSizes) -> bool:
        return self._size <= size

