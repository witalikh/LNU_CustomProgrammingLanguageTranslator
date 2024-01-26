from abc import ABC
from typing import Sequence


class ASTNode(ABC):
    def __init__(self, line, position):
        self.line = line
        self.position = position

    def __repr__(self):
        return _TreePrinter.print_tree(self)


class _TreePrinter:
    """

    """

    MIDDLE_VAR = '├──'
    LAST_VAR = '└──'
    EMPTY = '    '
    GOING = '│   '

    @staticmethod
    def print_tree(tree: ASTNode | Sequence[ASTNode], indent: str = "", last: bool | None = None):

        if not isinstance(tree, (ASTNode, list, tuple)):
            return str(tree) + "\n"

        if isinstance(tree, ASTNode) and hasattr(tree, '__print_tree__'):
            return tree.__print_tree__() + "\n"

        if last is not None:
            indent += (_TreePrinter.EMPTY if last else _TreePrinter.GOING)

        if isinstance(tree, (list, tuple)):

            arg_num = len(tree)
            result_string = "\n"
            for index, item in enumerate(tree):
                marker = _TreePrinter.LAST_VAR if index == arg_num - 1 else _TreePrinter.MIDDLE_VAR
                result_string += indent + marker + _TreePrinter.print_tree(item, indent, index == arg_num - 1)

            return result_string

        if hasattr(tree, "__tree_name__"):
            class_name = tree.__tree_name__()
        else:
            class_name = tree.__class__.__name__.replace("Node", "")
        result_string = f"{class_name}\n"

        attrs = tree.__tree_dict__() if hasattr(tree, "__tree_dict__") else tree.__dict__
        arg_num = len(attrs)
        for index, (arg_name, arg_value) in enumerate(attrs.items()):
            marker = _TreePrinter.LAST_VAR if index == arg_num - 1 else _TreePrinter.MIDDLE_VAR
            result_string += indent + marker + arg_name + ": "
            result_string += _TreePrinter.print_tree(arg_value, indent, index == arg_num - 1)
        return result_string
