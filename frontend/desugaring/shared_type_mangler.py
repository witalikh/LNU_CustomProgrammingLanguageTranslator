from ..abstract_syntax_tree import TypeNode



def mangle_typenode(type_node: TypeNode) -> None:
    """
    Standardized type node name mangler for every case in desugaring stage
    """
    l = []
    l += 'c' if type_node.is_constant else 'm'
    l += 'r' if type_node.is_reference else 'o'
    l += 'n' if type_node.is_nullable else 'p'
    l += type_node.type.name
    if type_node.arguments:
        l += '__'.join([mangle_typenode(t) for t in type_node.arguments])

    if type_node.represents_generic_param:
        raise ValueError("It shouldn't be herem the generic type repr...")
    
    return '_'.join(l)
