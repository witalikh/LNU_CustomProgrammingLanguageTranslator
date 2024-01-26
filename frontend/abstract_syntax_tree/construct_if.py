from typing import Union

from .ast_node import ASTNode
from .scope import ScopeNode


class IfElseNode(ASTNode):
    def __init__(
        self,
        condition: ASTNode,
        if_scope: ScopeNode,
        else_scope: Union[ScopeNode, "IfElseNode", None],
        line: int,
        position: int,
    ):
        super().__init__(line, position)
        self.condition = condition
        self.if_scope = if_scope
        self.else_scope = else_scope
