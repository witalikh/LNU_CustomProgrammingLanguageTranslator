from enum import IntEnum
from typing import Literal, TextIO
import struct

from .literals import LiteralNode


# NOTE: it's here due to possible circular import
class IntegerSizes(IntEnum):
    BYTE = 0
    SHORT = 1
    INTEGER = 2
    LONG = 3
    EXTENDED = 4


class FloatSizes(IntEnum):
    FLOAT = 0
    DOUBLE = 1


class IntegerLiteralNode(LiteralNode):
    def __init__(self, value: str, base: Literal[10, 16, 8, 2], line: int, position: int) -> None:
        super().__init__(line, position)
        self._value = int(value, base)
        self._size = None
        self.__init_size_()

    def __init_size_(self):
        # at least one bit is reserved for sign
        bit_length = self._value.bit_length() + 1

        if bit_length <= 8:
            self._size = IntegerSizes.BYTE
        elif bit_length <= 16:
            self._size = IntegerSizes.SHORT
        elif bit_length <= 32:
            self._size = IntegerSizes.INTEGER
        elif bit_length <= 64:
            self._size = IntegerSizes.LONG
        else:
            self._size = IntegerSizes.EXTENDED

    @property
    def value(self) -> int:
        return self._value

    @property
    def size(self) -> None | IntegerSizes:
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

    def translate(self, file: TextIO, **kwargs) -> None:
        file.write(str(self.value))


class FloatLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int) -> None:
        super().__init__(line=line, position=position)
        self._value = float(value)
        self._size = None
        self._init_sizes()

    def _init_sizes(self) -> None:
        if self.is_nan or self.is_negative_infinity or self.is_positive_infinity:
            self._size = FloatSizes.FLOAT
            return

        try:
            packed_value = struct.pack('f', self._value)
            unpacked_value = struct.unpack('f', packed_value)
            if unpacked_value == self._value:
                self._size = FloatSizes.FLOAT
            else:
                self._size = FloatSizes.DOUBLE

        except (OverflowError, ValueError,):
            self._size = FloatSizes.DOUBLE

    @property
    def value(self) -> float:
        return self._value

    @property
    def size(self) -> FloatSizes:
        return self._size

    @property
    def is_nan(self) -> bool:
        return self._value != self._value

    @property
    def is_positive_infinity(self) -> bool:
        return self._value == float('inf')

    @property
    def is_negative_infinity(self) -> bool:
        return self._value == float('-inf')

    @property
    def is_positive(self) -> bool:
        return self._value > 0

    @property
    def is_negative(self) -> bool:
        return self._value < 0

    @property
    def is_non_positive(self) -> bool:
        return self._value <= 0

    @property
    def is_non_negative(self) -> bool:
        return self._value >= 0

    @property
    def is_zero(self) -> bool:
        return self._value == 0

    def translate(self, file: TextIO, **kwargs) -> None:
        file.write(str(self.value))


class ImaginaryFloatLiteralNode(FloatLiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(value, line, position)
        self._value = value

    def translate(self, file: TextIO, **kwargs) -> None:
        file.write('IMAGINARY')
        file.write(' ')
        file.write(str(self.value))
