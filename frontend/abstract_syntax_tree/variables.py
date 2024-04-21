from .ast_node import ASTNode


class VariableDeclarationNode(ASTNode):

    def __init__(
        self,
        _type: "TypeNode",
        name: str,
        operator: str | None,
        value: ASTNode | None,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.type = _type
        self.name = name
        self.operator = operator
        self.value = value

    def is_valid(self) -> bool:
        return (
            self.valid
            and self.type.is_valid()
            and self.value.is_valid() if self.value is not None else True
        )
