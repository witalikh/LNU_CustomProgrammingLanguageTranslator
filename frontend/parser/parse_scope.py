from frontend.parser.parser import Parser
from frontend.parser.context_flag import ContextFlag
import frontend.abstract_syntax_tree as AST

from frontend.syntax import TokenType

import frontend.parser.parse_statement as stmt


def parse_scope(parser: Parser, context: ContextFlag) -> AST.ScopeNode:
    current_context = ContextFlag.add(context, ContextFlag.LOCAL)

    parser.consume(TokenType.BEGIN_OF_SCOPE)
    line, position = parser.line_and_position_of_consumed_token()

    statements = []
    local_variables = []

    while parser.current_token.type != TokenType.END_OF_SCOPE:
        statement = stmt.parse_statement(parser, current_context)

        statements.append(statement)
        if isinstance(statement, AST.VariableDeclarationNode):
            local_variables.append(statement)

    parser.consume(TokenType.END_OF_SCOPE)
    return AST.ScopeNode(statements, local_variables, line, position)