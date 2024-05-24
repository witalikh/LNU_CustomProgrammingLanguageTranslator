from ..abstract_syntax_tree import FunctionDefNode, ClassDefNode
from .core import ErrorLogger

error_logger = ErrorLogger()
class_definitions: list[ClassDefNode] = []
function_definitions: list[FunctionDefNode] = []
