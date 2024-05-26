from abc import ABC, abstractmethod
from typing import Sequence, TextIO


class ASTNode(ABC):
    def __init__(self, line, position):
        self.line = line
        self.position = position
        self.valid = None

    def __str__(self):
        return _TreePrinter.print_tree(self)[0] + _TreePrinter.END_COLOR

    @property
    def location(self) -> tuple[int, int]:
        return self.line, self.position

    @abstractmethod
    def translate(self, file: TextIO, **kwargs) -> None:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @staticmethod
    def write_instruction(file: TextIO, tokens):
        for token in tokens:
            file.write(token)
        file.write('\n')


class _TreePrinter:
    """

    """

    MIDDLE_VAR = '├──'
    LAST_VAR = '└──'
    EMPTY = '    '
    GOING = '│   '

    NOT_VALIDATED = '\033[93m'
    INVALID = '\033[91m'
    VALID = '\033[92m'

    END_COLOR = '\033[0m'

    @staticmethod
    def get_color(node: ASTNode | list | tuple, last_color: str | None = None) -> str:
        if last_color:
            return last_color

        if node.valid is None:
            return _TreePrinter.NOT_VALIDATED
        elif node.valid is False:
            return _TreePrinter.INVALID
        else:
            return _TreePrinter.VALID

    @staticmethod
    def print_tree(
        tree: ASTNode | Sequence[ASTNode],
        indent: str = "",
        last: bool | None = None,
        last_color: str = ""
    ):

        if not isinstance(tree, (ASTNode, list, tuple)):
            return last_color + str(tree) + "\n", last_color

        if isinstance(tree, ASTNode) and hasattr(tree, '__print_tree__'):
            color = _TreePrinter.get_color(tree)
            return color + tree.__print_tree__() + "\n", color

        if last is not None:
            indent += (
                _TreePrinter.get_color(tree, last_color) +
                (_TreePrinter.EMPTY if last else _TreePrinter.GOING)
            )

        if isinstance(tree, (list, tuple)):

            arg_num = len(tree)
            result_string = "\n"
            for index, item in enumerate(tree):
                marker = _TreePrinter.LAST_VAR if index == arg_num - 1 else _TreePrinter.MIDDLE_VAR

                substr, sub_color = _TreePrinter.print_tree(item, indent, index == arg_num - 1, last_color)
                result_string += f"{indent}{last_color}{marker}{substr}"

            return result_string, last_color

        if hasattr(tree, "__tree_name__"):
            class_name = tree.__tree_name__()
        else:
            class_name = type(tree).__name__.replace("Node", "")

        color = _TreePrinter.get_color(tree)
        res = f"{color}{class_name}\n"

        attrs = tree.__tree_dict__() if hasattr(tree, "__tree_dict__") else tree.__dict__.copy()
        attrs.pop("line", None)
        attrs.pop("position", None)
        attrs.pop("valid", None)
        attrs.pop("translatable", None)
        arg_num = len(attrs)
        for index, (arg_name, arg_value) in enumerate(attrs.items()):
            arg_name = arg_name.lstrip("_")
            marker = _TreePrinter.LAST_VAR if index == arg_num - 1 else _TreePrinter.MIDDLE_VAR
            substr, sub_color = _TreePrinter.print_tree(arg_value, indent, index == arg_num - 1, color)
            res += f"{indent}{color}{marker}{sub_color}{arg_name}: {substr}"
        return res, color
