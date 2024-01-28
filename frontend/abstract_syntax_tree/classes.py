from .ast_node import ASTNode
from .functions import FunctionParameter
from .scope import ScopeNode
from .typing import UserDefinedTypeNode, GenericClassTypeNode, TypeNode


class ClassDefinitionNode(ASTNode):
    def __init__(
        self,
        class_name: str,
        generic_parameters: list["GenericParameterNode"],
        inherited_class: UserDefinedTypeNode | GenericClassTypeNode | None,
        fields_definitions: list,
        methods_definitions: list,
        static_fields_definitions: list,
        static_methods_definitions: list,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.class_name = class_name
        self.generic_parameters = generic_parameters
        self.inherited_class = inherited_class
        self.fields_definitions = fields_definitions
        self.methods_definitions = methods_definitions
        self.static_fields_definitions = static_fields_definitions
        self.static_methods_definitions = static_methods_definitions


class GenericParameterNode(ASTNode):
    def __init__(self, name, line, position):
        super().__init__(line, position)
        self.name = name


class ClassMethodDeclarationNode(ASTNode):
    def __init__(
        self,
        return_type: TypeNode,
        function_name: str,
        parameters: list["FunctionParameter"],
        function_body: ScopeNode,
        access_type: str,
        static: bool,
        virtual: bool,
        overload: bool,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.return_type = return_type
        self.function_name = function_name
        self.parameters = parameters
        self.function_body = function_body

        self.access_type = access_type
        self.static = static
        self.virtual = virtual
        self.overload = overload


class ClassFieldDeclarationNode(ASTNode):
    def __init__(
        self,
        _type: ASTNode,
        name: str,
        operator: str | None,
        value: ASTNode | None,
        access_type: str,
        static: bool,
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self.type = _type
        self.name = name
        self.operator = operator
        self.value = value

        self.access_type = access_type
        self.static = static
