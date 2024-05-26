from .ast_node import ASTNode
from .classes.definition import ClassDefNode
from .functions import FunctionDefNode
from typing import TextIO


class ProgramNode(ASTNode):
    def __init__(
        self,
        class_definitions: list[ClassDefNode],
        function_definitions: list[FunctionDefNode],
        statements: list[ASTNode]
    ):
        super().__init__(line=0, position=0)
        self.class_definitions = class_definitions
        self.function_definitions = function_definitions
        self.statements = statements

    def translate(self, file: TextIO, **kwargs):
        if self.class_definitions:
            self.write_instruction(file, ['REGION', ' ', 'CLASS_DEFNS', '\n'])
            for cls in self.class_definitions:
                cls.translate(file, **kwargs)
                file.write('\n\n')
            self.write_instruction(file, ['ENDREGION', ' ', 'CLASS_DEFNS'])
            file.write('\n\n')

        if self.function_definitions:
            self.write_instruction(file, ['REGION', ' ', 'FUNC_DEFNS', '\n'])
            for fnc in self.function_definitions:
                fnc.translate(file, **kwargs)
                file.write('\n')
            self.write_instruction(file, ['ENDREGION', ' ', 'FUNC_DEFNS'])
            file.write('\n\n')

        for statement in self.statements:
            statement.translate(file, **kwargs)
            file.write('\n')

    def is_valid(self) -> bool:
        return all((
            self.valid,
            all((c.is_valid() for c in self.class_definitions)),
            all((f.is_valid() for f in self.function_definitions)),
            all((s.is_valid() for s in self.statements))
        ))
