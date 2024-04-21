from ..abstract_syntax_tree import FunctionDeclarationNode, ClassDefinitionNode
from .core import ErrorLogger

error_logger = ErrorLogger()
class_definitions: list[ClassDefinitionNode] = []
function_definitions: list[FunctionDeclarationNode] = []
