from ..abstract_syntax_tree import ASTNode


class ErrorLogger:
    def __init__(self):
        self.errors = []

    def add(self, location: ASTNode | tuple[int, int], reason: str) -> None:
        if isinstance(location, ASTNode):
            self.errors.append(
                f"[{location.line}:{location.position}]: {reason}"
            )
        elif isinstance(location, tuple):
            self.errors.append(
                f"[{location[0]}:{location[1]}]: {reason}"
            )

    def __iter__(self):
        return iter(self.errors)
