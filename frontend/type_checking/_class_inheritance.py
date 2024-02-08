# NOTE: done
from ..abstract_syntax_tree import *

from .shared import error_logger
from ._type_class import get_class_by_name
from ._type_function import strict_match_signatures
from ._type_match import strict_match_types


def validate_class_inheritance(
    class_node: ClassDefinitionNode
) -> bool:
    # 1. link classes
    valid_tree = _link_and_validate_class_inheritance(class_node)
    if not valid_tree:
        return False  # no possibility to properly check all fields/methods ...

    # 2. Check inherited fields signatures
    valid_fields = _validate_inherited_fields(class_node)
    valid_methods = _validate_inherited_methods(class_node)

    # 3.
    return valid_fields and valid_methods


def _link_and_validate_class_inheritance(
    class_node: ClassDefinitionNode
) -> bool:
    """
    This function is used to validate the inheritance of the class hierarchy,
    meanwhile linking
    :param class_node:
    :return:
    """
    # if class is somehow validated, return it
    if class_node.is_valid_inherited_class is not None:
        return class_node.is_valid_inherited_class

    if class_node.superclass is None:
        class_node.validate_inherited_class(True)
        return True

    generic_args = class_node.generic_params

    # check inherited class:
    # 1. if ever exists
    # 2. if no cyclic inheritance
    # 3. if inherited class is not already invalid in terms pf inheritance
    # 4. if generics args count mismatch
    # 5. if generic args are equal
    valid = True

    class_inheritance_names_list = {class_node.name}
    class_nodes_list = [class_node]

    curr_class_node = class_node
    while curr_class_node.superclass is not None:
        curr_class_node = get_class_by_name(curr_class_node.superclass.name)
        if (
            curr_class_node is None
        ):
            error_logger.error(
                class_node.location,
                f"Inherited class {class_nodes_list[-1].superclass.name} is not unambiguously defined"
            )
            valid = False
        elif curr_class_node.name in class_inheritance_names_list:
            error_logger.error(
                class_node.location,
                f"Circular inheritance: {curr_class_node.name} from {curr_class_node.superclass.name}"
            )
            valid = False
        elif curr_class_node.is_valid_inherited_class is False:
            error_logger.error(
                class_node.location,
                f"Invalid inheritance: {curr_class_node.name} from {curr_class_node.superclass.name}"
            )
            valid = False
        elif len(curr_class_node.generic_params) != generic_args:
            error_logger.error(
                class_node.location,
                f"Superclass should be instantiated with same generic signature!"
            )
            valid = False
        elif not all((lhs.name == rhs.name for lhs, rhs in zip(curr_class_node.generic_params, generic_args))):
            error_logger.error(
                class_node.location,
                f"Superclass should be instantiated with same generic signature!"
            )
            valid = False

        if not valid:
            for class_node in class_nodes_list:
                class_node.validate_inherited_class(False)
            return False

        # set references
        class_nodes_list[-1].set_inherited_class(curr_class_node)

        if curr_class_node.is_valid_inherited_class:
            break

        class_inheritance_names_list.add(curr_class_node.name)
        class_nodes_list.append(curr_class_node)

    # for now, inheritance is ok. Field/method checking is later
    for class_node in class_nodes_list:
        class_node.validate_inherited_class(True)
    return True


def _validate_inherited_fields(
    class_node: ClassDefinitionNode
):
    """
    Check if no duplicate field name found in tree hierarchy
    Checks only regular fields, as static fields are just some kind of namespaced global variable
    :param class_node:
    :return:
    """
    if class_node.superclass_node is None:
        return True

    # the name uniqueness within the class is guaranteed by previous checks
    field_name_set = {f.name for f in class_node.fields_definitions if not f.is_private}

    # error log ALL duplicate fields if found
    found_duplicate = False
    curr_node = class_node.superclass_node
    while curr_node is not None:
        for f in curr_node.fields_definitions:
            # don't care about private fields
            if f.is_private:
                continue
            if f.name in field_name_set:
                error_logger.add(
                    f.location,
                    f"Duplicate field redefinition: {f.name} is already defined in superclass {curr_node.name}!"
                )
                found_duplicate = True
            field_name_set.add(f.name)
        curr_node = curr_node.superclass_node

    return not found_duplicate


def _validate_inherited_methods(
    class_node: ClassDefinitionNode
):
    # if class is already validated, return value
    if class_node.is_valid_inherited_methods is not None:
        return class_node.is_valid_inherited_methods

    valid_superclass = True
    if class_node.superclass_node is not None:
        valid_superclass = _validate_inherited_methods(class_node.superclass_node)

    if not valid_superclass:
        # errors are already logged
        class_node.validate_inherited_methods(False)
        return False

    # otherwise, calculate
    # assuming all overloads are valid
    # if class is at the top
    if class_node.superclass is None:
        valid = True
        for m in class_node.methods_definitions:
            if m.is_overload:
                error_logger.add(m.location, f"No base class to overload from")
                valid = False
            if m.is_private and m.is_virtual:
                error_logger.add(m.location, f"Virtual method cannot be private")
                valid = False
        class_node.validate_inherited_methods(valid)
        return valid

    # superclasses should be already validated
    # so, just collect all virtual methods
    # (no circular inheritance is possible)
    virtual_methods_names = set()
    virtual_methods_nodes = []

    current_node = class_node.superclass_node
    while current_node is not None:
        for method in current_node.methods_definitions:
            if method.is_virtual:
                virtual_methods_names.add(method.function_name)
                virtual_methods_nodes.append(method)
        current_node = current_node.superclass_node

    valid = True
    for method in current_node.methods_definitions:
        if method.function_name not in virtual_methods_names:
            if method.is_overload:
                error_logger.add(method.location, f"Method {method.function_name} has no virtual one in superclasses")
                valid = False
            else:
                continue
        else:
            matching_method_instance = None
            for virtual_method in virtual_methods_nodes:
                if strict_match_signatures(
                    method.parameters_signature,
                    virtual_method.parameters_signature
                ):
                    matching_method_instance = virtual_method
                    break

            if matching_method_instance is None:
                if method.is_overload:
                    error_logger.add(
                        method.location,
                        f"Invalid method with current signature to overload: {method.function_name}"
                    )
                    valid = False
            else:
                if not method.is_overload or method.is_virtual:
                    error_logger.add(
                        method.location,
                        f"Invalid method: {method.function_name}. It's not marked as an overload"
                    )
                    valid = False
                if method.access_type != matching_method_instance.access_type:
                    error_logger.add(
                        method.location,
                        f"Altered access type when overloading"
                    )
                    valid = False
                if not strict_match_types(method.return_type, matching_method_instance.return_type):
                    error_logger.add(
                        method.location,
                        f"Altered return type when overloading"
                    )
                    valid = False

    current_node.validate_inherited_methods(valid)
    return valid
