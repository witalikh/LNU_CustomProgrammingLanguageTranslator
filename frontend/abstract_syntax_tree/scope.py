from .ast_node import ASTNode


class ScopeNode(ASTNode):
    def __init__(
        self,
        statements: list[ASTNode],
        local_variables: list[ASTNode],
        line: int,
        position: int,
    ):
        super().__init__(line, position)
        self.statements = statements
        self.local_variables = local_variables or []

        # self.all_paths_return = None
