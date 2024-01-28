from ..abstract_syntax_tree import ASTNode
from ..exceptions import SemanticException


def collect_error(node: ASTNode, reason: str):
    return SemanticException(reason, node.line, node.position)
