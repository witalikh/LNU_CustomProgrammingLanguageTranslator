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

        # self._all_paths_return = None

    # @property
    # def all_paths_return(self):
    #     if self._all_paths_return is None:
    #         if self.else_scope is None:
    #
    #         self._all_paths_return = self.if_scope.all_paths_return

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.condition.is_valid(),
            self.if_scope.is_valid(),
            self.else_scope.is_valid() if self.else_scope else True
        ))
