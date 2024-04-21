from .ast_node import ASTNode


class IdentifierNode(ASTNode):
    def __init__(self, name: str, line: int, position: int):
        super().__init__(line, position)
        self.name = name
        # self.type = None

    def is_valid(self) -> bool:
        return self.valid

    def __print_tree__(self):
        return f"Identifier({self.name})"
