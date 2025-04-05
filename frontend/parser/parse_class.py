from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag
import frontend.abstract_syntax_tree as AST

from frontend.syntax import Keyword, TokenType, ClassModifierKeyword

from typing import Literal, Union

import frontend.parser.parse_scope as scope
import frontend.parser.parse_type as types
import frontend.parser.parse_function as functions

def parse_full_class_keywords(
    parser: Parser,
    context: ContextFlag
) -> Union[AST.ClassFieldDeclarationNode, AST.FunctionDefNode]:

    # scope check: only in class, but not inside methods
    if not ContextFlag.strict_match(context, ContextFlag.CLASS):
        parser.error(f"Unexpected token {parser.current_token.value} in non-class context")

    # for checking repeating keywords
    class_keywords = set()

    # obtaining needed info: access_type, polymorphism marker and static marker
    access_modifier: str | None = None
    polymorphic_modifier: str | None = None
    static: bool = False

    while parser.match(TokenType.CLASS_KEYWORD):
        value = parser.consume(TokenType.CLASS_KEYWORD)
        if value in class_keywords:
            parser.error(f"Duplicated token {value} in field/method definition")
        class_keywords.add(value)

        if value in (AST.AccessType.PUBLIC, AST.AccessType.PRIVATE, AST.AccessType.PROTECTED):
            access_modifier = (
                value if access_modifier is None else
                parser.error(f"Conflicting or repeating access type token {value} in field/method definition")
            )

        if value in (ClassModifierKeyword.VIRTUAL, ClassModifierKeyword.OVERRIDE):
            polymorphic_modifier = (
                value if polymorphic_modifier is None else
                parser.error(
                    f"Conflicting or repeating polymorphic specifier type token {value} in field/method definition"
                )
            )

        if value == ClassModifierKeyword.STATIC:
            static = True

    # end of loop
    # it's either method OR field. Nothing else!
    if parser.match(
            TokenType.KEYWORD,
            (Keyword.FUNCTION, Keyword.CONSTRUCTOR, Keyword.DESTRUCTOR, Keyword.OPERATOR)):
        result = functions.parse_full_function_definition(parser, context)
    else:
        if polymorphic_modifier is not None:
            parser.error(f"Cannot assign polymorphism marker {polymorphic_modifier} other than class method.")
        result = types.parse_full_variable_declaration(parser, context)

    if not isinstance(
        result, (AST.ClassFieldDeclarationNode, AST.ClassMethodDeclarationNode, AST.FunctionDefNode)
    ):
        parser.error(msg="Parsed expression here is not neither field nor method.")

    if isinstance(result, AST.FunctionDefNode):
        if not result.function_name.startswith("$operator_"):
            raise AssertionError("It is not a global operator overload!")
        elif not static:
            parser.error(msg="Overloading operators should be static!")
        elif polymorphic_modifier is not None:
            parser.error(msg="Overloading operators cannot be virtual")
        elif polymorphic_modifier is not None and polymorphic_modifier != AST.AccessType.PUBLIC:
            parser.error(msg="Overloading operators cannot be different access type than public!")
        return result

    if access_modifier is not None:
        result.set_access_type(access_modifier)

    if polymorphic_modifier == ClassModifierKeyword.VIRTUAL:
        result.is_virtual = True

    if polymorphic_modifier == ClassModifierKeyword.OVERRIDE:
        result.is_override = True

    if static:
        result.is_static = True

    return result

def parse_full_class_definition(parser: Parser, context: ContextFlag) -> AST.ClassDefNode:

    # scope check: global only
    if not ContextFlag.strict_match(context, ContextFlag.GLOBAL):
        parser.error(f"Unexpected token {parser.current_token.value} in non-global context.")

    # denote for other statements that currently we're inside class definition
    current_context = ContextFlag.add(context, ContextFlag.CLASS)

    # consume class keyword
    parser.consume(TokenType.KEYWORD, Keyword.CLASS)
    line, position = parser.line_and_position_of_consumed_token()

    # consume class name, without brackets or parens
    class_name = parser.consume(TokenType.IDENTIFIER)

    # parse generic parameters declaration
    generic_parameters = []
    if parser.match(TokenType.OPENING_SQUARE_BRACKET):
        generic_parameters = parse_generic_parameters(parser, "declaration", current_context)

    # parse super class if present
    inherited_class = None
    if parser.match(TokenType.KEYWORD, Keyword.FROM):
        parser.consume(TokenType.KEYWORD, Keyword.FROM)
        inherited_class = types.parse_base_type(parser, current_context)

    # parse contents inside class scope and separate them
    _scope = scope.parse_scope(parser, current_context)
    class_fields = []
    class_methods = []
    static_fields = []
    static_methods = []

    # there are only two possible expressions: fields and methods (object-dependent or static).
    for expression in _scope.statements:
        if isinstance(expression, AST.ClassFieldDeclarationNode):
            if expression.is_static:
                static_fields.append(expression)
            else:
                class_fields.append(expression)
        elif isinstance(expression, AST.ClassMethodDeclarationNode):
            if expression.is_static:
                static_methods.append(expression)
            else:
                class_methods.append(expression)
        elif isinstance(expression, AST.FunctionDefNode):
            static_methods.append(expression)
        else:
            parser.error(
                f"Unexpected expression: {expression.__class__.__name__}\n"
                f"at line {expression.line} position {expression.position}"
            )

    # return instance
    return AST.ClassDefNode(
        class_name=class_name,
        generic_parameters=generic_parameters,
        superclass=inherited_class,
        fields_definitions=class_fields,
        methods_defs=class_methods,
        static_fields_defs=static_fields,
        static_methods_defs=static_methods,
        line=line, position=position,
    )

def parse_generic_parameters(
    parser: Parser,
    mode: Literal["declaration", "instantiation"],
    context: ContextFlag
) -> list[AST.GenericParameterNode | AST.TypeNode]:
    parser.consume(TokenType.OPENING_SQUARE_BRACKET)
    arguments = []

    while parser.current_token.type != TokenType.CLOSING_SQUARE_BRACKET:
        if mode == "declaration":
            identifier = parser.consume(TokenType.IDENTIFIER)
            line, position = parser.line_and_position_of_consumed_token()
            arguments.append(AST.GenericParameterNode(identifier, line, position))
        elif mode == "instantiation":
            arguments.append(types.parse_base_type(parser, context))
        else:
            raise ValueError(f"Unknown mode for parsing generics: {mode}")

        if parser.match(TokenType.CLOSING_SQUARE_BRACKET):
            break
        parser.consume(TokenType.COMMA)

    parser.consume(TokenType.CLOSING_SQUARE_BRACKET)
    return arguments
