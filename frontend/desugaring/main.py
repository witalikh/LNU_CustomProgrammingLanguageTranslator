from ..abstract_syntax_tree import ProgramNode
from .cleaning import clean_up_unused



def desugar_ast_tree(typed_ast: ProgramNode) -> None:
    p = typed_ast
    clean_up_unused(p)
    # p = mangle_templates(p)
    # p = mangle_methods(p)
    # p = mangle_functions(p)
    # p = mangle_classes_into_structs(p)
