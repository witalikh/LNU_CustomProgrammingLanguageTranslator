from .ast_node import ASTNode
from .literals import CalculationNode
from .scope import ScopeNode
from .typing import TypeNode
from .ast_mixins import Usable


class FunctionDeclarationNode(ASTNode, Usable):
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

    @property
    def parameters_signature(self) -> list[TypeNode]:
        return list(
            map(lambda p: p.type_node, self.parameters)
        )

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.return_type.is_valid() if self.return_type else True,
            all((p.is_valid() for p in self.parameters)),
            self.function_body.is_valid(),
            self.external_to.is_valid() if self.external_to else True
        ))


class FunctionParameter(ASTNode, Usable):
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

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.type_node.is_valid(),
            self.default_value.is_valid() if self.default_value else True
        ))


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

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((a.is_valid() for a in self.arguments))
        ))
