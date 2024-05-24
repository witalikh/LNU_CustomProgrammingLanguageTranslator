from ..abstract_syntax_tree import ProgramNode, ClassDefNode


def clean_up_unused(ast_tree: ProgramNode) -> None:
    cleaned_classes = []
    cleaned_functions = []

    # clean unused classes in general
    for class_node in ast_tree.class_definitions:
        assert class_node.usages is not None, f"Type checker did not check the class definition {class_node.name}"
        if class_node.usages > 0:
            cleaned_classes.append(class_node)
            clean_class_methods(class_node=class_node)

    ast_tree.class_definitions = cleaned_classes

    # clean unued functions in general
    for function_node in ast_tree.function_definitions:
        assert function_node.usages is not None
        if function_node.usages > 0:
            cleaned_functions.append(function_node)

    ast_tree.function_definitions = cleaned_functions


def clean_class_methods(class_node: ClassDefNode) -> None:
    cleaned_non_static_methods = []
    cleaned_static_methods = []
    for method_node in class_node.methods_defs:
        assert method_node.usages is not None, f"Type checker did not check the method definition {method_node.function_name}"
        if method_node.usages or method_node.is_overload or method_node.is_virtual:
            cleaned_non_static_methods.append(method_node)

    for static_method_node in class_node.static_methods_defs:
        assert static_method_node.usages is not None, f"Type checker did not check the static method definition {static_method_node.function_name}"
        if static_method_node.usages:
            cleaned_static_methods.append(static_method_node)

    class_node.methods_defs = cleaned_non_static_methods
    class_node.static_methods_defs = cleaned_static_methods
