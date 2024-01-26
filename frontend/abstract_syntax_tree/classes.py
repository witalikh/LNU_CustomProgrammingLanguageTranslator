from .ast_node import ASTNode


class ClassDefinitionNode(ASTNode):
    def __init__(self, class_name, *_, line: int, position: int):
        super().__init__(line, position)
        self.class_name = class_name
