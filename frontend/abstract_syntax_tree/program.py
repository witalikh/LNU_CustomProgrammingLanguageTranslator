from .ast_node import ASTNode
from .classes import ClassDefinitionNode
from .functions import FunctionDeclarationNode


class ProgramNode(ASTNode):
    def __init__(
        self,
        class_definitions: list[ClassDefinitionNode],
        function_definitions: list[FunctionDeclarationNode],
        statements: list[ASTNode]
    ):
        super().__init__(line=0, position=0)
        self.class_definitions = class_definitions
        self.function_definitions = function_definitions
        self.statements = statements
