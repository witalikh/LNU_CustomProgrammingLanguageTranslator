from typing import Sequence
from .ast_node import ASTNode


class ProgramNode(ASTNode):
    def __init__(self, class_definitions, function_definitions, statements):
        self.class_definitions = class_definitions
        self.function_definitions = function_definitions
        self.statements = statements


class GenericTypeNode(ASTNode):
    pass


class BaseTypeNode(GenericTypeNode):
    def __init__(self, type_name):
        self.type_name = type_name


class ArrayTypeNode(GenericTypeNode):
    def __init__(self, element_type: BaseTypeNode, dimensions: Sequence[ASTNode]):
        self.element_type = element_type
        self.dimensions = dimensions


class KeymapTypeNode(GenericTypeNode):
    def __init__(self, key_type, value_type):
        self.key_type = key_type
        self.value_type = value_type


class ConstTypeNode(GenericTypeNode):
    def __init__(self, base_type: GenericTypeNode):
        self.base_type = base_type


class CalculationNode(ASTNode):
    pass


class UnaryOperatorNode(CalculationNode):
    def __init__(self, operator: str, expression: ASTNode):
        self.operator = operator
        self.expression = expression


class AllocationOperatorNode(UnaryOperatorNode):
    pass


class LiteralNode(CalculationNode):
    def __print_tree__(self):
        formatted_name = self.__class__.__name__.replace("LiteralNode", "")
        if hasattr(self, "value"):
            return f"{formatted_name}({self.value})"
        return formatted_name


# class NumericLiteralNode(LiteralNode):
#     def __init__(self, value):
#         self.value = value


class FloatLiteralNode(LiteralNode):
    def __init__(self, value):
        self.value = value


class ImaginaryFloatLiteralNode(LiteralNode):
    def __init__(self, value):
        self.value = value


class StringLiteralNode(LiteralNode):
    def __init__(self, value):
        self.value = value


class ByteLiteralNode(LiteralNode):
    def __init__(self, value):
        self.value = value


class ByteStringLiteralNode(LiteralNode):
    def __init__(self, value):
        self.value = value


class CharLiteralNode(LiteralNode):
    def __init__(self, value):
        self.value = value


class BooleanLiteralNode(LiteralNode):
    def __init__(self, value):
        self.value = value


class NullLiteralNode(LiteralNode):
    pass


class UndefinedLiteralNode(LiteralNode):
    pass


class IndexNode(CalculationNode):
    def __init__(self, variable, arguments):
        self.variable = variable
        self.arguments = arguments


class ListLiteralNode(CalculationNode):
    def __init__(self, elements):
        self.elements = elements


class TemporaryIdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name
        self.type = None
        self.modifiers = 0

    # def __print_tree__(self):
    #     raise ValueError("It shouldn't be in final tree!")


class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name
        self.type = None

    @staticmethod
    def from_temporary(temporary_identifier: "TemporaryIdentifierNode") -> "IdentifierNode":
        result = IdentifierNode(name=temporary_identifier.name)
        result.type = temporary_identifier.type
        return result

    def __print_tree__(self):
        return f"Identifier({self.name})"


class VariableDeclarationNode(ASTNode):
    def __init__(self, _type, name, operator, value):
        self.type = _type
        self.name = name
        self.operator = operator
        self.value = value


class FunctionCallNode(CalculationNode):
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments


class ClassDefinitionNode(ASTNode):
    def __init__(self, class_name):
        self.class_name = class_name


class ScopeNode(ASTNode):
    def __init__(self, statements, local_variables=None):
        self.statements = statements
        self.local_variables = local_variables or []


class IfElseNode(ASTNode):
    def __init__(self, condition, if_scope, else_scope):
        self.condition = condition
        self.if_scope = if_scope
        self.else_scope = else_scope


class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value


class DeductionNode(ASTNode):
    pass

class WhileNode(ASTNode):
    def __init__(self, condition, while_scope):
        self.condition = condition
        self.while_scope = while_scope
