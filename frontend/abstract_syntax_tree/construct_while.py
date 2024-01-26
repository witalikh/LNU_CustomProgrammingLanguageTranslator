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
