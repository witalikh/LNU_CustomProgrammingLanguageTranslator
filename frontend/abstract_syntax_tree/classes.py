from .ast_node import ASTNode
from .functions import FunctionParameter
from .scope import ScopeNode
from .typing import TypeNode

from itertools import chain
from typing import Iterator, Union


class AccessType:
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


class ClassDefinitionNode(ASTNode):
    def __init__(
        self,
        class_name: str,
        generic_parameters: list["GenericParameterNode"],
        superclass: TypeNode | None,
        fields_definitions: list["ClassFieldDeclarationNode"],
        methods_definitions: list["ClassMethodDeclarationNode"],
        static_fields_definitions: list["ClassFieldDeclarationNode"],
        static_methods_definitions: list["ClassMethodDeclarationNode"],
        line: int,
        position: int
    ):
        super().__init__(line, position)
        self._name = class_name
        self._generic_params = generic_parameters
        self._superclass = superclass
        self.fields_definitions = fields_definitions
        self.methods_definitions = methods_definitions
        self.static_fields_definitions = static_fields_definitions
        self.static_methods_definitions = static_methods_definitions

        # inheritance meta info
        self._valid_inherited_class = True if self.superclass is None else None
        self._valid_inherited_methods = None
        self._inherited_class_instance = None

        #
        self._usages = 0
        self._instantiations = None

    @property
    def name(self):
        return self._name

    @property
    def generic_params(self):
        return self._generic_params

    @property
    def all_fields_definitions(self) -> Iterator["ClassFieldDeclarationNode"]:
        return chain(self.fields_definitions, self.static_fields_definitions)

    @property
    def superclass(self):
        return self._superclass

    @property
    def superclass_node(self) -> Union["ClassDefinitionNode", None]:
        return self._inherited_class_instance

    @property
    def is_valid_inherited_class(self) -> bool | None:
        return self._valid_inherited_class

    @property
    def is_valid_inherited_methods(self) -> bool | None:
        return self._valid_inherited_methods

    # AST type checker methods

    def set_inherited_class(self, inherited_class: "ClassDefinitionNode"):
        self._valid_inherited_class = inherited_class

    def validate_inherited_class(self, valid: bool) -> None:
        self._valid_inherited_class = valid

    def validate_inherited_methods(self, valid: bool) -> None:
        self._valid_inherited_methods = valid

    def use(self):
        self._usages += 1

    def add_instantiation(self, instantiation):
        self.use()
        if self._instantiations is None:
            self._instantiations = []

        if len(instantiation) != self.generic_params:
            raise ValueError("Args count mismatch")
        self._instantiations.append(instantiation)


class GenericParameterNode(ASTNode):
    def __init__(self, name, line, position):
        super().__init__(line, position)
        self.name = name


class AccessTypeMixin:
    @property
    def access_type(self) -> str:
        return self._access_type

    @property
    def is_public(self) -> bool:
        return self._access_type == AccessType.PUBLIC

    @property
    def is_private(self) -> bool:
        return self._access_type == AccessType.PRIVATE

    @property
    def is_protected(self) -> bool:
        return self._access_type == AccessType.PROTECTED

    def set_access_type(self, value: AccessType | str):
        self._access_type = value


class ClassMethodDeclarationNode(ASTNode, AccessTypeMixin):
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

        self._access_type = access_type
        self._static = static
        self._virtual = virtual
        self._overload = overload

        # Type checker
        self._usages = 0

    @property
    def is_static(self) -> bool:
        return self._static

    @is_static.setter
    def is_static(self, value: bool):
        self._static = value

    @property
    def is_virtual(self) -> bool:
        return self._virtual

    @is_virtual.setter
    def is_virtual(self, value: bool):
        self._static = value

    @property
    def is_overload(self) -> bool:
        return self._overload

    @is_overload.setter
    def is_overload(self, value: bool):
        self._overload = value

    @property
    def parameters_signature(self) -> list[TypeNode]:
        return list(
            map(lambda p: p.type_node, self.parameters)
        )

    def use(self):
        self._usages += 1


class ClassFieldDeclarationNode(ASTNode, AccessTypeMixin):
    def __init__(
        self,
        _type: TypeNode,
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

        self._access_type = access_type
        self._static = static

        # Type checking
        self._usages = 0

    @property
    def is_static(self) -> bool:
        return self._static

    @is_static.setter
    def is_static(self, value: bool):
        self._static = value

    def use(self):
        self._usages += 1
