from ..ast_node import ASTNode


class AccessType:
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


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


class GenericParameterNode(ASTNode):
    def __init__(self, name, line, position):
        super().__init__(line, position)
        self.name = name

    def is_validated(self) -> bool:
        return self.valid is not None

    def is_valid(self) -> bool:
        return self.valid
