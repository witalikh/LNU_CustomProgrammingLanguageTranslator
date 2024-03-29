from .ast_node import ASTNode
from .literals import CalculationNode
from .scope import ScopeNode
from .typing import TypeNode


class FunctionDeclarationNode(ASTNode):
    def __init__(
        self,
        return_type: TypeNode,
        function_name: str,
        parameters: list["FunctionParameter"],
        function_body: ScopeNode,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.return_type = return_type
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body

        # makes sense to operators overload
        self.external_to = None

        self.has_overloads = False
        self._usages = 0

    @property
    def parameters_signature(self) -> list[TypeNode]:
        return list(
            map(lambda p: p.type_node, self.parameters)
        )

    def use(self):
        self._usages += 1


class FunctionParameter(ASTNode):
    def __init__(
        self,
        type_node: TypeNode,
        parameter_name: str,
        default_value: ASTNode | None,
        line: int,
        position: int,
    ):
        super().__init__(line, position)
        self.type_node = type_node
        self.parameter_name = parameter_name
        self.default_value = default_value


class FunctionCallNode(CalculationNode):
    def __init__(
        self,
        identifier,
        arguments: list[ASTNode],
        line: int,
        position: int,
        is_constructor: bool = False,
    ):
        super().__init__(line, position)
        self.identifier = identifier
        self.arguments = arguments

        self.is_constructor = is_constructor

        # Type checking
        self.function = None
