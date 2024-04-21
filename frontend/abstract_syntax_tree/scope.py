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

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((s.is_valid() for s in self.statements)),
            all((v.is_valid() for v in self.local_variables))
        ))
