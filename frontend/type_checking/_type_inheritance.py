from ..abstract_syntax_tree import *

from ._helpers_class import get_class_by_name
from ._type_match import strict_match_types


# TODO: refactor
def __check_type_generic_params(
    type_class: TypeNode,
    other_class: TypeNode
):
    """
    Checks if the TypeNodes have the same instantiated generic parameters
    without any implicit casts possible
    :param type_class:
    :param other_class:
    :return:
    """
    # classes SHOULD be either both generic or both not
    if type_class.category != other_class.category:
        return False

    # check trivial cases
    if type_class.category == TypeCategory.GENERIC_CLASS:
        # uninstantiated generics (actually, it's code bug)
        if not type_class.arguments or not other_class.arguments:
            raise AssertionError("This shouldn't happen anyway")

        # different lengths
        if len(type_class.arguments) != len(other_class.arguments):
            return False

        # check if different signatures
        return not any((not strict_match_types(x, y) for x, y in zip(type_class.arguments, other_class.arguments)))

    elif type_class.category == TypeCategory.CLASS:
        # instantiated generics (actually, it's code bug)
        if type_class.arguments or other_class.arguments:
            raise AssertionError("This shouldn't happen anyway")
    return True


def least_common_base(
    cls: ClassDefinitionNode | TypeNode,
    other: ClassDefinitionNode | TypeNode
) -> str | None:
    """
    This method gets the name of the least common base class of the two given classes.
    E.g, Consider this scheme tree of inheritance:
    A -> B -> C;
    C -> D;
    C -> E -> F;
    Then least_common_base(D, F) will return C
    :param cls: TypeNode or ClassDefinitionNode
    :param other: TypeNode or ClassDefinitionNode
    :return: name of least common base class of the two given classes
    """
    # check usage and generics
    if isinstance(other, ClassDefinitionNode) and isinstance(cls, ClassDefinitionNode):
        if len(cls.generic_params) != len(other.generic_params):
            return None
    elif isinstance(other, TypeNode) and isinstance(cls, TypeNode):
        if not __check_type_generic_params(cls, other):
            return None
    else:
        raise AssertionError("Invalid use: should be a ClassDefinitionNode or TypeNode and equal type args")

    cls_inheritance_tree = get_superclass_list(cls, as_strings=True)
    other_inheritance_tree = get_superclass_list(other, as_strings=True)

    # one of classes doesn't even exist :/
    if cls_inheritance_tree is None or other_inheritance_tree is None:
        return None

    # find common one
    common = set(cls_inheritance_tree).intersection(other_inheritance_tree)
    if not common:
        return None
    else:
        # return first one in the sequence
        for cls_name in cls_inheritance_tree:
            if cls_name in common:
                return cls_name


# TODO: ugly code
def get_superclass_list(
    cls: ClassDefinitionNode | TypeNode | str,
    as_strings: bool = False
) -> list[ClassDefinitionNode | str] | None:
    """
    Gets a list of superclasses (as class definition nodes or string names) from a class definition node, or it's name
    :param cls: string of class name, TypeNode or ClassDefinitionNode instance
    :param as_strings: whether to return superclasses list as strings or nodes. True if strings, False if nodes
    :return: list of superclasses (including self), or empty if class is invalid
    """
    if isinstance(cls, TypeNode):
        cls_node = get_class_by_name(cls.name)
    elif isinstance(cls, str):
        cls_node = get_class_by_name(cls)
    else:
        cls_node = cls

    if cls_node is None:
        return []

    # inner restrictions for inheritance depth
    _loop_iterations = 0
    _while_loop_limiter = 100

    curr_class_node = cls_node
    tree = [curr_class_node.name if as_strings else curr_class_node]

    while curr_class_node.superclass is not None and _loop_iterations < _while_loop_limiter:
        curr_class_node = get_class_by_name(curr_class_node.superclass.name)
        if as_strings:
            tree.append(curr_class_node.name)
        else:
            tree.append(curr_class_node)
        _loop_iterations += 1
    return tree


def is_class_type_subtype_of(
    cls: TypeNode,
    other: TypeNode,
) -> bool:
    if isinstance(other, ClassDefinitionNode) and isinstance(cls, ClassDefinitionNode):
        return __is_subclass_of(cls, other)
    elif not (isinstance(other, TypeNode) and isinstance(cls, TypeNode)):
        raise AssertionError("Invalid use: should be a ClassDefinitionNode or TypeNode and equal type args")

    if (
        cls.category not in (TypeCategory.CLASS, TypeCategory.GENERIC_CLASS) or
        other.category not in (TypeCategory.CLASS, TypeCategory.GENERIC_CLASS)
    ):
        return False

    if not __check_type_generic_params(cls, other):
        return False

    # get class instances
    class_instance = get_class_by_name(cls.name)
    other_instance = get_class_by_name(other.name)

    # check if generics args count match
    if not (
            len(class_instance.generic_params) == len(other_instance.generic_params) == len(cls.arguments)
    ):
        return False

    # check inheritance
    return __is_subclass_of(
        class_instance, other_instance
    )


def __is_subclass_of(
    cls_node: ClassDefinitionNode,
    other_node: ClassDefinitionNode
):
    """
    (Private)
    Checks two ClassDefinitionNode instances if first is subclass of the second
    :param cls_node:
    :param other_node:
    :return:
    """
    # case 1. class is a subclass of itself
    if cls_node.name == other_node.name:
        return True

    elif cls_node.superclass is None:
        return False

    __loop_iterations = 0
    __while_loop_limiter = 100
    curr_class_node = cls_node
    while curr_class_node.superclass is not None and __loop_iterations < __while_loop_limiter:
        curr_class_node = get_class_by_name(curr_class_node.superclass.name)
        if curr_class_node is None:
            return False

        if curr_class_node.name == other_node.name:
            return True

        __loop_iterations += 1
    return False
