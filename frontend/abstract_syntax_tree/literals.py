from .ast_node import ASTNode


class CalculationNode(ASTNode):
    pass


class LiteralNode(CalculationNode):
    def __print_tree__(self):
        formatted_name = self.__class__.__name__.replace("LiteralNode", "")
        if hasattr(self, "value"):
            return f"{formatted_name}({self.value})"
        return formatted_name


# class NumericLiteralNode(LiteralNode):
#     def __init__(self, value):
#         self.value = value


class FloatLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class ImaginaryFloatLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class StringLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class ByteLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class ByteStringLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class CharLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class BooleanLiteralNode(LiteralNode):
    def __init__(self, value: str, line: int, position: int):
        super().__init__(line, position)
        self.value = value


class NullLiteralNode(LiteralNode):
    pass


class UndefinedLiteralNode(LiteralNode):
    pass


class ListLiteralNode(CalculationNode):
    def __init__(self, elements: list[ASTNode], line: int, position: int):
        super().__init__(line, position)
        self.elements = elements


class KeymapLiteralNode(CalculationNode):
    def __init__(self, elements: list[ASTNode], line: int, position: int):
        super().__init__(line, position)
        self.elements = elements


class EmptyLiteralNode(CalculationNode):
    def __init__(self, line: int, position: int):
        super().__init__(line, position)