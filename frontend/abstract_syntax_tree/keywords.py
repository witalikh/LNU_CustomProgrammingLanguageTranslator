from .ast_node import ASTNode


class KeywordNode(ASTNode):

    def is_valid(self) -> bool:
        return self.valid


class BreakNode(KeywordNode):
    pass


class ThisNode(KeywordNode):
    pass


class ContinueNode(KeywordNode):
    pass


class DeductionNode(KeywordNode):
    pass


class ReturnNode(KeywordNode):
    def __init__(self, value: ASTNode, line: int, position: int) -> None:
        super().__init__(line=line, position=position)
        self.value = value
