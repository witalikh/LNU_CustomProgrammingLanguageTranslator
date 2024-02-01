from enum import IntFlag

from abstract_syntax_tree import *
from exceptions import ParsingException
from syntax import Operator, Keyword, Assignment, TypeModifier, ClassModifierKeyword, Operands
from tokens import TokenType, Token
from typing import Iterator, KeysView, ValuesView, NoReturn, Literal


class ContextFlag(IntFlag):
    """
    Class indicating scope context.
    Useful when parsing keywords or statements that are exclusive to some kind of scope.
    """
    GLOBAL = 0b0
    LOCAL = 0b1
    CLASS = 0b11
    FUNCTION = 0b101
    LOOP = 0b1001

    @staticmethod
    def match(current_context, flag) -> bool:
        """
        Check if the context has the given flag.
        E.g. if the keyword should be exclusively in the loop, but the loop itself can be in the function or method
        :param current_context: the context to check
        :param flag: the flag that should be contained in the context
        :return: boolean indicating if the flag is contained in the current context
        """
        if flag == ContextFlag.GLOBAL:
            return current_context == ContextFlag.GLOBAL
        else:
            return (current_context & flag) == flag

    @staticmethod
    def strict_match(current_context, flag) -> bool:
        """
        Check if the current context is strictly equal the given flag.
        E.g. if keyword should be in class scope, but not inside method
        :param current_context: the context to check
        :param flag: the flag the context should equal
        :return: boolean indicating whether context and flag are equal
        """
        return current_context == flag

    @staticmethod
    def add(current_context, flag) -> "ContextFlag":
        """
        Add the given flag to the scope context
        :param current_context: current scope context
        :param flag: flag to add
        :return: modified scope context
        """
        return current_context | flag


class Parser(object):
    """
    Class for generating an AST tree from a stream of lexical tokens
    """
    def __init__(self, tokens: Iterator[Token]):
        """
        Initialize the AST parser
        :param tokens: Iterator or generator providing lexical tokens
        """
        self._tokens = tokens

        # we store only prev, current and next tokens
        # as it's enough to make sensible predictions
        self._prev_token: Token | None = None
        self._curr_token: Token | None = next(self._tokens)
        self._next_token: Token | None = next(self._tokens, None)

    @property
    def prev_token(self) -> Token | None:
        """
        Returns the previous token that was previously consumed by the parser
        or None if no token was consumed yet
        """
        return self._prev_token

    @property
    def current_token(self) -> Token | None:
        """
        Returns the current token the parser is pointing at, and it's not consumed yet
        or None if the last token is recently consumed
        """
        return self._curr_token

    @property
    def next_token(self) -> Token | None:
        """ Returns the next token that is next to the current token
        or None if the parser is at the end of the token stream
        """
        return self._next_token

    def __next__(self) -> None:
        """
        Iterate through the token stream and update the previous, current and next tokens
        """
        self._prev_token = self._curr_token
        self._curr_token = self._next_token
        self._next_token = next(self._tokens, None)

    def consume(self, expected_type: str, expected_value=None) -> str:
        """
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
        token = self._curr_token

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

    def is_consumable(self, expected_type, expected_value=None) -> bool:
        """
        Checks if the current token might be consumed without raising an exception.
        :param expected_type: TokenType or collection of TokenTypes to match within them
        :param expected_value: (optional) possible token value or collection of values to match within them
        :return: boolean indicating if current token might be consumed
        """
        if isinstance(expected_type, str):
            suitable_type = self._curr_token.type == expected_type
        elif isinstance(expected_type, (list, tuple, set, ValuesView, KeysView)):
            suitable_type = self._curr_token.type in expected_type
        else:
            return False

        if not suitable_type:
            return False

        if expected_value is None:
            return True
        elif isinstance(expected_value, str):
            return self._curr_token.value == expected_value
        elif isinstance(expected_value, (tuple, list, set, ValuesView, KeysView)):
            return self._curr_token.value in expected_value
        else:
            return False

    def line_and_position_of_consumed_token(self) -> tuple[int, int]:
        """
        Returns the line and position of the recently consumed token.
        Useful for debugging purposes.
        :return: line and position of the recently consumed token
        """
        return self._prev_token.line_number, self._prev_token.position

    def error(self, msg: str) -> NoReturn:
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
        # NOTE for developers: use only full parsers here. All logic is only there!
        # e.g. that one that covers all cases of syntax and consumes all required tokens
        # including END_OF_STATEMENT token
        # and here we don't modify context, instead other parsers do it if necessary

        # parse full scope
        if self.is_consumable(TokenType.BEGIN_OF_SCOPE):
            return self.parse_scope(context)

        # if-elseif-else clause
        if self.is_consumable(TokenType.KEYWORD, Keyword.IF):
            return self.parse_full_if_else_statement(context)

        # while loop
        if self.is_consumable(TokenType.KEYWORD, Keyword.WHILE):
            return self.parse_full_while_statement(context)

        # class definition
        if self.is_consumable(TokenType.KEYWORD, Keyword.CLASS):
            return self.parse_full_class_definition(context)

        # function definition
        if self.is_consumable(TokenType.KEYWORD, Keyword.FUNCTION):
            return self.parse_full_function_definition(context)

        # return statement
        if self.is_consumable(TokenType.KEYWORD, Keyword.RETURN):
            return self.parse_full_return_statement(context)

        # break
        if self.is_consumable(TokenType.KEYWORD, Keyword.BREAK):
            return self.parse_full_break_statement(context)

        # continue
        if self.is_consumable(TokenType.KEYWORD, Keyword.CONTINUE):
            return self.parse_full_continue_statement(context)

        if self.is_consumable(TokenType.CLASS_KEYWORD):
            return self.parse_full_class_keywords(context)

        # statement begins with built-in type or modified user-defined type
        if self.is_consumable(expected_type=(TokenType.SIMPLE_TYPE, TokenType.COMPOUND_TYPE, TokenType.TYPE_MODIFIER)):
            return self.parse_full_variable_declaration(context)

        return self.parse_full_expression(context)

    def parse_full_class_keywords(self, context: ContextFlag) -> ClassFieldDeclarationNode | ClassModifierKeyword:
        """
        Parse full statement beginning with class-only keywords such as private, virtual, static, overload...
        :param context: scope context flag. Should strictly equal to class
        :return:
        """
        # scope check: only in class, but not inside methods
        if not ContextFlag.strict_match(context, ContextFlag.CLASS):
            self.error(f"Unexpected token {self.current_token.value} in non-class context")

        # for checking repeating keywords
        class_keywords = set()

        # obtaining needed info: access_type, polymorphism marker and static marker
        access_modifier: str | None = None
        polymorphic_modifier: str | None = None
        static: bool = False

        while self.is_consumable(TokenType.CLASS_KEYWORD):
            value = self.consume(TokenType.CLASS_KEYWORD)
            if value in class_keywords:
                self.error(f"Duplicated token {value} in field/method definition")
            class_keywords.add(value)

            if value in (AccessType.PUBLIC, AccessType.PRIVATE, AccessType.PROTECTED):
                access_modifier = (
                    value if access_modifier is None else
                    self.error(f"Conflicting or repeating access type token {value} in field/method definition")
                )

            if value in (ClassModifierKeyword.VIRTUAL, ClassModifierKeyword.OVERRIDE):
                polymorphic_modifier = (
                    value if polymorphic_modifier is None else
                    self.error(
                        f"Conflicting or repeating polymorphic specifier type token {value} in field/method definition"
                    )
                )

            if value == ClassModifierKeyword.STATIC:
                static = True

        # end of loop
        # it's either method OR field. Nothing else!
        if self.is_consumable(Keyword.FUNCTION):
            result = self.parse_full_function_definition(context)
        else:
            if polymorphic_modifier is not None:
                self.error(f"Cannot assign polymorphism marker {polymorphic_modifier} other than class method.")
            result = self.parse_full_variable_declaration(context)

        if not isinstance(result, (ClassFieldDeclarationNode, ClassMethodDeclarationNode)):
            self.error(f"Parsed expression here is not neither field nor method.")

        if access_modifier is not None:
            result.access_type = access_modifier

        if polymorphic_modifier == ClassModifierKeyword.VIRTUAL:
            result.virtual = True

        if polymorphic_modifier == ClassModifierKeyword.OVERRIDE:
            result.override = True

        if static:
            result.static = True

        return result

    def parse_full_class_definition(self, context: ContextFlag) -> ClassDefinitionNode:
        """
        Parses the class definition, with all generics, inheritance, fields and methods
        :param context: scope context flag. Should be strictly global.
        :return: ClassDefinitionNode instance
        """
        # scope check: global only
        if not ContextFlag.strict_match(context, ContextFlag.GLOBAL):
            self.error(f"Unexpected token {self.current_token.value} in non-global context.")

        # denote for other statements that currently we're inside class definition
        current_context = ContextFlag.add(context, ContextFlag.CLASS)

        # consume class keyword
        self.consume(TokenType.KEYWORD, Keyword.CLASS)
        line, position = self.line_and_position_of_consumed_token()

        # consume class name, without brackets or parens
        class_name = self.consume(TokenType.IDENTIFIER)

        # parse generic parameters declaration
        generic_parameters = []
        if self.is_consumable(TokenType.OPENING_SQUARE_BRACKET):
            generic_parameters = self.parse_generic_parameters("declaration", current_context)

        # parse super class if present
        inherited_class = None
        if self.is_consumable(TokenType.KEYWORD, Keyword.FROM):
            self.consume(TokenType.KEYWORD, Keyword.FROM)
            inherited_class = self.parse_base_type(current_context)

        # parse contents inside class scope and separate them
        _scope = self.parse_scope(current_context)
        class_fields = []
        class_methods = []
        static_fields = []
        static_methods = []

        # there are only two possible expressions: fields and methods (object-dependent or static).
        for expression in _scope.statements:
            if isinstance(expression, ClassFieldDeclarationNode):
                if expression.static:
                    static_fields.append(expression)
                else:
                    class_fields.append(expression)
            elif isinstance(expression, ClassMethodDeclarationNode):
                if expression.static:
                    static_methods.append(expression)
                else:
                    class_methods.append(expression)
            else:
                self.error(
                    f"Unexpected expression: {expression.__class__.__name__}\n"
                    f"at line {expression.line} position {expression.position}"
                )

        # return instance
        return ClassDefinitionNode(
            class_name=class_name,
            generic_parameters=generic_parameters,
            inherited_class=inherited_class,
            fields_definitions=class_fields,
            methods_definitions=class_methods,
            static_fields_definitions=static_fields,
            static_methods_definitions=static_methods,
            line=line, position=position,
        )

    def parse_generic_parameters(
        self,
        mode: Literal["declaration", "instantiation"],
        context: ContextFlag
    ) -> list[GenericParameterNode | TypeNode]:
        """
        Parse generic parameters for user-defined class.
        Either as declaration, or as instantiation parameters.
        :param mode: "declaration" if we parse class declaration with generics, else "instantiation"
        :param context: scope context flag
        :return: list of GenericParameterNode or TypeNode instances
        """
        self.consume(TokenType.OPENING_SQUARE_BRACKET)
        arguments = []

        while self.current_token.type != TokenType.CLOSING_SQUARE_BRACKET:
            if mode == "declaration":
                self.consume(TokenType.KEYWORD, Keyword.TYPE)
                line, position = self.line_and_position_of_consumed_token()

                identifier = self.consume(TokenType.IDENTIFIER)
                arguments.append(GenericParameterNode(identifier, line, position))
            elif mode == "instantiation":
                arguments.append(self.parse_base_type(context))
            else:
                raise ValueError(f"Unknown mode for parsing generics: {mode}")

            if self.is_consumable(TokenType.CLOSING_SQUARE_BRACKET):
                break
            self.consume(TokenType.COMMA)

        self.consume(TokenType.CLOSING_SQUARE_BRACKET)
        return arguments

    def parse_scope(self, context: ContextFlag) -> ScopeNode:
        """
        Parse the scope, limited with braces
        :param context: parent scope context flag
        :return: ScopeNode instance
        """

        # modify context to disallow class and function definitions
        current_context = ContextFlag.add(context, ContextFlag.LOCAL)

        self.consume(TokenType.BEGIN_OF_SCOPE)
        line, position = self.line_and_position_of_consumed_token()

        statements = []
        local_variables = []

        met_finalizer = False

        while self.current_token.type != TokenType.END_OF_SCOPE:
            statement = self.parse_statement(current_context)

            # if parser did meet return or throw,
            # don't include further expressions into AST
            if not met_finalizer:
                statements.append(statement)
            if isinstance(statement, VariableDeclarationNode):
                local_variables.append(statement)
            if isinstance(statement, (ReturnNode, ContinueNode, BreakNode)):
                met_finalizer = True

        self.consume(TokenType.END_OF_SCOPE)
        return ScopeNode(statements, local_variables, line, position)

    def parse_full_if_else_statement(self, context: ContextFlag) -> IfElseNode:
        """
        Parses the if-else statement
        :param context: scope context flag. Mustn't be strictly class one
        :return: IfElseNode instance
        """

        # validate scope: it shouldn't be directly in the class (but can be in class method)
        if ContextFlag.strict_match(context, ContextFlag.CLASS):
            self.error(
                "If-else statements are not allowed inside class definition outside of method or constructor."
            )

        self.consume(TokenType.KEYWORD, Keyword.IF)
        line, position = self.line_and_position_of_consumed_token()

        condition = self._parse_condition(context)
        if_scope = self.parse_scope(context)

        root_node = IfElseNode(condition, if_scope, None, line, position)
        current_node = root_node

        # consume else ifs as much as possible.
        while self.is_consumable(TokenType.KEYWORD, Keyword.ELSE):
            self.consume(TokenType.KEYWORD, Keyword.ELSE)

            if self.is_consumable(TokenType.KEYWORD, Keyword.IF):
                # Handle "else if" condition
                self.consume(TokenType.KEYWORD, Keyword.IF)
                line, position = self.line_and_position_of_consumed_token()

                elif_condition = self._parse_condition(context)
                elif_scope = self.parse_scope(context)

                obj = IfElseNode(elif_condition, elif_scope, None, line, position)
                current_node.else_node = obj
                current_node = obj
            else:
                # Handle last "else" block
                current_node.else_scope = self.parse_scope(context)

        # semicolon is not required here, but not redundant
        if self.is_consumable(TokenType.END_OF_STATEMENT):
            self.consume(TokenType.END_OF_STATEMENT)
        return root_node

    def _parse_condition(self, context: ContextFlag) -> ASTNode:
        self.consume(TokenType.OPENING_PARENTHESIS)
        condition = self.parse_arithmetic_expression(context)
        self.consume(TokenType.CLOSING_PARENTHESIS)
        return condition

    def parse_full_while_statement(self, context: ContextFlag) -> WhileNode:

        # validate scope: it shouldn't be directly in the class (but can be in class method)
        if ContextFlag.strict_match(context, ContextFlag.CLASS):
            self.error(
                "Loops are not allowed inside class definition outside of method or constructor."
            )

        # modify context to allow BREAK and CONTINUE expressions
        current_context = ContextFlag.add(context, ContextFlag.LOOP)

        self.consume(TokenType.KEYWORD, Keyword.WHILE)
        line, position = self.line_and_position_of_consumed_token()

        condition = self._parse_condition(current_context)
        while_scope = self.parse_scope(current_context)
        if self.is_consumable(TokenType.END_OF_STATEMENT):
            self.consume(TokenType.END_OF_STATEMENT)
        return WhileNode(condition, while_scope, line, position)

    def parse_full_break_statement(self, context: ContextFlag) -> BreakNode:
        """
        Parses the break keyword statement.
        Doesn't modify the current context.
        Allowed only in loops.
        :param context: scope context flag. Should be loop one
        :return: BreakNode instance
        """
        # scope check: needs loop
        if not ContextFlag.match(context, ContextFlag.LOOP):
            self.error(f"Unexpected token {self.current_token.value} out of loop.")

        self.consume(TokenType.KEYWORD, Keyword.BREAK)
        line, position = self.line_and_position_of_consumed_token()
        self.consume(TokenType.END_OF_STATEMENT)
        return BreakNode(line, position)

    def parse_full_continue_statement(self, context: ContextFlag) -> ContinueNode:
        """
        Parses the continue keyword statement.
        Doesn't modify the current context.
        Allowed only in loops.
        :param context: scope context flag. Should be loop one.
        :return: ContinueNode instance
        """
        # scope check: needs loop
        if not ContextFlag.match(context, ContextFlag.LOOP):
            self.error(f"Unexpected token {self.current_token.value} out of loop.")

        self.consume(TokenType.KEYWORD, Keyword.CONTINUE)
        line, position = self.line_and_position_of_consumed_token()
        self.consume(TokenType.END_OF_STATEMENT)
        return ContinueNode(line, position)

    def parse_full_function_definition(self, context: ContextFlag) \
            -> FunctionDeclarationNode | ClassMethodDeclarationNode:
        """
        Parses the full function/method definition,
        including return type, parameters, and function body
        :param context: scope context flag. Should be only in global or in class.
        :return: FunctionDeclarationNode or ClassMethodDeclarationInstance instance
        """
        # scope check: global or class
        if not (
            ContextFlag.strict_match(context, ContextFlag.GLOBAL) or
            ContextFlag.strict_match(context, ContextFlag.CLASS)
        ):
            self.error(f"Unexpected non-anonymous function definition in non-global or non-class context.")

        # denote function for inner scopes
        current_context = ContextFlag.add(context, ContextFlag.FUNCTION)

        self.consume(TokenType.KEYWORD, Keyword.FUNCTION)
        line, position = self.line_and_position_of_consumed_token()

        return_type = None
        if self.is_consumable(TokenType.OPENING_SQUARE_BRACKET):
            self.consume(TokenType.OPENING_SQUARE_BRACKET)
            return_type = self.parse_type_declaration(current_context)
            self.consume(TokenType.CLOSING_SQUARE_BRACKET)

        function_name = self.consume(TokenType.IDENTIFIER)

        parameters = self._parse_function_parameters(current_context)
        function_body = self.parse_scope(current_context)

        if self.is_consumable(TokenType.END_OF_STATEMENT):
            self.consume(TokenType.END_OF_STATEMENT)

        if ContextFlag.strict_match(context, ContextFlag.CLASS):
            return ClassMethodDeclarationNode(
                return_type, function_name, parameters, function_body,
                access_type=AccessType.PUBLIC,
                static=False,
                virtual=False,
                overload=False,
                line=line, position=position
            )
        else:
            return FunctionDeclarationNode(return_type, function_name, parameters, function_body, line, position)

    def _parse_function_parameters(self, context: ContextFlag) -> list[FunctionParameter]:
        """
        Parse the function parameters declaration expression
        :param context: scope context flag. Should be a function.
        :return: list of function parameters
        """
        self.consume(TokenType.OPENING_PARENTHESIS)
        parameters = []
        while self.current_token.type != TokenType.CLOSING_PARENTHESIS:
            type_node = self.parse_type_declaration(context)

            parameter_name = self.consume(TokenType.IDENTIFIER)
            line, position = self.line_and_position_of_consumed_token()

            default_value = None
            if self.is_consumable(TokenType.GENERIC_ASSIGNMENT):

                # forbid reference defaults
                self.consume(TokenType.GENERIC_ASSIGNMENT, Assignment.VALUE_ASSIGNMENT)
                default_value = self.parse_arithmetic_expression(context)

            parameters.append(FunctionParameter(type_node, parameter_name, default_value, line, position))

            if self.is_consumable(TokenType.COMMA):
                self.consume(TokenType.COMMA)
        self.consume(TokenType.CLOSING_PARENTHESIS)
        return parameters

    def parse_full_return_statement(self, context: ContextFlag) -> ReturnNode:
        """
        Parses the return statement in a function or method.
        :param context: scope context flag. Should be a function.
        :return: ReturnNode object
        """

        # scope check: functions/methods only
        if not ContextFlag.match(context, ContextFlag.FUNCTION):
            self.error(f"Unexpected token {self.current_token.value} out of function or method.")

        self.consume(TokenType.KEYWORD, Keyword.RETURN)
        line, position = self.line_and_position_of_consumed_token()

        # return may be a sole keyword, or with some expression
        expression = None
        if not self.is_consumable(TokenType.END_OF_STATEMENT):
            expression = self.parse_arithmetic_expression(context)
        self.consume(TokenType.END_OF_STATEMENT)
        return ReturnNode(expression, line, position)

    # TODO: more comments
    # TODO: do we really need that parser? Check it
    def parse_full_variable_declaration(self, context: ContextFlag):
        type_node = self.parse_type_declaration(context)
        return self._parse_partial_variable_expression(type_node, context)

    def _parse_partial_variable_expression(self, type_node: ASTNode, context: ContextFlag)\
            -> VariableDeclarationNode | ClassFieldDeclarationNode:
        identifier = self.consume(TokenType.IDENTIFIER)
        line, position = self.line_and_position_of_consumed_token()

        if self.is_consumable(TokenType.GENERIC_ASSIGNMENT):
            operator = self.consume(TokenType.GENERIC_ASSIGNMENT)
            expression_node = self.parse_assignment_expression(context)
        else:
            operator = None
            expression_node = None

        if ContextFlag.strict_match(context, ContextFlag.CLASS):
            result = ClassFieldDeclarationNode(
                type_node, identifier, operator, expression_node,
                AccessType.PROTECTED, False,
                line, position
            )
        else:
            result = VariableDeclarationNode(type_node, identifier, operator, expression_node, line, position)

        self.consume(TokenType.END_OF_STATEMENT)
        return result

    def parse_full_expression(self, context):
        result = self.parse_assignment_expression(context)
        if self.is_consumable(TokenType.IDENTIFIER):
            type_name = self.refine_identifier(result, "class_name")
            return self._parse_partial_variable_expression(type_name, context)
        self.consume(TokenType.END_OF_STATEMENT)
        return result

    def parse_type_declaration(self, context: ContextFlag):
        # Check for const or reference modifiers
        modifiers = []
        while self.is_consumable(TokenType.TYPE_MODIFIER):
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

    def parse_base_type(self, context: ContextFlag, as_constructor: bool = False) -> TypeNode:
        if self.is_consumable(TokenType.SIMPLE_TYPE):
            type_name = self.consume(TokenType.SIMPLE_TYPE)
            line, position = self.line_and_position_of_consumed_token()
            type_literal_node = TypeLiteral(type_name, line, position)
            return TypeNode(TypeCategory.PRIMITIVE, type_literal_node, None, line, position)

        elif self.is_consumable(TokenType.COMPOUND_TYPE):
            compound_type = self.consume(TokenType.COMPOUND_TYPE)
            line, position = self.line_and_position_of_consumed_token()

            parameters = []
            if self.is_consumable(TokenType.OPENING_SQUARE_BRACKET):
                parameters = self.__parse_square_bracket_content(allow_keymaps=False, context=context)

            type_literal_node = TypeLiteral(compound_type, line, position)
            return TypeNode(TypeCategory.COLLECTION, type_literal_node, parameters, line, position)

        elif self.is_consumable(TokenType.IDENTIFIER):
            identifier = self.parse_identifier(context=context)
            return self.refine_identifier(identifier, "constructor" if as_constructor else "class_name")

        else:
            self.error("Invalid type declaration")

    def parse_arithmetic_expression(self, context: ContextFlag):
        return self.parse_logical_or_expression(context)

    def parse_assignment_expression(self, context: ContextFlag) -> AssignmentNode | ASTNode:
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
        :param context: scope context flag
        :return: Assignment node if assignment is present,
        otherwise anything the primary parser will return.
        """
        left_expr = self.parse_logical_or_expression(context)

        while self.is_consumable(TokenType.GENERIC_ASSIGNMENT):
            operator = self.consume(TokenType.GENERIC_ASSIGNMENT)
            line, position = self.line_and_position_of_consumed_token()
            right_expr = self.parse_logical_or_expression(context)
            left_expr = AssignmentNode(left_expr, operator, right_expr, line, position)

        return left_expr

    def parse_logical_or_expression(self, context: ContextFlag) -> LogicalOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 1 (low)
        Associativity: left to right
        Tokens: ||, or
        :param context: scope context flag
        :return: Logical operator node if disjunction is present,
        otherwise anything the next precedence (logical xor) parser will return.
        """
        left = self.parse_logical_xor_expression(context)

        while self.is_consumable(TokenType.OPERATOR, expected_value=(Operator.OR, Operator.FULL_OR)):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_logical_xor_expression(context)
            left = LogicalOperatorNode(left=left, operator=operator, right=right, line=line, position=position)

        return left

    def parse_logical_xor_expression(self, context: ContextFlag) -> LogicalOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 2 (low)
        Associativity: left to right
        Tokens: ^^, xor
        :param context: scope context flag
        :return: Logical operator node if exclusive disjunction (addition by modulo 2) is present,
        otherwise anything the next precedence (logical and) parser will return.
        """
        left = self.parse_logical_and_expression(context)

        while self.is_consumable(TokenType.OPERATOR, expected_value=(Operator.XOR, Operator.FULL_XOR)):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_logical_and_expression(context)
            left = LogicalOperatorNode(left=left, operator=operator, right=right, line=line, position=position)

        return left

    def parse_logical_and_expression(self, context: ContextFlag) -> LogicalOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 3 (low)
        Associativity: left to right
        Tokens: &&, and
        :param context: scope context flag
        :return: Logical operator node if conjunction is present,
        otherwise anything the next precedence (bitwise or) parser will return.
        """
        left = self.parse_bitwise_or_expression(context)

        while self.is_consumable(TokenType.OPERATOR, expected_value=(Operator.AND, Operator.FULL_AND)):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_bitwise_or_expression(context)
            left = LogicalOperatorNode(left=left, operator=operator, right=right, line=line, position=position)

        return left

    def parse_bitwise_or_expression(self, context: ContextFlag) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 4 (low-medium)
        Associativity: left to right
        Tokens: |
        :param context: scope context flag
        :return: Arithmetic operator node if bitwise disjunction is present,
        otherwise anything the next precedence (bitwise xor) parser will return.
        """
        left = self.parse_bitwise_xor_expression(context)

        while self.is_consumable(TokenType.OPERATOR, Operator.BITWISE_OR):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_bitwise_xor_expression(context)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right, line=line, position=position)

        return left

    def parse_bitwise_xor_expression(self, context: ContextFlag) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 5 (low-medium)
        Associativity: left to right
        Tokens: ^
        :param context: scope context flag
        :return: Arithmetic operator node if bitwise exclusive disjunction (addition by modulo 2) is present,
        otherwise anything the next precedence (bitwise and) parser will return.
        """
        left = self.parse_bitwise_and_expression(context)

        while self.is_consumable(TokenType.OPERATOR, Operator.BITWISE_XOR):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_bitwise_and_expression(context)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right, line=line, position=position)

        return left

    def parse_bitwise_and_expression(self, context: ContextFlag) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 6 (low-medium)
        Associativity: left to right
        Tokens: &
        :param context: scope context flag
        :return: Arithmetic operator node if bitwise conjunction is present,
        otherwise anything the next precedence (equality operators) parser will return.
        """
        left = self.parse_equality_expression(context)

        while self.is_consumable(TokenType.OPERATOR, Operator.BITWISE_AND):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_equality_expression(context)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right, line=line, position=position)

        return left

    def parse_equality_expression(self, context: ContextFlag) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 7 (medium)
        Associativity: right to left (with logical "and" proxy)
        Tokens: ==, !=, ===, !==
        :param context: scope context flag
        :return: Comparison operator node if one operator is present,
        or logical operator node ("and") if it's the chain of these operators
        otherwise anything the next precedence (comparison operators) parser will return.
        """
        left = self.parse_comparison_expression(context)

        statements = []
        while self.is_consumable(TokenType.OPERATOR, expected_value=(
            Operator.EQUAL,
            Operator.NOT_EQUAL,
            Operator.STRICT_EQUAL,
            Operator.NOT_STRICT_EQUAL,
        )):

            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_comparison_expression(context)

            statements.append(ComparisonNode(left=left, operator=operator, right=right, line=line, position=position))
            left = right

        if not statements:
            return left
        return self.__parse_chained_comparisons(statements)

    def parse_comparison_expression(self, context: ContextFlag) \
            -> ComparisonNode | LogicalOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 8 (medium)
        Associativity: right to left (with logical "and" proxy)
        Tokens: >, >=, <, <=
        :param context: scope context flag
        :return: Comparison operator node if one operator is present,
        or logical operator node ("and") if it's the chain of these operators
        otherwise anything the next precedence (bitwise shift operators) parser will return.
        """

        statements = []
        left = self.parse_bitwise_shift_expression(context)

        while self.is_consumable(TokenType.OPERATOR, expected_value=(
            Operator.LESSER_OR_EQUAL,
            Operator.GREATER_OR_EQUAL,
            Operator.LESSER,
            Operator.GREATER,
        )):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_bitwise_shift_expression(context)

            statements.append(ComparisonNode(left=left, operator=operator, right=right, line=line, position=position))
            left = right

        if not statements:
            return left
        return self.__parse_chained_comparisons(statements)

    @staticmethod
    def __parse_chained_comparisons(statements: list[ComparisonNode]) -> ComparisonNode | LogicalOperatorNode:
        r"""
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
        :param statements: the statements needed to be chained (or not)
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

    def parse_bitwise_shift_expression(self, context: ContextFlag) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 9 (upper-medium)
        Associativity: left-to-right
        Tokens: >>, <<
        :param context: scope context flag
        :return: Arithmetic operator node if bitwise shift operators are present,
        otherwise anything the next precedence (additive operators) parser will return.
        """
        left = self.parse_additive_expression(context)

        while self.is_consumable(TokenType.OPERATOR, expected_value=(
            Operator.BITWISE_LSHIFT,
            Operator.BITWISE_RSHIFT
        )):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_additive_expression(context)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right, line=line, position=position)

        return left

    def parse_additive_expression(self, context: ContextFlag) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 10 (upper-medium)
        Associativity: left-to-right
        Tokens: +, -
        :param context: scope context flag
        :return: Arithmetic operator node if additive operators are present,
        otherwise anything the next precedence (multiplicative operators) parser will return.
        """
        left = self.parse_multiplicative_expression(context)

        while self.is_consumable(TokenType.OPERATOR, expected_value=(Operator.PLUS, Operator.MINUS)):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_multiplicative_expression(context)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right, line=line, position=position)

        return left

    def parse_multiplicative_expression(self, context: ContextFlag) -> ArithmeticOperatorNode | ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 11 (upper)
        Associativity: left-to-right
        Tokens: *, /, %, //
        :param context: scope context flag
        :return: Arithmetic operator node if multiplicative operators are present,
        otherwise anything the next precedence (unary sign operator) parser will return.
        """
        left = self.parse_arithmetic_unary_expression(context)

        while self.is_consumable(TokenType.OPERATOR, expected_value=(
            Operator.MULTIPLY,
            Operator.DIVIDE,
            Operator.FLOOR_DIVIDE,
            Operator.MODULO,
        )):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_arithmetic_unary_expression(context)
            left = ArithmeticOperatorNode(left=left, operator=operator, right=right, line=line, position=position)

        return left

    def parse_arithmetic_unary_expression(self, context: ContextFlag):
        """
        Operator parser.
        Operator type: unary
        Precedence: 12 (upper)
        Associativity: none
        Tokens: +, -, ~
        :param context: scope context flag
        :return: Unary operator node if multiplicative unary operators are present,
        otherwise anything the next precedence (power operator) parser will return.
        """
        if self.is_consumable(TokenType.OPERATOR, expected_value=(
            Operator.PLUS,
            Operator.MINUS,
            Operator.BITWISE_INVERSE,
        )):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_power_expression(context)
            return UnaryOperatorNode(operator=operator, expression=right, line=line, position=position)
        else:
            return self.parse_power_expression(context)

    def parse_power_expression(self, context: ContextFlag):
        """
        Operator parser.
        Operator type: binary
        Precedence: 13 (upper)
        Associativity: right to left
        Tokens: **
        :param context: scope context flag
        :return: Arithmetic operator node if power operators are present,
        otherwise anything the next precedence (other unary) parser will return.
        """
        left = self.parse_other_unary_expression(context)
        right_expressions = [left]
        operators_positions = []

        while self.is_consumable(TokenType.OPERATOR, Operator.POWER):
            _ = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_other_unary_expression(context)
            right_expressions.append(right)
            operators_positions.append((line, position))

        if len(right_expressions) == 1:
            return left

        result = ArithmeticOperatorNode(
            left=right_expressions[-2], operator=Operator.POWER, right=right_expressions[-1],
            line=operators_positions[-1][0], position=operators_positions[-1][1]
        )
        for _left, (_line, _position) in reversed(list(zip(right_expressions[:-2], operators_positions[:-1]))):
            result = ArithmeticOperatorNode(
                left=_left, operator=Operator.POWER, right=result,
                line=_line, position=_position
            )

        return result

    # TODO: reference/dereference
    def parse_other_unary_expression(self, context: ContextFlag):
        """
        Operator parser.
        Operator type: unary
        Precedence: 14 (high)
        Associativity: right to left
        Tokens: not, [reference, dereference]
        :param context: scope context flag
        :return: Unary operator node if other unary operators (logical not, reference operators) are present,
        otherwise anything the next precedence (dynamic memory allocation) parser will return.
        """
        if self.is_consumable(TokenType.OPERATOR, expected_value=(Operator.NOT, )):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_dynamic_memory_allocation(context)
            return UnaryOperatorNode(operator=operator, expression=right, line=line, position=position)
        else:
            return self.parse_dynamic_memory_allocation(context)

    def parse_dynamic_memory_allocation(self, context: ContextFlag):
        """
        Operator parser.
        Operator type: unary
        Precedence: 15 (high)
        Associativity: none (non-stackable)
        Tokens: new, delete
        :param context: scope context flag
        :return: Allocation operator node if other unary operators dynamic memory allocation are present,
        otherwise anything the next precedence (member access) parser will return.
        """
        if self.is_consumable(TokenType.OPERATOR, Operator.NEW_INSTANCE):
            operator = self.consume(TokenType.OPERATOR, Operator.NEW_INSTANCE)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_base_type(context, as_constructor=True)
            return AllocationOperatorNode(operator=operator, expression=right, line=line, position=position)
        elif self.is_consumable(TokenType.OPERATOR, Operator.DELETE_INSTANCE):
            operator = self.consume(TokenType.OPERATOR, Operator.DELETE_INSTANCE)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_identifier(context, pure_identifier=True)
            return AllocationOperatorNode(operator=operator, expression=right, line=line, position=position)
        else:
            return self.parse_member_access(context)

    def parse_member_access(self, context: ContextFlag):
        """
        Operator parser.
        Operator type: binary
        Precedence: 16 (highest)
        Associativity: left to right
        Tokens: . ->
        :param context: scope context flag
        :return: Member operator node if class member operators are present,
        otherwise anything the primary parser will return.
        """
        left = self.parse_primary_expression(context)

        while self.is_consumable(TokenType.OPERATOR, expected_value=(
            Operator.OBJECT_MEMBER_ACCESS,
            Operator.REFERENCE_MEMBER_ACCESS,
        )):
            operator = self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_primary_expression(context)
            left = MemberOperatorNode(left=left, operator=operator, right=right, line=line, position=position)
        return left

    # TODO: this keyword, string adequate parser, comments, refactor it into methods ...
    def parse_primary_expression(self, context: ContextFlag) -> ASTNode:
        if self.is_consumable(expected_type=(
            TokenType.DECIMAL_INTEGER_LITERAL,
            TokenType.HEXADECIMAL_INTEGER_LITERAL,
            TokenType.OCTAL_INTEGER_LITERAL,
            TokenType.BINARY_INTEGER_LITERAL
        )):
            return self.parse_integer()

        if self.is_consumable(TokenType.IMAGINARY_FLOAT_LITERAL):
            value = self.consume(TokenType.IMAGINARY_FLOAT_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return ImaginaryFloatLiteralNode(value=value, line=line, position=position)

        if self.is_consumable(TokenType.FLOAT_LITERAL):
            value = self.consume(TokenType.FLOAT_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return FloatLiteralNode(value=value, line=line, position=position)

        if self.is_consumable(TokenType.OPERAND, Operands.DEDUCTION):
            self.consume(TokenType.OPERAND, Operands.DEDUCTION)
            line, position = self.line_and_position_of_consumed_token()
            return DeductionNode(line=line, position=position)

        if self.is_consumable(TokenType.IDENTIFIER):
            return self.parse_identifier(context)

        if self.is_consumable(TokenType.STRING_LITERAL):
            return self.parse_string()

        if self.is_consumable(TokenType.CHAR_LITERAL):
            value = self.consume(TokenType.CHAR_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return CharLiteralNode(value, line=line, position=position)

        if self.is_consumable(TokenType.BOOLEAN_LITERAL):
            value = self.consume(TokenType.BOOLEAN_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return BooleanLiteralNode(value, line=line, position=position)

        if self.is_consumable(TokenType.NULL_LITERAL):
            _ = self.consume(TokenType.NULL_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return NullLiteralNode(line, position=position)

        if self.is_consumable(TokenType.UNDEFINED_LITERAL):
            _ = self.consume(TokenType.UNDEFINED_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return UndefinedLiteralNode(line, position=position)

        if self.is_consumable(TokenType.BYTE_LITERAL):
            value = self.consume(TokenType.BYTE_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return ByteLiteralNode(value, line=line, position=position)

        if self.is_consumable(TokenType.BYTE_STRING_LITERAL):
            value = self.consume(TokenType.BYTE_STRING_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return ByteStringLiteralNode(value, line=line, position=position)

        if self.is_consumable(TokenType.OPENING_PARENTHESIS):
            self.consume(TokenType.OPENING_PARENTHESIS)
            node = self.parse_arithmetic_expression(context)
            self.consume(TokenType.CLOSING_PARENTHESIS)
            return node
        if self.is_consumable(TokenType.OPENING_SQUARE_BRACKET):
            return self.parse_square_bracket_literal_expression(context)

        if self.is_consumable(expected_type=(TokenType.SIMPLE_TYPE, TokenType.COMPOUND_TYPE, TokenType.TYPE_MODIFIER)):
            return self.parse_type_declaration(context)

        self.error(f"Unexpected token {self.current_token.value}")
        pass

    def parse_integer(self) -> IntegerLiteralNode:
        token_type = self.current_token.type
        if token_type == TokenType.DECIMAL_INTEGER_LITERAL:
            base: Literal[10, 16, 8, 2] = 10
        elif token_type == TokenType.HEXADECIMAL_INTEGER_LITERAL:
            base: Literal[10, 16, 8, 2] = 16
        elif token_type == TokenType.OCTAL_INTEGER_LITERAL:
            base: Literal[10, 16, 8, 2] = 8
        elif token_type == TokenType.BINARY_INTEGER_LITERAL:
            base: Literal[10, 16, 8, 2] = 2
        else:
            self.error(f"Unexpected token {token_type}")

        value = self.consume(token_type)
        line, position = self.line_and_position_of_consumed_token()
        return IntegerLiteralNode(value=value, base=base, line=line, position=position)

    def parse_string(self) -> StringLiteralNode:
        value = self.consume(TokenType.STRING_LITERAL)
        line, position = self.line_and_position_of_consumed_token()
        return StringLiteralNode(value, line=line, position=position)

    def parse_identifier(
        self,
        context: ContextFlag,
        pure_identifier: bool = False,
        **_
    ) -> IdentifierNode | IndexNode | FunctionCallNode:
        """
        Parse an identifier
        It can be a label to some variable, function or even class

        The next token can be the parenthesis or square bracket expression

        :param context:
        :param pure_identifier: (optional) whether square brackets or
        :return:
        """
        identifier = self.consume(TokenType.IDENTIFIER)
        line, position = self.line_and_position_of_consumed_token()
        previous_result = IdentifierNode(identifier, line, position)
        return self._parse_indexation_or_function_calls_if_exist(previous_result, context, pure_identifier)

    def _parse_indexation_or_function_calls_if_exist(self, node, context: ContextFlag, pure_identifier: bool = False):
        token = self.current_token
        if token.type == TokenType.OPENING_SQUARE_BRACKET:
            if pure_identifier:
                self.error(f"Unexpected token: {self.current_token.value}")
            result = self._parse_indexation_call(node, context)
            return result
        elif token.type == TokenType.OPENING_PARENTHESIS:
            if pure_identifier:
                self.error(f"Unexpected token: {self.current_token.value}")
            result = self._parse_function_call(node, context)
            return result
        else:
            return node

    def _parse_function_call(self, identifier, context: ContextFlag):
        line, position = self.line_and_position_of_consumed_token()
        arguments = self.__parse_parentheses_content(context)
        result = FunctionCallNode(identifier, arguments, line, position)
        return self._parse_indexation_or_function_calls_if_exist(result, context)

    def _parse_indexation_call(self, identifier, context: ContextFlag):
        line, position = self.line_and_position_of_consumed_token()
        arguments = self.__parse_square_bracket_content(allow_keymaps=False, context=context)
        result = IndexNode(identifier, arguments, line, position)
        return self._parse_indexation_or_function_calls_if_exist(result, context)

    def __parse_square_bracket_content(self, allow_keymaps: bool, context: ContextFlag) -> list[ASTNode]:

        self.consume(TokenType.OPENING_SQUARE_BRACKET)
        arguments = []

        while self.current_token.type != TokenType.CLOSING_SQUARE_BRACKET:
            if allow_keymaps:
                argument = self.parse_arithmetic_expression_with_keymaps(context)
            else:
                argument = self.parse_arithmetic_expression(context)
            arguments.append(argument)

            if self.is_consumable(TokenType.CLOSING_SQUARE_BRACKET):
                break
            self.consume(TokenType.COMMA)

        self.consume(TokenType.CLOSING_SQUARE_BRACKET)
        return arguments

    def __parse_parentheses_content(self, context: ContextFlag) -> list[ASTNode]:
        self.consume(TokenType.OPENING_PARENTHESIS)
        arguments = []

        while self.current_token.type != TokenType.CLOSING_PARENTHESIS:
            argument = self.parse_arithmetic_expression(context)
            arguments.append(argument)

            if self.is_consumable(TokenType.CLOSING_PARENTHESIS):
                break
            self.consume(TokenType.COMMA)

        self.consume(TokenType.CLOSING_PARENTHESIS)
        return arguments

    def parse_square_bracket_literal_expression(
        self,
        context: ContextFlag
    ) -> ListLiteralNode | KeymapLiteralNode | EmptyLiteralNode:
        arguments = self.__parse_square_bracket_content(allow_keymaps=True, context=context)
        line, position = self.line_and_position_of_consumed_token()

        keymap_literals_count = sum(map(lambda x: isinstance(x, KeymapOperatorNode), arguments))
        if keymap_literals_count == 0:
            if arguments:
                return ListLiteralNode(arguments, line, position)
            else:
                return EmptyLiteralNode(line, position)
        elif keymap_literals_count == len(arguments):
            return KeymapLiteralNode(arguments, line, position)
        else:
            self.error(f"List/keymap literal cannot have both keymap and non-keymap expressions")

    def parse_arithmetic_expression_with_keymaps(self, context: ContextFlag):
        # absent associativity
        left = self.parse_arithmetic_expression(context)

        if self.is_consumable(TokenType.OPERATOR, Operator.KEYMAP_LITERAL):
            self.consume(TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_arithmetic_expression(context)
            return KeymapOperatorNode(
                left=left, operator=Operator.KEYMAP_LITERAL, right=right,
                line=line, position=position
            )
        else:
            return left

    def refine_identifier(
        self,
        node,
        refine_as: Literal["class_name", "constructor"]
    ) -> TypeNode | FunctionCallNode:
        if refine_as == "class_name":
            return self.refine_identifier_as_class_name(node)
        elif refine_as == "constructor":
            if not isinstance(node, FunctionCallNode):
                self.error("Expected parenthesised expression for constructor")
            return FunctionCallNode(
                identifier=self.refine_identifier_as_class_name(node.identifier),
                arguments=node.arguments,
                line=node.line,
                position=node.position
            )
        raise ValueError(f"Unexpected value: {refine_as}")

    def refine_identifier_as_class_name(
        self,
        node
    ) -> TypeNode:
        if isinstance(node, IdentifierNode):
            return TypeNode(TypeCategory.CLASS, node, None, node.line, node.position)
        elif isinstance(node, IndexNode):
            if not isinstance(node.variable, IdentifierNode):
                self.error(f"Invalid class type declaration: {node.variable.__class__.__name__}")
            return TypeNode(
                category=TypeCategory.GENERIC_CLASS,
                type_node=node.variable,
                args=[self.refine_identifier_as_class_name(x) for x in node.arguments],
                line=node.line,
                position=node.position
            )
        elif isinstance(node, TypeNode):
            if node.category in (TypeCategory.PRIMITIVE, TypeCategory.COLLECTION):
                return node
        else:
            self.error(f"Invalid class type declaration: {node.__class__.__name__}")
