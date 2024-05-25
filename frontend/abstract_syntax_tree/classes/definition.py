from itertools import chain
from typing import Iterator, Union, TextIO

from ..ast_node import ASTNode
from ..ast_mixins import Usable
from ..typing import TypeNode
from .common import GenericParameterNode
from .field import ClassFieldDeclarationNode
from .method import ClassMethodDeclarationNode


class ClassDefNode(ASTNode, Usable):
    def __init__(
        self,
        class_name: str,
        generic_parameters: list["GenericParameterNode"],
        superclass: TypeNode | None,
        fields_definitions: list["ClassFieldDeclarationNode"],
        methods_defs: list["ClassMethodDeclarationNode"],
        static_fields_defs: list["ClassFieldDeclarationNode"],
        static_methods_defs: list["ClassMethodDeclarationNode"],
        line: int,
        position: int
    ) -> None:
        super().__init__(line=line, position=position)
        self._name = class_name
        self._generic_params = generic_parameters
        self._superclass = superclass
        self.fields_definitions = fields_definitions
        self.methods_defs = methods_defs
        self.static_fields_defs = static_fields_defs
        self.static_methods_defs = static_methods_defs

        # inheritance meta info
        self._valid_inherited_class = True if self.superclass is None else None
        self._valid_inherited_methods = None
        self._inherited_class_instance = None

        # Type checker
        self._instantiations = None
        self._usages = 0

        # META INFO:
        self.translatable = not self.generic_params

    @property
    def name(self):
        return self._name

    @property
    def generic_params(self) -> list[GenericParameterNode]:
        return self._generic_params

    @property
    def superclass(self) -> TypeNode | None:
        return self._superclass

    @property
    def superclass_node(self) -> Union["ClassDefNode", None]:
        return self._inherited_class_instance

    @property
    def all_fields_definitions(self) -> Iterator["ClassFieldDeclarationNode"]:
        return chain(self.fields_definitions, self.static_fields_defs)

    @property
    def is_valid_inherited_class(self) -> bool | None:
        return self._valid_inherited_class

    @property
    def is_valid_inherited_methods(self) -> bool | None:
        return self._valid_inherited_methods

    def is_valid(self) -> bool:
        return all((
            self.valid,
            self.superclass.is_valid() if self.superclass else True,
            all((x.is_valid() for x in self.generic_params)) if self.generic_params else True,
            all((f.is_valid() for f in self.fields_definitions)),
            all((f.is_valid() for f in self.static_fields_defs)),
            all((m.is_valid() for m in self.methods_defs)),
            all((m.is_valid() for m in self.static_methods_defs)),
        ))

    # AST type checker methods

    def set_inherited_class(self, inherited_class: "ClassDefNode"):
        self._valid_inherited_class = inherited_class

    def validate_inherited_class(self, valid: bool) -> None:
        self._valid_inherited_class = valid

    def validate_inherited_methods(self, valid: bool) -> None:
        self._valid_inherited_methods = valid

    def add_instantiation(self, instantiation):
        self.use()
        if self._instantiations is None:
            self._instantiations = []

        if len(instantiation) != self.generic_params:
            raise ValueError("Args count mismatch")
        self._instantiations.append(instantiation)

    def translate(self, file: TextIO) -> None:
        if not self.translatable:
            raise ValueError("Translation error: generics not mangled ")
        if self.static_methods_defs:
            raise ValueError("Translation error: static methods not mangled")
        if self.fields_definitions:
            raise ValueError("Translation error: fields definitions not mangled")

        self.write_instruction(file, ['CLASS', ' ', self.name])
        for field in self.fields_definitions:
            field.translate(file)
            file.write('\n')
        file.write('\n')

        for method in self.methods_defs:
            method.translate(file)
            file.write('\n')

        self.write_instruction(file, ['ENDCLASS', ' ', self.name])
