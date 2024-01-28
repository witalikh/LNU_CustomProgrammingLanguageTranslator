from .ast_node import ASTNode


class IdentifierNode(ASTNode):
    def __init__(self, name: str, line: int, position: int):
        super().__init__(line, position)
        self.name = name
        # self.type = None

    def __print_tree__(self):
        return f"Identifier({self.name})"


class TemporaryIdentifierNode(ASTNode):
    def __init__(self, name: str, line: int, position: int):
        super().__init__(line, position)
        self.name = name
        self.type = None
        self.modifiers = 0

    def __print_tree__(self):
        raise ValueError("It shouldn't be in final tree!")
