from .ast_node import ASTNode
from .typing import TypeNode


class FunctionDeclarationNode(ASTNode):
    def __init__(self, return_type, function_name, parameters, function_body):
        self.return_type = return_type
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body


class FunctionParameter(ASTNode):
    def __init__(
            self,
            type_node: TypeNode,
            parameter_name: str,
            operator_type: str | None,
            default_value: ASTNode | None = None
    ):
        self.type_node = type_node
        self.parameter_name = parameter_name
        self.operator_type = operator_type
        self.default_value = default_value
