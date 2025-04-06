from frontend.parser.parser import Parser
import frontend.abstract_syntax_tree as AST


from typing import Literal


def refine_identifier(
    parser: Parser,
    node,
    refine_as: Literal["class_name", "constructor"]
) -> AST.TypeNode | AST.FunctionCallNode:
    if refine_as == "class_name":
        return refine_identifier_as_class_name(parser, node)
    elif refine_as == "constructor":
        if not isinstance(node, AST.FunctionCallNode):
            parser.error(msg="Expected parenthesised expression for constructor")
        return AST.FunctionCallNode(
            identifier=refine_identifier_as_class_name(parser, node=node.identifier),
            arguments=node.arguments,
            line=node.line,
            position=node.position,
            is_constructor=True,
        )

def refine_identifier_as_class_name(
    parser: Parser,
    node
) -> AST.TypeNode:
    if isinstance(node, AST.IdentifierNode):
        return AST.TypeNode(
            category=AST.TypeCategory.CLASS,
            type_node=node, args=None, line=node.line, position=node.position
        )
    elif isinstance(node, AST.IndexNode):
        if not isinstance(node.variable, AST.IdentifierNode):
            parser.error(msg=f"Invalid class type declaration: {node.variable.__class__.__name__}")
        return AST.TypeNode(
            category=AST.TypeCategory.GENERIC_CLASS,
            type_node=node.variable,
            args=[refine_identifier_as_class_name(parser, node=x) for x in node.arguments],
            line=node.line,
            position=node.position
        )
    elif isinstance(node, AST.TypeNode):
        if node.category in (AST.TypeCategory.PRIMITIVE, AST.TypeCategory.COLLECTION):
            return node
    else:
        parser.error(msg=f"Invalid class type declaration: {node.__class__.__name__}")