from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag

import frontend.abstract_syntax_tree as AST

from frontend.syntax import TokenType

import frontend.parser.parse_statement as stmt


def parse(parser: Parser) -> AST.ProgramNode:

    class_definitions = []
    function_definitions = []
    statements = []

    while parser.current_token.type != TokenType.END_OF_CODE:
        statement = stmt.parse_statement(parser, ContextFlag.GLOBAL)
        if isinstance(statement, AST.ClassDefNode):
            operator_overloads = list(
                filter(
                    lambda node: isinstance(node, AST.FunctionDefNode),
                    statement.static_methods_defs
                )
            )
            other_static = list(
                filter(
                    lambda node: not isinstance(node, AST.FunctionDefNode),
                    statement.static_methods_defs
                )
            )
            for overload in operator_overloads:
                overload.external_to = statement
            statement.static_methods_defs = other_static
            function_definitions.extend(operator_overloads)
            class_definitions.append(statement)
        elif isinstance(statement, AST.FunctionDefNode):
            function_definitions.append(statement)
        else:
            statements.append(statement)
    return AST.ProgramNode(class_definitions, function_definitions, statements)