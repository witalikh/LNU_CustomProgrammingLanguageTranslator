from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag
import frontend.abstract_syntax_tree as AST

from frontend.syntax import TokenType, TypeModifier

import frontend.parser.parse_operators as arith
import frontend.parser.parse_literal as literals
import frontend.parser.post_parser as post


# TODO: more comments
# TODO: do we really need that parser? Check it
def parse_full_variable_declaration(parser: Parser, context: ContextFlag) -> AST.VariableDeclarationNode | AST.ClassFieldDeclarationNode:
    type_node = parse_type_declaration(parser, context)
    return _parse_partial_variable_expression(parser, type_node, context)

def _parse_partial_variable_expression(parser: Parser, type_node: AST.ASTNode, context: ContextFlag)\
        -> AST.VariableDeclarationNode | AST.ClassFieldDeclarationNode:
    identifier: str = parser.consume(TokenType.IDENTIFIER)
    line, position = parser.line_and_position_of_consumed_token()

    if ContextFlag.strict_match(context, flag=ContextFlag.CLASS):
        result = AST.ClassFieldDeclarationNode(
            _type=type_node, name=identifier,
            access_type=AST.AccessType.PROTECTED, static=False,
            line=line, position=position
        )
    else:
        if parser.match(TokenType.GENERIC_ASSIGNMENT):
            operator = parser.consume(TokenType.GENERIC_ASSIGNMENT)
            expression_node = arith.parse_assignment_expression(parser, context)
        else:
            operator = None
            expression_node = None

        result = AST.VariableDeclarationNode(
            _type=type_node, name=identifier,
            operator=operator, value=expression_node, line=line, position=position)

    parser.consume(TokenType.END_OF_STATEMENT)
    return result

def parse_full_expression(parser: Parser, context) -> AST.VariableDeclarationNode | AST.ClassFieldDeclarationNode | AST.AssignmentNode | AST.ASTNode:
    result = arith.parse_assignment_expression(parser, context)
    if parser.match(TokenType.IDENTIFIER):
        type_name = post.refine_identifier(parser, result, refine_as="class_name")
        return _parse_partial_variable_expression(parser, type_name, context)
    parser.consume(TokenType.END_OF_STATEMENT)
    return result

def parse_type_declaration(parser: Parser, context: ContextFlag) -> AST.TypeNode:
    # Check for const or reference modifiers
    modifiers = []
    while parser.match(TokenType.TYPE_MODIFIER):
        modifiers.append(parser.consume(TokenType.TYPE_MODIFIER))

    # Parse the base type (simple or compound)
    base_type = parse_base_type(parser, context)

    # Apply modifiers to the base type
    for modifier in modifiers:
        match modifier:
            case TypeModifier.CONST:
                base_type.set_constant()
            case TypeModifier.NULLABLE:
                base_type.set_nullable()
            case TypeModifier.REFERENCE:
                base_type.set_reference()

    return base_type

def parse_base_type(parser: Parser, context: ContextFlag, as_constructor: bool = False) -> AST.TypeNode:
    if parser.match(TokenType.SIMPLE_TYPE):
        type_name = parser.consume(TokenType.SIMPLE_TYPE)
        line, position = parser.line_and_position_of_consumed_token()
        type_literal_node = AST.TypeLiteral(name=type_name, line=line, location=position)
        return AST.TypeNode(
            category=AST.TypeCategory.PRIMITIVE,
            type_node=type_literal_node, args=None, line=line, position=position
        )

    elif parser.match(TokenType.COMPOUND_TYPE):
        compound_type = parser.consume(TokenType.COMPOUND_TYPE)
        line, position = parser.line_and_position_of_consumed_token()

        parameters = []
        if parser.match(TokenType.OPENING_SQUARE_BRACKET):
            parser.consume(TokenType.OPENING_SQUARE_BRACKET)
            line, position = parser.line_and_position_of_consumed_token()

            parameters = []

            while parser.current_token.type != TokenType.CLOSING_SQUARE_BRACKET:
                argument = arith.parse_arithmetic_expression(parser, context=context)
                parameters.append(argument)

                if parser.match(TokenType.CLOSING_SQUARE_BRACKET):
                    break
                parser.consume(TokenType.COMMA)

            parser.consume(TokenType.CLOSING_SQUARE_BRACKET)

        type_literal_node = AST.TypeLiteral(name=compound_type, line=line, location=position)
        return AST.TypeNode(
            category=AST.TypeCategory.COLLECTION,
            type_node=type_literal_node, args=parameters, line=line, position=position
        )

    elif parser.match(TokenType.IDENTIFIER):
        identifier = arith.parse_function_call(parser, context)
        return post.refine_identifier(parser, node=identifier, refine_as="constructor" if as_constructor else "class_name")

    else:
        parser.error(msg="Invalid type declaration")