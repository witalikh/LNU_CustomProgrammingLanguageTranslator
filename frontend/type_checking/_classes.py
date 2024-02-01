from ..abstract_syntax_tree import *

from .shared import error_logger, class_definitions, function_definitions

from ._environment import validate_type
from ._overloads import validate_overloaded_function_definitions


def validate_all_class_definitions() -> bool:
    has_no_duplicates = _check_no_duplicate_class_definitions()
    valid_classes = [
        _validate_class_definition(concrete_class)
        for concrete_class in class_definitions
    ]
    return has_no_duplicates and all(valid_classes)


# noinspection DuplicatedCode
def _check_no_duplicate_class_definitions() -> bool:
    distinct_classes = set()
    repeated_classes = set()
    for class_definition in class_definitions:
        name = class_definition.class_name
        if name not in distinct_classes:
            distinct_classes.add(name)
            continue
        else:
            repeated_classes.add(name)

    # TODO: generic overloads?
    for class_definition in class_definitions:
        if class_definition.class_name in repeated_classes:
            error_logger.add(
                class_definition,
                f"Repeated class name: {class_definition.class_name}"
            )

    return not repeated_classes


def _validate_class_definition(
    concrete_class: ClassDefinitionNode
) -> bool:
    all_fields = concrete_class.fields_definitions + concrete_class.static_fields_definitions

    has_no_duplicate_fields = check_no_duplicate_fields(all_fields)

    valid_field_types = [
        validate_class_field(field)
        for field in all_fields
    ]

    # TODO: copypaste for methods and check virtuals
    has_no_collided_overloaded_methods = validate_overloaded_function_definitions(
        concrete_class.methods_definitions,
    )

    valid_inheritance = validate_class_inheritance(
        concrete_class,
    )

    valid_static_methods = [
        validate_static_method_definition(
            concrete_class,
            static_method
        )
        for static_method in concrete_class.methods_definitions
    ]

    valid_methods = [
        validate_method_definition(
            concrete_class,
            method
        )
        for method in concrete_class.methods_definitions
    ]

    return all((
        has_no_duplicate_fields,
        all(valid_field_types),
        has_no_collided_overloaded_methods,
        valid_inheritance,
        all(valid_static_methods),
        all(valid_methods)
    ))


# noinspection DuplicatedCode
def check_no_duplicate_fields(
    fields_definitions: list[ClassFieldDeclarationNode],
) -> bool:
    distinct_fields = set()
    repeated_fields = set()
    for field_definition in fields_definitions:
        name = field_definition.name
        if name not in distinct_fields:
            distinct_fields.add(name)
            continue
        else:
            repeated_fields.add(name)

    for field_definition in fields_definitions:
        if field_definition.name in repeated_fields:
            error_logger.add(
                field_definition,
                f"Repeated field name: {field_definition.name}"
            )

    return not repeated_fields


def validate_class_field(
    field: ClassFieldDeclarationNode
) -> bool:
    return validate_type(field)


def validate_class_inheritance(
    concrete_class: ClassDefinitionNode,
) -> bool:
    # TODO: implement
    pass


def validate_static_method_definition(
    concrete_class: ClassDefinitionNode,
    static_method: ClassMethodDeclarationNode
) -> bool:
    # TODO: implement
    pass


def validate_method_definition(
    concrete_class: ClassDefinitionNode,
    method: ClassMethodDeclarationNode
) -> bool:
    # TODO: implement
    pass
