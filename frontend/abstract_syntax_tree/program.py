from .ast_node import ASTNode
from .classes.definition import ClassDefinitionNode
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

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((c.is_valid() for c in self.class_definitions)),
            all((f.is_valid() for f in self.function_definitions)),
            all((s.is_valid() for s in self.statements))
        ))
