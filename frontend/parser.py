from enum import IntFlag

from ._syntax.keywords import ClassModifierKeyword, Keyword
from ._syntax.types_modifier import TypeModifier
from ._syntax.operators import Operator, Comparison, OperatorMethods
from .abstract_syntax_tree import MemberOperatorNode

try:
    import frontend.abstract_syntax_tree as AST
except ImportError:
    import abstract_syntax_tree as AST

from .exceptions import ParsingException
from .tokens import TokenType, Token
from typing import Iterator, KeysView, ValuesView, NoReturn, Literal


# TODO: inherited generics should equal base
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
    def match(current_context: "ContextFlag", flag: "ContextFlag") -> bool:
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
    def strict_match(current_context: "ContextFlag", flag: "ContextFlag") -> bool:
        """
        Check if the current context is strictly equal the given flag.
        E.g. if keyword should be in class scope, but not inside method
        :param current_context: the context to check
        :param flag: the flag the context should equal
        :return: boolean indicating whether context and flag are equal
        """
        return current_context == flag

    @staticmethod
    def add(current_context: "ContextFlag", flag: "ContextFlag") -> "ContextFlag":
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

    def consume(self, expected_type: str, expected_value: str | None = None) -> str:
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
                       f"but got {token.type} ({token.value})")

            # token value is not among collection of the expected ones => error
            elif isinstance(expected_value, (tuple, list, set, ValuesView, KeysView)):
                msg = (f"Expected token is among these values: {str(expected_value)}, "
                       f"but got {token.type} (Token type {token.type})")

            # only one token value is expected, but got different => error
            else:
                msg = (f"Expected token is {expected_value}, "
                       f"but got {token.type} (Token type {token.type})")
            self.error(msg)

    def is_consumable(self, expected_type, expected_value: str | tuple | None = None) -> bool:
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

    def parse(self) -> AST.ProgramNode:
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

    def parse_statement(self, context: ContextFlag, **kwargs) -> AST.ASTNode:
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
            return self.parse_scope(context, **kwargs)

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
            return self.parse_full_break_statement(context, **kwargs)

        # continue
        if self.is_consumable(TokenType.KEYWORD, Keyword.CONTINUE):
            return self.parse_full_continue_statement(context, **kwargs)

        if self.is_consumable(TokenType.CLASS_KEYWORD):
            return self.parse_full_class_keywords(context)

        # statement begins with built-in type or modified user-defined type
        if self.is_consumable(expected_type=(TokenType.SIMPLE_TYPE, TokenType.COMPOUND_TYPE, TokenType.TYPE_MODIFIER)):
            return self.parse_full_variable_declaration(context)

        return self.parse_full_expression(context)

    def parse_full_class_keywords(
        self,
        context: ContextFlag
    ) -> AST.ClassFieldDeclarationNode | ClassModifierKeyword | AST.FunctionDefNode:
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

            if value in (AST.AccessType.PUBLIC, AST.AccessType.PRIVATE, AST.AccessType.PROTECTED):
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
        if self.is_consumable(
                TokenType.KEYWORD,
                (Keyword.FUNCTION, Keyword.CONSTRUCTOR, Keyword.DESTRUCTOR, Keyword.OPERATOR)):
            result = self.parse_full_function_definition(context)
        else:
            if polymorphic_modifier is not None:
                self.error(f"Cannot assign polymorphism marker {polymorphic_modifier} other than class method.")
            result = self.parse_full_variable_declaration(context)

        if not isinstance(
            result, (AST.ClassFieldDeclarationNode, AST.ClassMethodDeclarationNode, AST.FunctionDefNode)
        ):
            self.error(msg="Parsed expression here is not neither field nor method.")

        if isinstance(result, AST.FunctionDefNode):
            if not result.function_name.startswith("$operator_"):
                raise AssertionError("It is not a global operator overload!")
            elif not static:
                self.error(msg="Overloading operators should be static!")
            elif polymorphic_modifier is not None:
                self.error(msg="Overloading operators cannot be virtual")
            elif polymorphic_modifier is not None and polymorphic_modifier != AST.AccessType.PUBLIC:
                self.error(msg="Overloading operators cannot be different access type than public!")
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

    def parse_full_class_definition(self, context: ContextFlag) -> AST.ClassDefNode:
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
                self.error(
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
        self,
        mode: Literal["declaration", "instantiation"],
        context: ContextFlag
    ) -> list[AST.GenericParameterNode | AST.TypeNode]:
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
                identifier = self.consume(TokenType.IDENTIFIER)
                line, position = self.line_and_position_of_consumed_token()
                arguments.append(AST.GenericParameterNode(identifier, line, position))
            elif mode == "instantiation":
                arguments.append(self.parse_base_type(context))
            else:
                raise ValueError(f"Unknown mode for parsing generics: {mode}")

            if self.is_consumable(TokenType.CLOSING_SQUARE_BRACKET):
                break
            self.consume(TokenType.COMMA)

        self.consume(TokenType.CLOSING_SQUARE_BRACKET)
        return arguments

    def parse_scope(self, context: ContextFlag, **kwargs) -> AST.ScopeNode:
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
            statement = self.parse_statement(current_context, **kwargs)

            # if parser did meet return or throw,
            # don't include further expressions into AST
            if not met_finalizer:
                statements.append(statement)
            if isinstance(statement, AST.VariableDeclarationNode):
                local_variables.append(statement)
            if isinstance(statement, (AST.ReturnNode, AST.ContinueNode, AST.BreakNode)):
                met_finalizer = True

        self.consume(TokenType.END_OF_SCOPE)
        return AST.ScopeNode(statements, local_variables, line, position)

    def parse_full_if_else_statement(self, context: ContextFlag) -> AST.IfElseNode:
        """
        Parses the if-else statement
        :param context: scope context flag. Mustn't be strictly class one
        :return: IfElseNode instance
        """

        # validate scope: it shouldn't be directly in the class (but can be in class method)
        if ContextFlag.strict_match(current_context=context, flag=ContextFlag.CLASS):
            self.error(
                msg="If-else statements are not allowed inside class definition outside of method or constructor."
            )

        self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.IF)
        line, position = self.line_and_position_of_consumed_token()

        condition = self._parse_condition(context=context)
        if_scope = self.parse_scope(context=context)

        root_node = AST.IfElseNode(condition=condition, if_scope=if_scope, else_scope=None, line=line, position=position)
        current_node: AST.IfElseNode = root_node

        # consume else ifs as much as possible.
        while self.is_consumable(expected_type=TokenType.KEYWORD, expected_value=Keyword.ELSE):
            self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.ELSE)

            if self.is_consumable(expected_type=TokenType.KEYWORD, expected_value=Keyword.IF):
                # Handle "else if" condition
                self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.IF)
                line, position = self.line_and_position_of_consumed_token()

                elif_condition = self._parse_condition(context=context)
                elif_scope = self.parse_scope(context=context)

                obj = AST.IfElseNode(condition=elif_condition, if_scope=elif_scope, else_scope=None, line=line, position=position)
                current_node.else_node = obj
                current_node = obj
            else:
                # Handle last "else" block
                current_node.else_scope = self.parse_scope(context)

        # semicolon is not required here, but not redundant
        if self.is_consumable(expected_type=TokenType.END_OF_STATEMENT):
            self.consume(expected_type=TokenType.END_OF_STATEMENT)
        return root_node

    def _parse_condition(self, context: ContextFlag) -> AST.ASTNode:
        self.consume(expected_type=TokenType.OPENING_PARENTHESIS)
        condition = self.parse_arithmetic_expression(context=context)
        self.consume(expected_type=TokenType.CLOSING_PARENTHESIS)
        return condition

    def parse_full_while_statement(self, context: ContextFlag) -> AST.WhileNode:

        # validate scope: it shouldn't be directly in the class (but can be in class method)
        if ContextFlag.strict_match(current_context=context, flag=ContextFlag.CLASS):
            self.error(
                "Loops are not allowed inside class definition outside of method or constructor."
            )

        # modify context to allow BREAK and CONTINUE expressions
        current_context = ContextFlag.add(current_context=context, flag=ContextFlag.LOOP)

        self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.WHILE)
        line, position = self.line_and_position_of_consumed_token()

        condition = self._parse_condition(context=current_context)
        while_scope = self.parse_scope(context=current_context, loop=AST.WhileNode.INSTANCES)
        if self.is_consumable(expected_type=TokenType.END_OF_STATEMENT):
            self.consume(expected_type=TokenType.END_OF_STATEMENT)
        return AST.WhileNode(condition=condition, while_scope=while_scope, line=line, position=position)

    def parse_full_break_statement(self, context: ContextFlag, **kwargs) -> AST.BreakNode:
        """
        Parses the break keyword statement.
        Doesn't modify the current context.
        Allowed only in loops.
        :param context: scope context flag. Should be loop one
        :return: AST.BreakNode instance
        """

        self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.BREAK)
        line, position = self.line_and_position_of_consumed_token()

        expression = None
        if not self.is_consumable(expected_type=TokenType.END_OF_STATEMENT):
            expression = self.parse_arithmetic_expression(context=context)
        self.consume(expected_type=TokenType.END_OF_STATEMENT)

        # scope check: needs loop
        if expression is None:
            if not ContextFlag.match(current_context=context, flag=ContextFlag.LOOP):
                self.error(msg=f"Unexpected token {self.prev_token.value} out of loop.")

            loop = kwargs.get('loop')
            if not loop:
                raise NotImplementedError

            return AST.BreakNode(loop=loop, line=line, position=position)
        else:
            return AST.BreakNode(error=expression, line=line, position=position)

    def parse_full_continue_statement(self, context: ContextFlag, **kwargs) -> AST.ContinueNode:
        """
        Parses the continue keyword statement.
        Doesn't modify the current context.
        Allowed only in loops.
        :param context: scope context flag. Should be loop one.
        :return: AST.ContinueNode instance
        """
        self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.CONTINUE)
        line, position = self.line_and_position_of_consumed_token()

        expression = None
        if not self.is_consumable(expected_type=TokenType.END_OF_STATEMENT):
            expression = self.parse_arithmetic_expression(context=context)
        self.consume(expected_type=TokenType.END_OF_STATEMENT)

        if not expression:
            # scope check: needs loop
            if not ContextFlag.match(current_context=context, flag=ContextFlag.LOOP):
                self.error(msg=f"Unexpected token {self.current_token.value} out of loop.")

            loop = kwargs.get('loop')
            if not loop:
                raise NotImplementedError

            return AST.ContinueNode(loop=loop, line=line, position=position)
        else:
            return AST.ContinueNode(error=expression, line=line, position=position)

    def parse_full_function_definition(self, context: ContextFlag) \
            -> AST.FunctionDefNode | AST.ClassMethodDeclarationNode:
        """
        Parses the full function/method definition,
        including return type, parameters, and function body
        :param context: scope context flag. Should be only in global or in class.
        :return: FunctionDeclarationNode or ClassMethodDeclarationInstance instance
        """
        # scope check: global or class
        if not (
            ContextFlag.strict_match(current_context=context, flag=ContextFlag.GLOBAL) or
            ContextFlag.strict_match(current_context=context, flag=ContextFlag.CLASS)
        ):
            self.error("Unexpected non-anonymous function definition in non-global or non-class context.")

        # denote function for inner scopes
        current_context = ContextFlag.add(current_context=context, flag=ContextFlag.FUNCTION)

        is_constructor = False
        is_destructor = False
        if self.is_consumable(TokenType.KEYWORD, Keyword.FUNCTION):
            self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.FUNCTION)
        elif self.is_consumable(TokenType.KEYWORD, Keyword.CONSTRUCTOR):
            is_constructor = True
            self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.CONSTRUCTOR)
        else:
            is_destructor = True
            self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.CONSTRUCTOR)
        line, position = self.line_and_position_of_consumed_token()
        is_constructor_or_destructor = is_constructor or is_destructor

        if is_constructor_or_destructor and not ContextFlag.match(current_context, ContextFlag.CLASS):
            self.error("Unexpected constructor/destructor definition in global context.")

        return_type = None
        if not is_constructor_or_destructor and self.is_consumable(expected_type=TokenType.OPENING_SQUARE_BRACKET):
            self.consume(expected_type=TokenType.OPENING_SQUARE_BRACKET)
            return_type = self.parse_type_declaration(context=current_context)
            self.consume(expected_type=TokenType.CLOSING_SQUARE_BRACKET)

        is_operator_overload = False
        if not is_constructor_or_destructor and self.is_consumable(expected_type=TokenType.KEYWORD, expected_value=Keyword.OPERATOR):
            is_operator_overload = True
            dct = {}
            gen = self._parse_operator_overload(dct, context=current_context)
            next(gen)
            parameters = self._parse_function_parameters(context=current_context)
            dct['n'] = len(parameters)
            function_name = next(gen)
        elif not is_constructor_or_destructor:
            function_name = self.consume(expected_type=TokenType.IDENTIFIER)
            parameters = self._parse_function_parameters(context=current_context)
        elif is_destructor:
            function_name = "$destructor"
            parameters = self._parse_function_parameters(context=current_context)
            if len(parameters) > 0:
                self.error("Destructor cannot have parameters!.")
        else:
            function_name = "$constructor"
            parameters = self._parse_function_parameters(context=current_context)

        function_body = self.parse_scope(context=current_context)

        if self.is_consumable(expected_type=TokenType.END_OF_STATEMENT):
            self.consume(expected_type=TokenType.END_OF_STATEMENT)

        if ContextFlag.strict_match(current_context=context, flag=ContextFlag.CLASS) and not is_operator_overload:
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

    def _parse_function_parameters(self, context: ContextFlag) -> list[AST.FunctionParameter]:
        """
        Parse the function parameters declaration expression
        :param context: scope context flag. Should be a function.
        :return: list of function parameters
        """
        self.consume(TokenType.OPENING_PARENTHESIS)
        parameters = []
        while self.current_token.type != TokenType.CLOSING_PARENTHESIS:
            type_node = self.parse_type_declaration(context)

            parameter_name = self.consume(expected_type=TokenType.IDENTIFIER)
            line, position = self.line_and_position_of_consumed_token()
            parameters.append(
                AST.FunctionParameter(
                    type_=type_node, parameter_name=parameter_name,
                    line=line, position=position
                )
            )

            if self.is_consumable(expected_type=TokenType.COMMA):
                self.consume(expected_type=TokenType.COMMA)
        self.consume(expected_type=TokenType.CLOSING_PARENTHESIS)
        return parameters

    def _parse_operator_overload(self, dct: dict, context: ContextFlag) -> Iterator[str]:
        """
        Parses operator overloading declaration and returns mangled function name
        :param context:
        :return:
        """
        if not ContextFlag.match(current_context=context, flag=ContextFlag.CLASS):
            self.error(msg="Invalid place to overload operator behaviour")

        _ = self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.OPERATOR)
        if self.is_consumable(expected_type=TokenType.OPERATOR):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            if not OperatorMethods.overloadable(operator):
                self.error(msg=f"Invalid operator for overload: {operator}")

            yield
            n: int = dct['n']

            yield f"$operator_{OperatorMethods.translate(operator, n)}"
        elif self.is_consumable(expected_type=TokenType.OPENING_SQUARE_BRACKET):
            _ = self.consume(expected_type=TokenType.OPENING_SQUARE_BRACKET)
            _ = self.consume(expected_type=TokenType.CLOSING_SQUARE_BRACKET)
            yield
            yield "$operator_index"
        elif self.is_consumable(expected_type=TokenType.OPENING_PARENTHESIS):
            _ = self.consume(expected_type=TokenType.OPENING_PARENTHESIS)
            _ = self.consume(expected_type=TokenType.CLOSING_PARENTHESIS)
            yield
            yield "$operator_call"
        else:
            self.error(msg="Invalid operator to overload")

    def parse_full_return_statement(self, context: ContextFlag) -> AST.ReturnNode:
        """
        Parses the return statement in a function or method.
        :param context: scope context flag. Should be a function.
        :return: AST.ReturnNode object
        """

        # scope check: functions/methods only
        if not ContextFlag.match(current_context=context, flag=ContextFlag.FUNCTION):
            self.error(msg=f"Unexpected token {self.current_token.value} out of function or method.")

        self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.RETURN)
        line, position = self.line_and_position_of_consumed_token()

        # return may be a sole keyword, or with some expression
        expression = None
        if not self.is_consumable(expected_type=TokenType.END_OF_STATEMENT):
            expression = self.parse_arithmetic_expression(context=context)
        self.consume(expected_type=TokenType.END_OF_STATEMENT)
        return AST.ReturnNode(value=expression, line=line, position=position)

    # TODO: more comments
    # TODO: do we really need that parser? Check it
    def parse_full_variable_declaration(self, context: ContextFlag) -> AST.VariableDeclarationNode | AST.ClassFieldDeclarationNode:
        type_node = self.parse_type_declaration(context=context)
        return self._parse_partial_variable_expression(type_node=type_node, context=context)

    def _parse_partial_variable_expression(self, type_node: AST.ASTNode, context: ContextFlag)\
            -> AST.VariableDeclarationNode | AST.ClassFieldDeclarationNode:
        identifier: str = self.consume(expected_type=TokenType.IDENTIFIER)
        line, position = self.line_and_position_of_consumed_token()

        if ContextFlag.strict_match(current_context=context, flag=ContextFlag.CLASS):
            result = AST.ClassFieldDeclarationNode(
                _type=type_node, name=identifier,
                access_type=AST.AccessType.PROTECTED, static=False,
                line=line, position=position
            )
        else:
            if self.is_consumable(expected_type=TokenType.GENERIC_ASSIGNMENT):
                operator = self.consume(expected_type=TokenType.GENERIC_ASSIGNMENT)
                expression_node = self.parse_assignment_expression(context=context)
            else:
                operator = None
                expression_node = None

            result = AST.VariableDeclarationNode(_type=type_node, name=identifier, operator=operator, value=expression_node, line=line, position=position)

        self.consume(expected_type=TokenType.END_OF_STATEMENT)
        return result

    def parse_full_expression(self, context) -> AST.VariableDeclarationNode | AST.ClassFieldDeclarationNode | AST.AssignmentNode | AST.ASTNode:
        result = self.parse_assignment_expression(context=context)
        if self.is_consumable(expected_type=TokenType.IDENTIFIER):
            type_name = self.refine_identifier(node=result, refine_as="class_name")
            return self._parse_partial_variable_expression(type_node=type_name, context=context)
        self.consume(expected_type=TokenType.END_OF_STATEMENT)
        return result

    def parse_type_declaration(self, context: ContextFlag) -> AST.TypeNode:
        # Check for const or reference modifiers
        modifiers = []
        while self.is_consumable(expected_type=TokenType.TYPE_MODIFIER):
            modifiers.append(self.consume(expected_type=TokenType.TYPE_MODIFIER, expected_value=TypeModifier.values()))

        # Parse the base type (simple or compound)
        base_type = self.parse_base_type(context=context)

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

    def parse_base_type(self, context: ContextFlag, as_constructor: bool = False) -> AST.TypeNode:
        if self.is_consumable(expected_type=TokenType.SIMPLE_TYPE):
            type_name = self.consume(expected_type=TokenType.SIMPLE_TYPE)
            line, position = self.line_and_position_of_consumed_token()
            type_literal_node = AST.TypeLiteral(name=type_name, line=line, location=position)
            return AST.TypeNode(
                category=AST.TypeCategory.PRIMITIVE,
                type_node=type_literal_node, args=None, line=line, position=position
            )

        elif self.is_consumable(expected_type=TokenType.COMPOUND_TYPE):
            compound_type = self.consume(expected_type=TokenType.COMPOUND_TYPE)
            line, position = self.line_and_position_of_consumed_token()

            parameters = []
            if self.is_consumable(expected_type=TokenType.OPENING_SQUARE_BRACKET):
                parameters = self.__parse_square_bracket_content(allow_keymaps=False, context=context)

            type_literal_node = AST.TypeLiteral(name=compound_type, line=line, location=position)
            return AST.TypeNode(
                category=AST.TypeCategory.COLLECTION,
                type_node=type_literal_node, args=parameters, line=line, position=position
            )

        elif self.is_consumable(expected_type=TokenType.IDENTIFIER):
            identifier = self.parse_identifier(context=context)
            return self.refine_identifier(node=identifier, refine_as="constructor" if as_constructor else "class_name")

        else:
            self.error(msg="Invalid type declaration")

    def parse_arithmetic_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
        return self.parse_logical_or_expression(context=context)

    def parse_assignment_expression(self, context: ContextFlag) -> AST.AssignmentNode | AST.ASTNode:
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
        left_expr = self.parse_logical_or_expression(context=context)

        while self.is_consumable(expected_type=TokenType.GENERIC_ASSIGNMENT):
            operator = self.consume(expected_type=TokenType.GENERIC_ASSIGNMENT)
            line, position = self.line_and_position_of_consumed_token()
            right_expr = self.parse_logical_or_expression(context=context)
            left_expr = AST.AssignmentNode(
                left=left_expr, operator=operator, right=right_expr, line=line, position=position
            )

        return left_expr

    def parse_logical_or_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
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
        left = self.parse_logical_xor_expression(context=context)

        while self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=(Operator.OR, Operator.FULL_OR)):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_logical_xor_expression(context=context)
            left = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Logical,
                left=left, operator=operator, right=right, line=line, position=position
            )

        return left

    def parse_logical_xor_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
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
        left = self.parse_logical_and_expression(context=context)

        while self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=(Operator.XOR, Operator.FULL_XOR)):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_logical_and_expression(context=context)
            left = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Logical,
                left=left, operator=operator, right=right, line=line, position=position
            )

        return left

    def parse_logical_and_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
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
        left = self.parse_bitwise_or_expression(context=context)

        while self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=(Operator.AND, Operator.FULL_AND)):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_bitwise_or_expression(context=context)
            left = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Logical,
                left=left, operator=operator, right=right, line=line, position=position
            )

        return left

    def parse_bitwise_or_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
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
        left = self.parse_bitwise_xor_expression(context=context)

        while self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=Operator.BITWISE_OR):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_bitwise_xor_expression(context=context)
            left = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Arithmetic,
                left=left, operator=operator, right=right, line=line, position=position
            )

        return left

    def parse_bitwise_xor_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
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
        left = self.parse_bitwise_and_expression(context=context)

        while self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=Operator.BITWISE_XOR):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_bitwise_and_expression(context=context)
            left = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Arithmetic,
                left=left, operator=operator, right=right, line=line, position=position
            )

        return left

    def parse_bitwise_and_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
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
        left = self.parse_equality_expression(context=context)

        while self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=Operator.BITWISE_AND):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_equality_expression(context=context)
            left = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Arithmetic,
                left=left, operator=operator, right=right, line=line, position=position
            )

        return left

    def parse_equality_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
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
        left = self.parse_comparison_expression(context=context)

        statements = []
        while self.is_consumable(expected_type=TokenType.COMPARISON, expected_value=(
            Comparison.EQUAL,
            Comparison.NOT_EQUAL,
            Comparison.STRICT_EQUAL,
            Comparison.NOT_STRICT_EQUAL,
        )):
            operator = self.consume(expected_type=TokenType.COMPARISON)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_comparison_expression(context=context)

            statements.append(AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Comparison,
                left=left, operator=operator, right=right, line=line, position=position
            ))
            left = right

        if not statements:
            return left
        return self.__parse_chained_comparisons(statements=statements)

    def parse_comparison_expression(self, context: ContextFlag) \
            -> AST.BinaryOperatorABCNode | AST.ASTNode:
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
        left = self.parse_membership_operator_expression(context=context)

        while self.is_consumable(expected_type=TokenType.COMPARISON, expected_value=(
            Comparison.LESSER_OR_EQUAL,
            Comparison.GREATER_OR_EQUAL,
            Comparison.LESSER,
            Comparison.GREATER,
        )):
            operator = self.consume(expected_type=TokenType.COMPARISON)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_membership_operator_expression(context)

            statements.append(AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Comparison,
                left=left, operator=operator, right=right, line=line, position=position
            ))
            left = right

        if not statements:
            return left
        return self.__parse_chained_comparisons(statements=statements)

    @staticmethod
    def __parse_chained_comparisons(statements: list[AST.BinaryOperatorABCNode]) -> AST.BinaryOperatorABCNode:
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
        root = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Logical,
            left=statements[0], operator=Operator.AND, right=None)  # type: ignore
        curr = root
        for index, statement in enumerate(statements):
            if index == 0:
                continue
            elif index != statements_count - 1:
                new_node = AST.BinaryOperatorABCNode(
                    category=AST.OperatorCategory.Logical,
                    left=statement, operator=Operator.AND, right=None)  # type: ignore
                curr.right = new_node
                curr = new_node
            else:
                curr.right = statement
        return root

    def parse_membership_operator_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 9 (medium)
        Associativity: none
        Tokens: in
        :param context: scope context flag
        :return: Arithmetic operator node if bitwise conjunction is present,
        otherwise anything the next precedence (equality operators) parser will return.
        """
        left = self.parse_bitwise_shift_expression(context=context)

        if self.is_consumable(expected_type=TokenType.COMPARISON, expected_value=Comparison.MEMBERSHIP_OPERATOR):
            operator = self.consume(expected_type=TokenType.COMPARISON, expected_value=Comparison.MEMBERSHIP_OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_bitwise_shift_expression(context=context)
            left = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Comparison,
                left=left, operator=operator, right=right, line=line, position=position
            )

        return left

    def parse_bitwise_shift_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 10 (upper-medium)
        Associativity: left-to-right
        Tokens: >>, <<
        :param context: scope context flag
        :return: Arithmetic operator node if bitwise shift operators are present,
        otherwise anything the next precedence (additive operators) parser will return.
        """
        left = self.parse_additive_expression(context=context)

        while self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=(
            Operator.BITWISE_LSHIFT,
            Operator.BITWISE_RSHIFT
        )):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_additive_expression(context=context)
            left = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Comparison,
                left=left, operator=operator, right=right, line=line, position=position
            )

        return left

    def parse_additive_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 11 (upper-medium)
        Associativity: left-to-right
        Tokens: +, -
        :param context: scope context flag
        :return: Arithmetic operator node if additive operators are present,
        otherwise anything the next precedence (multiplicative operators) parser will return.
        """
        left = self.parse_multiplicative_expression(context=context)

        while self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=(Operator.PLUS, Operator.MINUS)):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_multiplicative_expression(context=context)
            left = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Arithmetic,
                left=left, operator=operator, right=right, line=line, position=position
            )

        return left

    def parse_multiplicative_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 12 (upper)
        Associativity: left-to-right
        Tokens: *, /, %, //
        :param context: scope context flag
        :return: Arithmetic operator node if multiplicative operators are present,
        otherwise anything the next precedence (unary sign operator) parser will return.
        """
        left = self.parse_arithmetic_unary_expression(context=context)

        while self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=(
            Operator.MULTIPLY,
            Operator.DIVIDE,
            Operator.FLOOR_DIVIDE,
            Operator.MODULO,
        )):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_arithmetic_unary_expression(context=context)
            left = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Arithmetic,
                left=left, operator=operator, right=right, line=line, position=position
            )

        return left

    def parse_arithmetic_unary_expression(
            self, context: ContextFlag
            ) -> AST.UnaryOperatorABCNode | AST.BinaryOperatorABCNode | AST.ASTNode:
        """
        Operator parser.
        Operator type: unary
        Precedence: 13 (upper)
        Associativity: none
        Tokens: +, -, ~
        :param context: scope context flag
        :return: Unary operator node if multiplicative unary operators are present,
        otherwise anything the next precedence (power operator) parser will return.
        """
        if self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=(
            Operator.PLUS,
            Operator.MINUS,
            Operator.BITWISE_INVERSE,
        )):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_power_expression(context=context)
            return AST.UnaryOperatorABCNode(
                category=AST.OperatorCategory.Arithmetic,
                operator=operator, expression=right, line=line, position=position
            )
        else:
            return self.parse_power_expression(context=context)

    def parse_power_expression(self, context: ContextFlag) -> AST.BinaryOperatorABCNode | AST.ASTNode:
        """
        Operator parser.
        Operator type: binary
        Precedence: 14 (upper)
        Associativity: right to left
        Tokens: **
        :param context: scope context flag
        :return: Arithmetic operator node if power operators are present,
        otherwise anything the next precedence (other unary) parser will return.
        """
        left = self.parse_other_unary_expression(context=context)
        right_expressions = [left]
        operators_positions = []

        while self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=Operator.POWER):
            _ = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_other_unary_expression(context=context)
            right_expressions.append(right)
            operators_positions.append((line, position))

        if len(right_expressions) == 1:
            return left

        result = AST.BinaryOperatorABCNode(
            category=AST.OperatorCategory.Arithmetic,
            left=right_expressions[-2], operator=Operator.POWER, right=right_expressions[-1],
            line=operators_positions[-1][0], position=operators_positions[-1][1]
        )
        for _left, (_line, _position) in reversed(list(zip(right_expressions[:-2], operators_positions[:-1]))):
            result = AST.BinaryOperatorABCNode(
                category=AST.OperatorCategory.Arithmetic,
                left=_left, operator=Operator.POWER, right=result,
                line=_line, position=_position
            )

        return result

    # TODO: reference/dereference
    def parse_other_unary_expression(
            self, context: ContextFlag
            ) -> AST.UnaryOperatorABCNode | AST.ASTNode | AST.MemberOperatorNode:
        """
        Operator parser.
        Operator type: unary
        Precedence: 15 (high)
        Associativity: right to left
        Tokens: not, [reference, dereference]
        :param context: scope context flag
        :return: Unary operator node if other unary operators (logical not, reference operators) are present,
        otherwise anything the next precedence (dynamic memory allocation) parser will return.
        """
        if self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=(Operator.NOT, )):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_dynamic_memory_allocation(context=context)
            return AST.UnaryOperatorABCNode(
                category=AST.OperatorCategory.Logical,
                operator=operator, expression=right, line=line, position=position
            )
        elif self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=(Operator.REFERENCE, Operator.DEREFERENCE)):
            operator = self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_identifier(context=context, pure_identifier=True)
            return AST.UnaryOperatorABCNode(
                category=AST.OperatorCategory.Reference,
                operator=operator, expression=right, line=line, position=position
            )
        else:
            return self.parse_dynamic_memory_allocation(context=context)

    def parse_dynamic_memory_allocation(
            self, context: ContextFlag
            ) -> AST.UnaryOperatorABCNode | AST.ASTNode | AST.MemberOperatorNode:
        """
        Operator parser.
        Operator type: unary
        Precedence: 16 (high)
        Associativity: none (non-stackable)
        Tokens: new, delete
        :param context: scope context flag
        :return: Allocation operator node if other unary operators dynamic memory allocation are present,
        otherwise anything the next precedence (member access) parser will return.
        """
        if self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=Operator.NEW_INSTANCE):
            operator = self.consume(expected_type=TokenType.OPERATOR, expected_value=Operator.NEW_INSTANCE)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_base_type(context=context, as_constructor=True)
            return AST.UnaryOperatorABCNode(
                category=AST.OperatorCategory.Allocation,
                operator=operator, expression=right, line=line, position=position
            )
        elif self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=Operator.DELETE_INSTANCE):
            operator = self.consume(expected_type=TokenType.OPERATOR, expected_value=Operator.DELETE_INSTANCE)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_identifier(context=context, pure_identifier=True)
            return AST.UnaryOperatorABCNode(
                category=AST.OperatorCategory.Allocation,
                operator=operator, expression=right, line=line, position=position
            )
        else:
            return self.parse_primary_expression(context=context)  # not sure

    # TODO: string adequate parser, comments, refactor it into methods ...
    def parse_primary_expression(self, context: ContextFlag) -> AST.ASTNode:
        if self.is_consumable(expected_type=(
            TokenType.DECIMAL_INTEGER_LITERAL,
            TokenType.HEXADECIMAL_INTEGER_LITERAL,
            TokenType.OCTAL_INTEGER_LITERAL,
            TokenType.BINARY_INTEGER_LITERAL
        )):
            return self.parse_integer()

        if self.is_consumable(expected_type=TokenType.IMAGINARY_FLOAT_LITERAL):
            value = self.consume(expected_type=TokenType.IMAGINARY_FLOAT_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return AST.ImaginaryFloatLiteralNode(value=value, line=line, position=position)

        if self.is_consumable(expected_type=TokenType.FLOAT_LITERAL):
            value = self.consume(expected_type=TokenType.FLOAT_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return AST.FloatLiteralNode(value=value, line=line, position=position)

        if self.is_consumable(expected_type=TokenType.IDENTIFIER):
            return self.parse_identifier(context=context, pure_identifier=False)

        if self.is_consumable(expected_type=TokenType.STRING_LITERAL):
            return self.parse_string()

        if self.is_consumable(expected_type=TokenType.CHAR_LITERAL):
            value = self.consume(expected_type=TokenType.CHAR_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return AST.CharLiteralNode(value=value, line=line, position=position)

        if self.is_consumable(expected_type=TokenType.BOOLEAN_LITERAL):
            value = self.consume(expected_type=TokenType.BOOLEAN_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return AST.BooleanLiteralNode(value=value, line=line, position=position)

        if self.is_consumable(expected_type=TokenType.NULL_LITERAL):
            _ = self.consume(expected_type=TokenType.NULL_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return AST.NullLiteralNode(line=line, position=position)

        if self.is_consumable(expected_type=TokenType.UNDEFINED_LITERAL):
            _ = self.consume(expected_type=TokenType.UNDEFINED_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return AST.UndefinedLiteralNode(line=line, position=position)

        if self.is_consumable(expected_type=TokenType.BYTE_STRING_LITERAL):
            value = self.consume(expected_type=TokenType.BYTE_STRING_LITERAL)
            line, position = self.line_and_position_of_consumed_token()
            return AST.ByteStringLiteralNode(value=value, line=line, position=position)

        if self.is_consumable(expected_type=TokenType.KEYWORD, expected_value=Keyword.THIS):
            return self.parse_this_keyword(context=context)

        if self.is_consumable(expected_type=TokenType.OPENING_PARENTHESIS):
            self.consume(expected_type=TokenType.OPENING_PARENTHESIS)
            node = self.parse_arithmetic_expression(context)
            self.consume(expected_type=TokenType.CLOSING_PARENTHESIS)
            return node
        if self.is_consumable(expected_type=TokenType.OPENING_SQUARE_BRACKET):
            return self.parse_square_bracket_literal_expression(context)

        if self.is_consumable(expected_type=(TokenType.SIMPLE_TYPE, TokenType.COMPOUND_TYPE, TokenType.TYPE_MODIFIER)):
            return self.parse_type_declaration(context=context)

        self.error(msg=f"Unexpected token {self.current_token.value}")

    def parse_integer(self) -> AST.IntegerLiteralNode:
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
            self.error(msg=f"Unexpected token {token_type}")

        value = self.consume(expected_type=token_type)
        line, position = self.line_and_position_of_consumed_token()
        return AST.IntegerLiteralNode(value=value, base=base, line=line, position=position)

    def parse_string(self) -> AST.StringLiteralNode:
        value = self.consume(expected_type=TokenType.STRING_LITERAL)
        line, position = self.line_and_position_of_consumed_token()
        return AST.StringLiteralNode(value=value, line=line, position=position)

    def parse_this_keyword(self, context: ContextFlag) -> AST.ThisNode:
        if not ContextFlag.match(current_context=context, flag=ContextFlag.CLASS & ContextFlag.FUNCTION):
            self.error(msg="Unexpected token 'this' out of class method context")

        _ = self.consume(expected_type=TokenType.KEYWORD, expected_value=Keyword.THIS)
        line, position = self.line_and_position_of_consumed_token()
        previous_result = AST.ThisNode(line=line, position=position)
        return self._parse_indexation_or_function_calls_if_exist(previous_result, context)

    def parse_identifier(
        self,
        context: ContextFlag,
        pure_identifier: bool = False,
        **_
    ) -> AST.IdentifierNode | AST.IndexNode | AST.FunctionCallNode:
        """
        Parse an identifier
        It can be a label to some variable, function or even class

        The next token can be the parenthesis or square bracket expression

        :param context:
        :param pure_identifier: (optional) whether square brackets or
        :return:
        """
        identifier = self.consume(expected_type=TokenType.IDENTIFIER)
        line, position = self.line_and_position_of_consumed_token()
        previous_result = AST.IdentifierNode(name=identifier, line=line, position=position)
        if pure_identifier:
            return previous_result
        return self._parse_indexation_or_function_calls_if_exist(node=previous_result, context=context)

    def _parse_indexation_or_function_calls_if_exist(self, node, context: ContextFlag):
        node = node
        while (
            self.is_consumable(TokenType.OPENING_SQUARE_BRACKET) or
            self.is_consumable(TokenType.OPENING_PARENTHESIS) or
            self.is_consumable(TokenType.OPERATOR, (Operator.OBJECT_MEMBER_ACCESS, Operator.REFERENCE_MEMBER_ACCESS))
        ):
            token = self.current_token
            if token.type == TokenType.OPERATOR:
                node = self._parse_membership_operator(identifier=node, context=context)
            elif token.type == TokenType.OPENING_SQUARE_BRACKET:
                node = self._parse_indexation_call(identifier=node, context=context)
            elif token.type == TokenType.OPENING_PARENTHESIS:
                node = self._parse_function_call(identifier=node, context=context)

        return node

    def _parse_function_call(self, identifier, context: ContextFlag):
        line, position = self.line_and_position_of_consumed_token()
        arguments = self.__parse_parentheses_content(context)
        return AST.FunctionCallNode(identifier=identifier, arguments=arguments, line=line, position=position)

    def _parse_indexation_call(self, identifier, context: ContextFlag):
        line, position = self.line_and_position_of_consumed_token()
        arguments = self.__parse_square_bracket_content(allow_keymaps=False, context=context)
        return AST.IndexNode(variable=identifier, arguments=arguments, line=line, position=position)

    def _parse_membership_operator(self, identifier, context: ContextFlag):
        op = self.consume(expected_type=TokenType.OPERATOR)
        line, position = self.line_and_position_of_consumed_token()
        arguments = self.parse_identifier(context, True)
        return AST.MemberOperatorNode(identifier, op, arguments, line=line, position=position)

    def __parse_square_bracket_content(self, allow_keymaps: bool, context: ContextFlag) -> list[AST.ASTNode]:

        self.consume(expected_type=TokenType.OPENING_SQUARE_BRACKET)
        arguments = []

        while self.current_token.type != TokenType.CLOSING_SQUARE_BRACKET:
            if allow_keymaps:
                argument = self.parse_arithmetic_expression_with_keymaps(context=context)
            else:
                argument = self.parse_arithmetic_expression(context=context)
            arguments.append(argument)

            if self.is_consumable(expected_type=TokenType.CLOSING_SQUARE_BRACKET):
                break
            self.consume(expected_type=TokenType.COMMA)

        self.consume(expected_type=TokenType.CLOSING_SQUARE_BRACKET)
        return arguments

    def __parse_parentheses_content(self, context: ContextFlag) -> list[AST.ASTNode]:
        self.consume(expected_type=TokenType.OPENING_PARENTHESIS)
        arguments = []

        while self.current_token.type != TokenType.CLOSING_PARENTHESIS:
            argument = self.parse_arithmetic_expression(context=context)
            arguments.append(argument)

            if self.is_consumable(expected_type=TokenType.CLOSING_PARENTHESIS):
                break
            self.consume(expected_type=TokenType.COMMA)

        self.consume(expected_type=TokenType.CLOSING_PARENTHESIS)
        return arguments

    def parse_square_bracket_literal_expression(
        self,
        context: ContextFlag
    ) -> AST.ListLiteralNode | AST.KeymapLiteralNode | AST.EmptyLiteralNode:
        arguments = self.__parse_square_bracket_content(allow_keymaps=True, context=context)
        line, position = self.line_and_position_of_consumed_token()

        keymap_literals_count = sum(map(lambda x: isinstance(x, AST.KeymapElementNode), arguments))
        if keymap_literals_count == 0:
            if arguments:
                return AST.ListLiteralNode(elements=arguments, line=line, position=position)
            else:
                return AST.EmptyLiteralNode(line=line, position=position)
        elif keymap_literals_count == len(arguments):
            return AST.KeymapLiteralNode(elements=arguments, line=line, position=position)
        else:
            self.error(msg="List/keymap literal cannot have both keymap and non-keymap expressions")

    def parse_arithmetic_expression_with_keymaps(self, context: ContextFlag) -> AST.KeymapElementNode | AST.BinaryOperatorABCNode:
        # absent associativity
        left = self.parse_arithmetic_expression(context=context)

        if self.is_consumable(expected_type=TokenType.OPERATOR, expected_value=Operator.KEYMAP_LITERAL):
            self.consume(expected_type=TokenType.OPERATOR)
            line, position = self.line_and_position_of_consumed_token()
            right = self.parse_arithmetic_expression(context=context)
            return AST.KeymapElementNode(
                left=left, right=right,
                line=line, position=position
            )
        else:
            return left

    def refine_identifier(
        self,
        node,
        refine_as: Literal["class_name", "constructor"]
    ) -> AST.TypeNode | AST.FunctionCallNode:
        if refine_as == "class_name":
            return self.refine_identifier_as_class_name(node)
        elif refine_as == "constructor":
            if not isinstance(node, AST.FunctionCallNode):
                self.error(msg="Expected parenthesised expression for constructor")
            return AST.FunctionCallNode(
                identifier=self.refine_identifier_as_class_name(node=node.identifier),
                arguments=node.arguments,
                line=node.line,
                position=node.position,
                is_constructor=True,
            )

    def refine_identifier_as_class_name(
        self,
        node
    ) -> AST.TypeNode:
        if isinstance(node, AST.IdentifierNode):
            return AST.TypeNode(
                category=AST.TypeCategory.CLASS,
                type_node=node, args=None, line=node.line, position=node.position
            )
        elif isinstance(node, AST.IndexNode):
            if not isinstance(node.variable, AST.IdentifierNode):
                self.error(msg=f"Invalid class type declaration: {node.variable.__class__.__name__}")
            return AST.TypeNode(
                category=AST.TypeCategory.GENERIC_CLASS,
                type_node=node.variable,
                args=[self.refine_identifier_as_class_name(node=x) for x in node.arguments],
                line=node.line,
                position=node.position
            )
        elif isinstance(node, AST.TypeNode):
            if node.category in (AST.TypeCategory.PRIMITIVE, AST.TypeCategory.COLLECTION):
                return node
        else:
            self.error(msg=f"Invalid class type declaration: {node.__class__.__name__}")
