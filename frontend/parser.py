from tokens import TokenType, Token
from exceptions import ParsingException
from syntax import Operator, Keyword, Assignment, TypeModifier
from semantics import TypeModifierFlag
from typing import Iterator, KeysView, ValuesView
from abstract_syntax_tree import *
from enum import IntFlag


class ContextFlag(IntFlag):
    GLOBAL = 0b0
    LOCAL = 0b1
    CLASS = 0b11
    FUNCTION = 0b101
    LOOP = 0b1001
    IF_CLAUSE = 0b10001
    TRY_CLAUSE = 0b100001
    ANY_EXPRESSION = 0b1000001
    ARITHMETIC_EXPRESSION = 0b11000001
    # BOOLEAN_EXPRESSION = 0b
    # TYPE_DECLARATION = 0b11000001  # TODO: really?

    @staticmethod
    def match(current_context, flag) -> bool:
        if flag == ContextFlag.GLOBAL:
            return current_context == ContextFlag.GLOBAL
        else:
            return (current_context & flag) == flag

    @staticmethod
    def strict_match(current_context, flag) -> bool:
        return current_context == flag

    @staticmethod
    def add(current_context, flag) -> "ContextFlag":
        return current_context | flag


class Parser(object):
    """
    Class for generating an AST tree from a stream of lexical tokens
    """
    def __init__(self, tokens: Iterator[Token]):
        """

        :param tokens: Iterator or generator providing lexical tokens
        """
        self._tokens: Iterator[Token] = tokens

        # we store only prev, current and next tokens
        # as it's enough to make sensible predictions
        self._prev_token: Token | None = None
        self._curr_token: Token | None = next(self._tokens)
        self._next_token: Token | None = next(self._tokens, None)

    @property
    def prev_token(self) -> Token | None:
        return self._prev_token

    @property
    def current_token(self) -> Token | None:
        return self._curr_token

    @property
    def next_token(self) -> Token | None:
        return self._next_token

    def __next__(self) -> None:
        self._prev_token = self._curr_token
        self._curr_token = self._next_token
        self._next_token = next(self._tokens, None)

    def consume(self, expected_type: str, expected_value=None) -> str:
        """
        The crucial method of Parser class.
        Process current token and return the value of it,
        and set the next token as current one.
        It's important to provide the expected type of token that will be consumed,
        and in case of type mismatch, the ParsingException is raised.
        Also, an expected value or list/tuple/set of expected values can be provided
        to check if the consumed token matches the expected value, or if not, the ParsingException is raised.
        :param expected_type: expected token type to match against actual one
        :param expected_value: (optional) expected value or list/tuple/set of expected values
        :return: the value of consumed token
        """
        # store the copy of current token
        token = self.current_token

        # token is passed when
        # 1. expected type matches
        # 2. if expected value or collection of values provided, check the value
        if token.type == expected_type and (
            (expected_value is None) or
            (isinstance(expected_value, str) and expected_value == token.value) or
            (isinstance(expected_value, (tuple, list, set, ValuesView, KeysView)) and token.value in expected_value)
        ):
            self.__next__()
            return token.value
        else:
            # token type mismatch => error
            if token.type != expected_type:
                msg = (f"Expected token of type {expected_type}, "
                       f"but got {token.type}")

            # token value is not among collection of the expected ones => error
            elif isinstance(expected_value, (tuple, list, set, ValuesView, KeysView)):
                msg = (f"Expected token is among these values: {str(expected_value)}, "
                       f"but got {token.type} (Token type {token.type})")

            # only one token value is expected, but got different => error
            else:
                msg = (f"Expected token is {expected_value}, "
                       f"but got {token.type} (Token type {token.type})")
            self.error(msg)

    def error(self, msg: str) -> None:
        """
        Raise an error message, with sufficient information to user
        which token (line and position in the code) is invalid.
        Presumes that the current token is the reason of error.
        :param msg: reason why the error occurred
        :raises: ParsingException
        """
        raise ParsingException(msg, self.current_token.line_number, self.current_token.position)

    def parse(self) -> ProgramNode:
        """
        Parses the code from beginning to end of the file
        To do so, we need to parse all the classes (and their methods), functions and global statements
        we meet in the code.
        :return: parsed AST tree of the program
        """

        class_definitions = []
        function_definitions = []
        statements = []
        while self.current_token.type != TokenType.END_OF_CODE:
            statement = self.parse_statement(ContextFlag.GLOBAL)
            if isinstance(statement, FunctionDeclarationNode):
                function_definitions.append(statement)
            else:
                statements.append(statement)
        return ProgramNode(class_definitions, function_definitions, statements)

    def parse_statement(self, context: ContextFlag) -> ASTNode:
        """
        Parses any complete statement:
            - class, class methods, function definitions,
            - variable declarations,
            - assignments,
            - function/functor/constructor calls, iterables iterations,
            - literals
            - arithmetic operations
            - if/else statements, loops, other keywords
            - scopes

        :param context: Context flag, indicating the current scope of statement
        :return: any AST node if valid, otherwise raises ParsingException
        :raises ParsingException: if the current statement syntax is invalid or some kind of semantics error;
        """
        # NOTE for developers: use only full parsers here
        # e.g. that one that covers all cases of syntax and consumes all required tokens
        # including END_OF_STATEMENT token
        # and here we don't modify context, instead other parsers do it if necessary

        # parse full scope
        if self.current_token.type == TokenType.BEGIN_OF_SCOPE:
            return self.parse_scope(context)

        # parse syntax constructions, related to keyword-beginning statements
        if self.current_token.type == TokenType.KEYWORD:

            # if-elseif-else clause
            if self.current_token.value == Keyword.IF:
                # we never use if-else clauses inside classes definitions and outside methods.
                if ContextFlag.strict_match(context, ContextFlag.CLASS):
                    self.error(
                        "If-else statement is not allowed inside class definition outside of method or constructor."
                    )
                return self.parse_full_if_else_statement(context)

            # while loop
            if self.current_token.value == Keyword.WHILE:
                if ContextFlag.strict_match(context, ContextFlag.CLASS):
                    self.error(
                        "Loops are allowed inside class definition outside of method or constructor."
                    )
                return self.parse_full_while_statement(context)

            # TODO: for, foreach (later)

            # function declaration: only in global or class scope
            if self.current_token.value == Keyword.FUNCTION:
                if (
                    ContextFlag.strict_match(context, ContextFlag.GLOBAL) or
                    ContextFlag.strict_match(context, ContextFlag.CLASS)
                ):
                    return self.parse_full_function_declaration(context)
                else:
                    self.error(f"Unexpected token {self.current_token.value} in non-global context.")

            # return statement, allowed in functions and methods
            if self.current_token.value == Keyword.RETURN:
                if ContextFlag.match(context, ContextFlag.FUNCTION):
                    return self.parse_full_return_statement(context)
                else:
                    self.error(f"Unexpected token {self.current_token.value} out of function or method.")

            if self.current_token.value == Keyword.BREAK:
                if ContextFlag.match(context, ContextFlag.LOOP):
                    # sole keyword that doesn't need context
                    return self.parse_full_break_statement()
                else:
                    self.error(f"Unexpected token {self.current_token.value} out of loop.")

            if self.current_token.value == Keyword.CONTINUE:
                if ContextFlag.match(context, ContextFlag.LOOP):
                    # sole keyword that doesn't need context
                    return self.parse_full_continue_statement()
                else:
                    self.error(f"Unexpected token {self.current_token.value} out of loop.")

        # if statement begins with type
        if self.current_token.type in (TokenType.SIMPLE_TYPE, TokenType.COMPOUND_TYPE, TokenType.TYPE_MODIFIER):
            return self.parse_full_variable_declaration(context)

        if self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_full_statement_beginning_with_identifier(context)

        return self.parse_full_expression(context)

    def parse_full_statement_beginning_with_identifier(self, context: ContextFlag):
        # TODO: context
        if self.next_token.type == TokenType.IDENTIFIER:
            return self.parse_full_variable_declaration(context)
        elif self.next_token.type == TokenType.GENERIC_ASSIGNMENT:
            return self.parse_full_expression(context)
        else:
            return self.parse_full_expression(context, possibly_type=True)

    def parse_scope(self, context: ContextFlag) -> ScopeNode:

        # modify context to disallow class and function definitions
        current_context = ContextFlag.add(context, ContextFlag.LOCAL)

        self.consume(TokenType.BEGIN_OF_SCOPE)
        statements = []
        local_variables = []

        met_finalizer = False

        while self.current_token.type != TokenType.END_OF_SCOPE:
            statement = self.parse_statement(current_context)

            # if parser did meet return or throw,
            # don't include further syntax bullshit into AST
            if not met_finalizer:
                statements.append(statement)
            if isinstance(statement, VariableDeclarationNode):
                local_variables.append(statement)
            if isinstance(statement, (ReturnNode, ContinueNode, BreakNode)):
                met_finalizer = True

        self.consume(TokenType.END_OF_SCOPE)
        return ScopeNode(statements, local_variables, )

    def parse_full_if_else_statement(self, context: ContextFlag):
        current_context = ContextFlag.add(context, ContextFlag.IF_CLAUSE)

        self.consume(TokenType.KEYWORD, Keyword.IF)
        condition = self._parse_condition(current_context)
        if_scope = self.parse_scope(current_context)

        root_node = IfElseNode(condition, if_scope, None)
        current_node = root_node

        while self.current_token.type == TokenType.KEYWORD and self.current_token.value == Keyword.ELSE:
            self.consume(TokenType.KEYWORD, Keyword.ELSE)

            if self.current_token.type == TokenType.KEYWORD and self.current_token.value == Keyword.IF:
                # Handle "else if" condition
                self.consume(TokenType.KEYWORD, Keyword.IF)
                elif_condition = self._parse_condition(current_context)
                elif_scope = self.parse_scope(current_context)

                obj = IfElseNode(elif_condition, elif_scope, None)
                current_node.else_node = obj
                current_node = obj
            else:
                # Handle Keyword.ELSE block
                current_node.else_scope = self.parse_scope(current_context)

        if self.current_token.type == TokenType.END_OF_STATEMENT:
            self.consume(TokenType.END_OF_STATEMENT)
        return root_node

    def _parse_condition(self, context: ContextFlag) -> ASTNode:
        # TODO: context
        self.consume(TokenType.OPENING_PARENTHESIS)
        condition = self.parse_arithmetic_expression(context)
        self.consume(TokenType.CLOSING_PARENTHESIS)
        return condition

    def parse_full_while_statement(self, context: ContextFlag) -> WhileNode:

        # modify context to allow BREAK and CONTINUE expressions
        current_context = ContextFlag.add(context, ContextFlag.LOOP)

        self.consume(TokenType.KEYWORD, Keyword.WHILE)
        condition = self._parse_condition(current_context)
        while_scope = self.parse_scope(current_context)
        if self.current_token.type == TokenType.END_OF_STATEMENT:
            self.consume(TokenType.END_OF_STATEMENT)
        return WhileNode(condition, while_scope)

    def parse_full_break_statement(self) -> BreakNode:
        """
        Parses the break keyword statement.
        Doesn't modify the current context.
        Allowed only in loops (for now).
        :return: BreakNode instance
        """
        self.consume(TokenType.KEYWORD, Keyword.BREAK)
        self.consume(TokenType.END_OF_STATEMENT)
        return BreakNode()

    def parse_full_continue_statement(self) -> ContinueNode:
        """
        Parses the continue keyword statement.
        Doesn't modify the current context.
        Allowed only in loops.
        :return: ContinueNode instance
        """
        self.consume(TokenType.KEYWORD, Keyword.CONTINUE)
        self.consume(TokenType.END_OF_STATEMENT)
        return ContinueNode()

    # FUNCTION DECLARATION
    def parse_full_function_declaration(self, context: ContextFlag) -> FunctionDeclarationNode:
        current_context = ContextFlag.add(context, ContextFlag.FUNCTION)

        self.consume(TokenType.KEYWORD, Keyword.FUNCTION)

        return_type = None
        if self.current_token.type == TokenType.OPENING_SQUARE_BRACKET:
            self.consume(TokenType.OPENING_SQUARE_BRACKET)
            return_type = self.parse_type_declaration(current_context)
            self.consume(TokenType.CLOSING_SQUARE_BRACKET)

        function_name = self.consume(TokenType.IDENTIFIER)

        parameters = self._parse_function_parameters(current_context)
        function_body = self.parse_scope(current_context)

        if self.current_token.type == TokenType.END_OF_STATEMENT:
            self.consume(TokenType.END_OF_STATEMENT)

        return FunctionDeclarationNode(return_type, function_name, parameters, function_body)

    def _parse_function_parameters(self, context: ContextFlag) -> list[FunctionParameter]:
        # TODO: context
        self.consume(TokenType.OPENING_PARENTHESIS)
        parameters = []
        while self.current_token.type != TokenType.CLOSING_PARENTHESIS:
            type_node = self.parse_type_declaration(context)

            parameter_name = self.consume(TokenType.IDENTIFIER)

            default_value = None
            operator_type = None
            if self.current_token.type == TokenType.GENERIC_ASSIGNMENT:

                operator_type = self.consume(
                    TokenType.GENERIC_ASSIGNMENT,
                    (Assignment.VALUE_ASSIGNMENT, Assignment.REFERENCE_ASSIGNMENT)
                )
                default_value = self.parse_arithmetic_expression(context)

            parameters.append(FunctionParameter(type_node, parameter_name, operator_type, default_value))

            if self.current_token.type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
        self.consume(TokenType.CLOSING_PARENTHESIS)
        return parameters

    def parse_full_return_statement(self, context: ContextFlag) -> ReturnNode:
        self.consume(TokenType.KEYWORD, Keyword.RETURN)
        expression = self.parse_arithmetic_expression(context)
        self.consume(TokenType.END_OF_STATEMENT)
        return ReturnNode(expression)

    # TODO: try-catch-else-finally, keyword recognition
    # TODO: for, class declaration, class methods
    # TODO: slices, better keymap declaration
    def parse_full_variable_declaration(self, context: ContextFlag):
        # TODO: context
        type_node = self.parse_type_declaration(context)
        return self._parse_partial_variable_expression(type_node, context)

    def _parse_partial_variable_expression(self, type_node: ASTNode, context: ContextFlag):
        # TODO: context
        identifier = self.consume(TokenType.IDENTIFIER)

        if self.current_token.type == TokenType.GENERIC_ASSIGNMENT:
            operator = self.consume(TokenType.GENERIC_ASSIGNMENT)
            expression_node = self.parse_assignment_expression(context)
            result = VariableDeclarationNode(type_node, identifier, operator, expression_node)
        else:
            result = VariableDeclarationNode(type_node, identifier, None, TokenType.UNDEFINED_LITERAL)

        self.consume(TokenType.END_OF_STATEMENT)
        return result

    def parse_full_expression(self, context, **kwargs):
        # TODO: context
        result = self.parse_assignment_expression(context, **kwargs)
        if kwargs.get("possibly_type") and self.current_token.type == TokenType.IDENTIFIER:
            return self._parse_partial_variable_expression(result, context)
        self.consume(TokenType.END_OF_STATEMENT)
        return result

    # TODO: nodes
    def parse_type_declaration(self, context: ContextFlag):
        # TODO: context
        # Check for const or reference modifiers
        modifiers = []
        while self.current_token.type == TokenType.TYPE_MODIFIER:
            modifiers.append(self.consume(TokenType.TYPE_MODIFIER, TypeModifier.values()))

        # Parse the base type (simple or compound)
        base_type = self.parse_base_type(context)

        # Apply modifiers to the base type
        for modifier in modifiers:
            match modifier:
                case TypeModifier.CONST:
                    base_type.add_flag(TypeModifierFlag.CONSTANT)
                case TypeModifier.NULLABLE:
                    base_type.add_flag(TypeModifierFlag.NULLABLE)
                case TypeModifier.REFERENCE:
                    base_type.add_flag(TypeModifierFlag.REFERENCE)

        return base_type

    # TODO: better generic parsing
    def parse_base_type(self, context: ContextFlag) -> TypeNode:
        # TODO: context
        if self.current_token.type == TokenType.SIMPLE_TYPE:
            type_name = self.consume(TokenType.SIMPLE_TYPE)
            return SimpleTypeNode(type_name)

        elif self.current_token.type == TokenType.COMPOUND_TYPE:
            return self.parse_compound_types(context=context)

        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_identifier(context=context, is_type=True)

        else:
            self.error("Invalid type declaration")

    def parse_compound_types(self, context: ContextFlag) -> CompoundTypeNode:
        compound_type = self.consume(TokenType.COMPOUND_TYPE)

        parameters = []
        if self.current_token.type == TokenType.OPENING_SQUARE_BRACKET:
            parameters = self.__parse_square_bracket_content(allow_keymap_or_slice=False, context=context)

        return CompoundTypeNode(compound_type, parameters)

    def parse_arithmetic_expression(self, context: ContextFlag, **kwargs):
        return self.parse_logical_or_expression(context, **kwargs)

    def parse_assignment_expression(self, context: ContextFlag, **kwargs) -> AssignmentNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 0 (lowest)
        Associativity: right to left
        Tokens:
            :=, =,
            +=, -=, *=, /=, //=, %=, **=,
            ^=, &=, |=, >>=, <<=,
        Parses the assignment chain expression.

        :return: Assignment node if assignment is present,
        otherwise anything the primary parser will return.
        """
        # TODO: context
        left_expr = self.parse_logical_or_expression(context, **kwargs)

        while self.current_token.type == TokenType.GENERIC_ASSIGNMENT:
            operator = self.consume(TokenType.GENERIC_ASSIGNMENT)
            right_expr = self.parse_logical_or_expression(context, **kwargs)
            left_expr = AssignmentNode(left_expr, operator, right_expr)

        return left_expr

    def parse_logical_or_expression(self, context: ContextFlag, **kwargs) -> LogicalOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 1 (low)
        Associativity: left to right
        Tokens: ||, or
        :return: Logical operator node if disjunction is present,
        otherwise anything the next precedence (logical xor) parser will return.
        """
        left = self.parse_logical_xor_expression(context, **kwargs)

        while self.current_token.value in (Operator.OR, Operator.FULL_OR):
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_logical_xor_expression(context, **kwargs)
            left = LogicalOperatorNode(left=left, operator=operator, right=right)

        return left

    def parse_logical_xor_expression(self, context: ContextFlag, **kwargs) -> LogicalOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 2 (low)
        Associativity: left to right
        Tokens: ^^, xor
        :return: Logical operator node if exclusive disjunction (addition by modulo 2) is present,
        otherwise anything the next precedence (logical and) parser will return.
        """
        left = self.parse_logical_and_expression(context, **kwargs)

        while self.current_token.value in (Operator.XOR, Operator.FULL_XOR):
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_logical_and_expression(context, **kwargs)
            left = LogicalOperatorNode(left=left, operator=operator, right=right)

        return left

    def parse_logical_and_expression(self, context: ContextFlag, **kwargs) -> LogicalOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 3 (low)
        Associativity: left to right
        Tokens: &&, and
        :return: Logical operator node if conjunction is present,
        otherwise anything the next precedence (bitwise or) parser will return.
        """
        left = self.parse_bitwise_or_expression(context, **kwargs)

        while self.current_token.value in (Operator.AND, Operator.FULL_AND):
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_bitwise_or_expression(context, **kwargs)
            left = LogicalOperatorNode(left=left, operator=operator, right=right)

        return left

    def parse_bitwise_or_expression(self, context: ContextFlag, **kwargs) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 4 (low-medium)
        Associativity: left to right
        Tokens: |
        :return: Arithmetic operator node if bitwise disjunction is present,
        otherwise anything the next precedence (bitwise xor) parser will return.
        """
        left = self.parse_bitwise_xor_expression(context, **kwargs)

        while self.current_token.value == Operator.BITWISE_OR:
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_bitwise_xor_expression(context, **kwargs)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right)

        return left

    def parse_bitwise_xor_expression(self, context: ContextFlag, **kwargs) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 5 (low-medium)
        Associativity: left to right
        Tokens: ^
        :return: Arithmetic operator node if bitwise exclusive disjunction (addition by modulo 2) is present,
        otherwise anything the next precedence (bitwise and) parser will return.
        """
        left = self.parse_bitwise_and_expression(context, **kwargs)

        while self.current_token.value == Operator.BITWISE_XOR:
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_bitwise_and_expression(context, **kwargs)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right)

        return left

    def parse_bitwise_and_expression(self, context: ContextFlag, **kwargs) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 6 (low-medium)
        Associativity: left to right
        Tokens: &
        :return: Arithmetic operator node if bitwise conjunction is present,
        otherwise anything the next precedence (equality operators) parser will return.
        """
        left = self.parse_equality_expression(context, **kwargs)

        while self.current_token.value == Operator.BITWISE_AND:
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_equality_expression(context, **kwargs)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right)

        return left

    def parse_equality_expression(self, context: ContextFlag, **kwargs) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 7 (medium)
        Associativity: right to left (with logical "and" proxy)
        Tokens: ==, !=, ===, !==
        :return: Comparison operator node if one operator is present,
        or logical operator node ("and") if it's the chain of these operators
        otherwise anything the next precedence (comparison operators) parser will return.
        """
        left = self.parse_comparison_expression(context, **kwargs)

        statements = []
        while self.current_token.value in (
            Operator.EQUAL,
            Operator.NOT_EQUAL,
            Operator.STRICT_EQUAL,
            Operator.NOT_STRICT_EQUAL
        ):

            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_comparison_expression(context, **kwargs)

            statements.append(ComparisonNode(left=left, operator=operator, right=right))
            left = right

        if not statements:
            return left
        return self.__parse_chained_comparisons(statements)

    def parse_comparison_expression(self, context: ContextFlag, **kwargs) \
            -> ComparisonNode | LogicalOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 8 (medium)
        Associativity: right to left (with logical "and" proxy)
        Tokens: >, >=, <, <=
        :return: Comparison operator node if one operator is present,
        or logical operator node ("and") if it's the chain of these operators
        otherwise anything the next precedence (bitwise shift operators) parser will return.
        """

        statements = []
        left = self.parse_bitwise_shift_expression(context, **kwargs)

        while self.current_token.value in (
            Operator.LESSER_OR_EQUAL,
            Operator.GREATER_OR_EQUAL,
            Operator.LESSER,
            Operator.GREATER
        ):
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_bitwise_shift_expression(context, **kwargs)

            statements.append(ComparisonNode(left=left, operator=operator, right=right))
            left = right

        if not statements:
            return left
        return self.__parse_chained_comparisons(statements)

    @staticmethod
    def __parse_chained_comparisons(statements: list[ComparisonNode]) -> ComparisonNode | LogicalOperatorNode:
        r"""
        (Helper)
        Parse the chain of comparisons as the "and"-operator based AST tree
        with right-to-left associativity (right branch is more "leafy")
        e.g.
        a == b == c == d is translated as ((a == b) and ((b == c) and (c == d)))
                 and
              /      \
            ==       and
           |  \    /     \
           a  b   ==      ==
                 /  \    |  \
                b    c   c   d
        :return: Comparison operator is that's only one, or else Logical operator based tree
        """
        if len(statements) == 1:
            return statements[0]

        statements_count = len(statements)
        root = LogicalOperatorNode(left=statements[0], operator=Operator.AND, right=None)  # type: ignore
        curr = root
        for index, statement in enumerate(statements):
            if index == 0:
                continue
            elif index != statements_count - 1:
                new_node = LogicalOperatorNode(left=statement, operator=Operator.AND, right=None)  # type: ignore
                curr.right = new_node
                curr = new_node
            else:
                curr.right = statement
        return root

    def parse_bitwise_shift_expression(self, context: ContextFlag, **kwargs) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 9 (upper-medium)
        Associativity: left-to-right
        Tokens: >>, <<
        :return: Arithmetic operator node if bitwise shift operators are present,
        otherwise anything the next precedence (additive operators) parser will return.
        """
        left = self.parse_additive_expression(context, **kwargs)

        while self.current_token.value in (Operator.BITWISE_LSHIFT, Operator.BITWISE_RSHIFT):
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_additive_expression(context, **kwargs)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right)

        return left

    def parse_additive_expression(self, context: ContextFlag, **kwargs) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 10 (upper-medium)
        Associativity: left-to-right
        Tokens: +, -
        :return: Arithmetic operator node if additive operators are present,
        otherwise anything the next precedence (multiplicative operators) parser will return.
        """
        left = self.parse_multiplicative_expression(context, **kwargs)

        while self.current_token.value in (Operator.PLUS, Operator.MINUS):
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_multiplicative_expression(context, **kwargs)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right)

        return left

    def parse_multiplicative_expression(self, context: ContextFlag, **kwargs) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 11 (upper)
        Associativity: left-to-right
        Tokens: *, /, %, //
        :return: Arithmetic operator node if multiplicative operators are present,
        otherwise anything the next precedence (unary sign operator) parser will return.
        """
        left = self.parse_arithmetic_unary_expression(context, **kwargs)

        while self.current_token.value in (Operator.MULTIPLY, Operator.DIVIDE, Operator.FLOOR_DIVIDE, Operator.MODULO):
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_arithmetic_unary_expression(context, **kwargs)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right)

        return left

    def parse_arithmetic_unary_expression(self, context: ContextFlag, **kwargs):
        """
        Operator parser.
        Operator type: unary
        Precedence: 12 (upper)
        Associativity: right to left
        Tokens: +, -, ~
        :return: Unary operator node if multiplicative unary operators are present,
        otherwise anything the next precedence (power operator) parser will return.
        """
        if self.current_token.value in (Operator.PLUS, Operator.MINUS, Operator.BITWISE_INVERSE):
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_power_expression(context, **kwargs)
            return UnaryOperatorNode(operator=operator, expression=right)
        else:
            return self.parse_power_expression(context, **kwargs)

    def parse_power_expression(self, context: ContextFlag, **kwargs):
        """
        Operator parser.
        Operator type: binary
        Precedence: 13 (upper)
        Associativity: right to left
        Tokens: **
        :return: Arithmetic operator node if power operators are present,
        otherwise anything the next precedence (other unary) parser will return.
        """
        left = self.parse_other_unary_expression(context, **kwargs)
        right_expressions = [left]

        while self.current_token.value == Operator.POWER:
            _ = self.consume(TokenType.OPERATOR)
            right = self.parse_other_unary_expression(context, **kwargs)
            right_expressions.append(right)

        if len(right_expressions) == 1:
            return left

        result = ArithmeticOperatorNode(
            left=right_expressions[-2], operator=Operator.POWER, right=right_expressions[-1]
        )
        for _left in reversed(right_expressions[:-2]):
            result = ArithmeticOperatorNode(
                left=_left, operator=Operator.POWER, right=result
            )

        return result

    def parse_other_unary_expression(self, context: ContextFlag, **kwargs):
        """
        Operator parser.
        Operator type: unary
        Precedence: 14 (high)
        Associativity: right to left
        Tokens: not, [reference, dereference]
        :return: Unary operator node if other unary operators (logical not, reference operators) are present,
        otherwise anything the next precedence (dynamic memory allocation) parser will return.
        """
        if self.current_token.value == Operator.NOT:
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_dynamic_memory_allocation(context, **kwargs)
            return UnaryOperatorNode(operator=operator, expression=right)
        else:
            return self.parse_dynamic_memory_allocation(context, **kwargs)

    def parse_dynamic_memory_allocation(self, context: ContextFlag, **kwargs):
        """
        Operator parser.
        Operator type: unary
        Precedence: 15 (high)
        Associativity: none (non-stackable)
        Tokens: new, delete
        :return: Allocation operator node if other unary operators dynamic memory allocation are present,
        otherwise anything the next precedence (member access) parser will return.
        """
        if self.current_token.value in (Operator.NEW_INSTANCE, Operator.DELETE_INSTANCE):
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_type_declaration(context)  # TODO: check
            return AllocationOperatorNode(operator=operator, expression=right)
        else:
            return self.parse_member_access(context, **kwargs)

    def parse_member_access(self, context: ContextFlag, **kwargs):
        """
        Operator parser.
        Operator type: binary
        Precedence: 16 (highest)
        Associativity: left to right
        Tokens: . ->
        :return: Member operator node if class member operators are present,
        otherwise anything the primary parser will return.
        """
        left = self.parse_primary_expression(context, **kwargs)

        while self.current_token.value in (Operator.OBJECT_MEMBER_ACCESS, Operator.REFERENCE_MEMBER_ACCESS):
            operator = self.consume(TokenType.OPERATOR)
            right = self.parse_primary_expression(context, **kwargs)
            left = MemberOperatorNode(left=left, operator=operator, right=right)
        return left

    def parse_primary_expression(self, context: ContextFlag, **kwargs):
        # TODO: context
        if self.current_token.type == TokenType.DECIMAL_INTEGER_LITERAL:
            return IntegerLiteralNode(value=self.consume(TokenType.DECIMAL_INTEGER_LITERAL), base=10)

        if self.current_token.type == TokenType.HEXADECIMAL_INTEGER_LITERAL:
            return IntegerLiteralNode(value=self.consume(TokenType.HEXADECIMAL_INTEGER_LITERAL), base=16)

        if self.current_token.type == TokenType.OCTAL_INTEGER_LITERAL:
            return IntegerLiteralNode(value=self.consume(TokenType.OCTAL_INTEGER_LITERAL), base=8)

        if self.current_token.type == TokenType.BINARY_INTEGER_LITERAL:
            return IntegerLiteralNode(value=self.consume(TokenType.BINARY_INTEGER_LITERAL), base=2)

        if self.current_token.type == TokenType.IMAGINARY_FLOAT_LITERAL:
            return ImaginaryFloatLiteralNode(value=self.consume(TokenType.IMAGINARY_FLOAT_LITERAL))

        if self.current_token.type == TokenType.FLOAT_LITERAL:
            return FloatLiteralNode(value=self.consume(TokenType.FLOAT_LITERAL))

        if self.current_token.type == TokenType.OPERATOR and self.current_token.value == Operator.DEDUCTION:
            self.consume(TokenType.OPERATOR, Operator.DEDUCTION)
            return DeductionNode()

        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_identifier(context, **kwargs)

        elif self.current_token.type == TokenType.STRING_LITERAL:
            value = self.consume(TokenType.STRING_LITERAL)
            return StringLiteralNode(value)

        elif self.current_token.type == TokenType.CHAR_LITERAL:
            value = self.consume(TokenType.CHAR_LITERAL)
            return CharLiteralNode(value)

        elif self.current_token.type == TokenType.BOOLEAN_LITERAL:
            value = self.consume(TokenType.BOOLEAN_LITERAL)
            return BooleanLiteralNode(value)

        elif self.current_token.type == TokenType.NULL_LITERAL:
            _ = self.consume(TokenType.NULL_LITERAL)
            return NullLiteralNode()

        elif self.current_token.type == TokenType.UNDEFINED_LITERAL:
            _ = self.consume(TokenType.UNDEFINED_LITERAL)
            return UndefinedLiteralNode()

        elif self.current_token.type == TokenType.BYTE_LITERAL:
            value = self.consume(TokenType.BYTE_LITERAL)
            return ByteLiteralNode(value)

        elif self.current_token.type == TokenType.BYTE_STRING_LITERAL:
            value = self.consume(TokenType.BYTE_STRING_LITERAL)
            return ByteStringLiteralNode(value)

        elif self.current_token.type == TokenType.OPENING_PARENTHESIS:
            self.consume(TokenType.OPENING_PARENTHESIS)
            node = self.parse_arithmetic_expression(context)
            self.consume(TokenType.CLOSING_PARENTHESIS)
            return node
        elif self.current_token.type == TokenType.OPENING_SQUARE_BRACKET:
            return self.parse_square_bracket_literal_expression(context)

        elif self.current_token.type in (TokenType.SIMPLE_TYPE, TokenType.COMPOUND_TYPE, TokenType.TYPE_MODIFIER):
            return self.parse_type_declaration(context)

        else:
            self.error(f"Unexpected token {self.current_token}")
            pass

    def parse_identifier(self, context: ContextFlag, **kwargs) \
            -> IdentifierNode | UserDefinedTypeNode | TemporaryIdentifierNode:
        """
        Parse an identifier
        It can be a label to some variable, function or even class

        The next token can be the parenthesis or square bracket expression

        :param context:
        :param kwargs: consumes 'is_type' and 'possibly_type'
        :return:
        """
        identifier = self.consume(TokenType.IDENTIFIER)
        if kwargs.get('is_type'):
            kwargs.pop('is_type', None)
            previous_result = UserDefinedTypeNode(identifier)
        elif kwargs.get('possibly_type'):
            kwargs.pop('possibly_type', None)
            previous_result = TemporaryIdentifierNode(identifier)
        else:
            previous_result = IdentifierNode(identifier)
        return self._parse_indexation_or_function_calls_if_exist(previous_result, context)

    def _parse_indexation_or_function_calls_if_exist(self, node, context: ContextFlag):
        token = self.current_token
        if token.type == TokenType.OPENING_SQUARE_BRACKET:
            return self._parse_indexation_call(node, context)
        elif token.type == TokenType.OPENING_PARENTHESIS:
            return self._parse_function_call(node, context)
        else:
            return node

    def _parse_function_call(self, identifier, context: ContextFlag):
        arguments = self.__parse_parentheses_content(context)
        # TODO: constructors
        # if isinstance(identifier, UserDefinedTypeNode):
        #     self.error(f"Unexpected token {self.current_token}")
        result = FunctionCallNode(identifier, arguments)
        return self._parse_indexation_or_function_calls_if_exist(result, context)

    def _parse_indexation_call(self, identifier, context: ContextFlag):
        # TODO: context
        arguments = self.__parse_square_bracket_content(allow_keymap_or_slice=True, context=context)
        if isinstance(identifier, UserDefinedTypeNode):
            result = CompoundTypeNode(identifier, arguments)
        elif isinstance(identifier, TemporaryIdentifierNode):
            if self.current_token.type == TokenType.IDENTIFIER:
                identifier = UserDefinedTypeNode.from_temporary(identifier)
                result = CompoundTypeNode(identifier, arguments)

            # TODO: parsing nested generics
            else:
                result = IndexNode(identifier, arguments)
        else:
            result = IndexNode(identifier, arguments)
        return self._parse_indexation_or_function_calls_if_exist(result, context)

    def __parse_square_bracket_content(self, allow_keymap_or_slice: bool, context: ContextFlag) -> list[ASTNode]:
        # TODO: context
        self.consume(TokenType.OPENING_SQUARE_BRACKET)
        arguments = []

        while self.current_token.type != TokenType.CLOSING_SQUARE_BRACKET:
            if allow_keymap_or_slice:
                argument = self.parse_arithmetic_expression_with_keymaps(context)
            else:
                argument = self.parse_arithmetic_expression(context)
            arguments.append(argument)

            if self.current_token.type == TokenType.CLOSING_SQUARE_BRACKET:
                break
            self.consume(TokenType.COMMA)

        self.consume(TokenType.CLOSING_SQUARE_BRACKET)
        return arguments

    def __parse_parentheses_content(self, context: ContextFlag) -> list[ASTNode]:
        # TODO: context
        self.consume(TokenType.OPENING_PARENTHESIS)
        arguments = []

        while self.current_token.type != TokenType.CLOSING_PARENTHESIS:
            argument = self.parse_arithmetic_expression(context)
            arguments.append(argument)

            if self.current_token.type == TokenType.CLOSING_PARENTHESIS:
                break
            self.consume(TokenType.COMMA)

        self.consume(TokenType.CLOSING_PARENTHESIS)
        return arguments

    def parse_square_bracket_literal_expression(self, context: ContextFlag) -> ListLiteralNode:
        # TODO: context
        arguments = self.__parse_square_bracket_content(allow_keymap_or_slice=True, context=context)
        return ListLiteralNode(arguments)

    def parse_arithmetic_expression_with_keymaps(self, context: ContextFlag):
        # TODO: context
        # right-to-left associativity
        left = self.parse_arithmetic_expression(context)

        right_expressions = [left]
        while self.current_token.value == Operator.KEYMAP_LITERAL:
            self.consume(TokenType.OPERATOR)
            right = self.parse_arithmetic_expression(context)
            right_expressions.append(right)

        if len(right_expressions) == 1:
            return left

        result = BinaryOperatorNode(
            left=right_expressions[-2], operator=Operator.KEYMAP_LITERAL, right=right_expressions[-1]
        )
        for _left in reversed(right_expressions[:-2]):
            result = BinaryOperatorNode(
                left=_left, operator=Operator.KEYMAP_LITERAL, right=result
            )

        return result
