from .ast_node import ASTNode


class BreakNode(ASTNode):
    pass


class ThisNode(ASTNode):
    pass


class ContinueNode(ASTNode):
    pass


class DeductionNode(ASTNode):
    pass


class ReturnNode(ASTNode):
    def __init__(self, value: ASTNode, line: int, position: int):
        super().__init__(line, position)
        self.value = value
