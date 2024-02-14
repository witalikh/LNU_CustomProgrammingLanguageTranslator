from ..abstract_syntax_tree import *

from .shared import error_logger, class_definitions, function_definitions

from ._helpers_class import get_class_by_name
from typing import Literal


def get_variable_type_from_environment(
    variable_name: str,
    environment: dict[str, TypeNode],
    location: tuple[int, int]
) -> TypeNode | None:
    if variable_name in environment:
        return environment[variable_name]
    error_logger.add(location, f"Variable '{variable_name}' is not defined in this context.")
    return None
