from .ast_node import ASTNode
from .scope import ScopeNode


class WhileNode(ASTNode):
    def __init__(
        self,
        condition: ASTNode,
        while_scope: ScopeNode,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.condition = condition
        self.while_scope = while_scope

        # self.all_paths_return = None

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.condition.is_valid(),
            self.while_scope.is_valid(),
        ))
