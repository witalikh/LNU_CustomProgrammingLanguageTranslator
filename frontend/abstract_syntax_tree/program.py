from .ast_node import ASTNode
from .function import FunctionDeclarationNode


class ProgramNode(ASTNode):
    def __init__(
        self,
        class_definitions,
        function_definitions: list[FunctionDeclarationNode],
        statements: list[ASTNode]
    ):
        super().__init__(line=0, position=0)
        self.class_definitions = class_definitions
        self.function_definitions = function_definitions
        self.statements = statements
