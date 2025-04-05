from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag
import frontend.abstract_syntax_tree as AST

from frontend.syntax import Keyword, TokenType, OperatorMethods

from typing import Union, Iterator

import frontend.parser.parse_operators as arith
import frontend.parser.parse_type as types
import frontend.parser.parse_scope as scope

def parse_full_function_definition(parser: Parser, context: ContextFlag) \
        -> Union[AST.FunctionDefNode, AST.ClassMethodDeclarationNode]:
    # scope check: global or class
    if not (
            ContextFlag.strict_match(context, flag=ContextFlag.GLOBAL) or
            ContextFlag.strict_match(context, flag=ContextFlag.CLASS)
    ):
        parser.error("Unexpected non-anonymous function definition in non-global or non-class context.")

    # denote function for inner scopes
    current_context = ContextFlag.add(context, flag=ContextFlag.FUNCTION)

    is_constructor = False
    is_destructor = False
    if parser.match(TokenType.KEYWORD, Keyword.FUNCTION):
        parser.consume(TokenType.KEYWORD, Keyword.FUNCTION)
    elif parser.match(TokenType.KEYWORD, Keyword.CONSTRUCTOR):
        is_constructor = True
        parser.consume(TokenType.KEYWORD, Keyword.CONSTRUCTOR)
    else:
        is_destructor = True
        parser.consume(TokenType.KEYWORD, Keyword.CONSTRUCTOR)
    line, position = parser.line_and_position_of_consumed_token()
    is_constructor_or_destructor = is_constructor or is_destructor

    if is_constructor_or_destructor and not ContextFlag.match(current_context, ContextFlag.CLASS):
        parser.error("Unexpected constructor/destructor definition in global context.")

    return_type = None
    if not is_constructor_or_destructor and parser.match(TokenType.OPENING_SQUARE_BRACKET):
        parser.consume(TokenType.OPENING_SQUARE_BRACKET)
        return_type = types.parse_type_declaration(parser, current_context)
        parser.consume(TokenType.CLOSING_SQUARE_BRACKET)

    is_operator_overload = False
    if not is_constructor_or_destructor and parser.match(TokenType.KEYWORD, Keyword.OPERATOR):
        is_operator_overload = True
        dct = {}
        gen = _parse_operator_overload(parser, dct, current_context)
        next(gen)
        parameters = _parse_function_parameters(parser, current_context)
        dct['n'] = len(parameters)
        function_name = next(gen)
    elif not is_constructor_or_destructor:
        function_name = parser.consume(TokenType.IDENTIFIER)
        parameters = _parse_function_parameters(parser, current_context)
    elif is_destructor:
        function_name = "$destructor"
        parameters = _parse_function_parameters(parser, current_context)
        if len(parameters) > 0:
            parser.error("Destructor cannot have parameters!.")
    else:
        function_name = "$constructor"
        parameters = _parse_function_parameters(parser, current_context)

    function_body = scope.parse_scope(parser, current_context)

    if parser.match(TokenType.END_OF_STATEMENT):
        parser.consume(TokenType.END_OF_STATEMENT)

    if ContextFlag.strict_match(context, flag=ContextFlag.CLASS) and not is_operator_overload:
        return AST.ClassMethodDeclarationNode(
            return_type=return_type,
            function_name=function_name,
            parameters=parameters,
            function_body=function_body,
            is_constructor=is_constructor,
            is_destructor=is_destructor,
            access_type=AST.AccessType.PUBLIC,
            static=False,
            virtual=False,
            overload=False,
            line=line, position=position
        )
    else:
        return AST.FunctionDefNode(
            return_type=return_type, function_name=function_name, parameters=parameters,
            function_body=function_body,
            line=line, position=position
        )

def _parse_function_parameters(parser: Parser, context: ContextFlag) -> list[AST.FunctionParameter]:
    """
    Parse the function parameters declaration expression
    :param context: scope context flag. Should be a function.
    :return: list of function parameters
    """
    parser.consume(TokenType.OPENING_PARENTHESIS)
    parameters = []
    while parser.current_token.type != TokenType.CLOSING_PARENTHESIS:
        type_node = types.parse_type_declaration(parser, context)

        parameter_name = parser.consume(TokenType.IDENTIFIER)
        line, position = parser.line_and_position_of_consumed_token()
        parameters.append(
            AST.FunctionParameter(
                type_=type_node, parameter_name=parameter_name,
                line=line, position=position
            )
        )

        if parser.match(TokenType.COMMA):
            parser.consume(TokenType.COMMA)
    parser.consume(TokenType.CLOSING_PARENTHESIS)
    return parameters

def _parse_operator_overload(parser: Parser, dct: dict, context: ContextFlag) -> Iterator[str]:
    """
    Parses operator overloading declaration and returns mangled function name
    :param context:
    :return:
    """
    if not ContextFlag.match(context, flag=ContextFlag.CLASS):
        parser.error(msg="Invalid place to overload operator behaviour")

    _ = parser.consume(TokenType.KEYWORD, Keyword.OPERATOR)
    if parser.match(TokenType.OPERATOR):
        operator = parser.consume(TokenType.OPERATOR)
        if not OperatorMethods.overloadable(operator):
            parser.error(msg=f"Invalid operator for overload: {operator}")

        yield
        n: int = dct['n']

        yield f"$operator_{OperatorMethods.translate(operator, n)}"
    elif parser.match(TokenType.OPENING_SQUARE_BRACKET):
        _ = parser.consume(TokenType.OPENING_SQUARE_BRACKET)
        _ = parser.consume(TokenType.CLOSING_SQUARE_BRACKET)
        yield
        yield "$operator_index"
    elif parser.match(TokenType.OPENING_PARENTHESIS):
        _ = parser.consume(TokenType.OPENING_PARENTHESIS)
        _ = parser.consume(TokenType.CLOSING_PARENTHESIS)
        yield
        yield "$operator_call"
    else:
        parser.error(msg="Invalid operator to overload")

def parse_full_return_statement(parser: Parser, context: ContextFlag) -> AST.ReturnNode:

    # scope check: functions/methods only
    if not ContextFlag.match(context, flag=ContextFlag.FUNCTION):
        parser.error(msg=f"Unexpected token {parser.current_token.value} out of function or method.")

    parser.consume(TokenType.KEYWORD, Keyword.RETURN)
    line, position = parser.line_and_position_of_consumed_token()

    # return may be a sole keyword, or with some expression
    expression = None
    if not parser.match(TokenType.END_OF_STATEMENT):
        expression = arith.parse_arithmetic_expression(parser, context)
    parser.consume(TokenType.END_OF_STATEMENT)
    return AST.ReturnNode(value=expression, line=line, position=position)
