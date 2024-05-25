from ..abstract_syntax_tree import ProgramNode


def instantiate_all_generics(root: ProgramNode):

    cleaned_class_definitions = []
    for class_defn in root.class_definitions:
        if class_defn.generic_params:
            for inst in class_defn._instantiations:
                pass



def instantiate_generics():
    pass