from frontend.abstract_syntax_tree import ClassDefNode, ClassMethodDeclarationNode

from ..shared import error_logger, class_definitions

from .._type_validate import validate_type

from .inheritance import validate_class_inheritance
from .._overloads import validate_overloaded_function_definitions
from .._scope import validate_scope

from .._helpers_function import instantiate_environment_from_function_parameters


def validate_all_class_definitions() -> bool:
    """
    Validate all class definitions in the program
    :return: True if all classes are valid, False otherwise
    """
    # 1. Check if class definitions are duplicated
    has_no_duplicates = _check_no_duplicate_class_definitions()
    if not has_no_duplicates:
        return False

    # 2. Check if fields inside them are duplicated or not
    # and if types and default values are valid
    no_field_duplicates = [
        _flat_check_no_duplicate_fields(concrete_class)
        for concrete_class in class_definitions
    ]

    valid_field_types = [
        _flat_check_field_types(concrete_class)
        for concrete_class in class_definitions
    ]

    # 3. Check if methods inside classes are not duplicated in terms of overloading etc
    no_method_collisions = [
        _flat_check_no_method_collisions(concrete_class)
        for concrete_class in class_definitions
    ]

    if not (no_field_duplicates and valid_field_types and no_method_collisions):
        return False

    # 3. Validate classes themselves
    # (inheritance, methods content, has constructor...)
    valid_classes = [
        _validate_class_definition(concrete_class)
        for concrete_class in class_definitions
    ]
    return all(valid_classes)


# noinspection DuplicatedCode
def _check_no_duplicate_class_definitions() -> bool:
    """
    (Hidden) Check if there are no duplicate class definitions in the program
    :return: True if there are no duplicate class definitions in the program, False otherwise
    """
    # 1. check if the names are repeating
    distinct_classes = set()
    repeated_classes = set()
    for class_definition in class_definitions:
        name = class_definition.name
        if name not in distinct_classes:
            distinct_classes.add(name)
            continue
        else:
            repeated_classes.add(name)

    # 2. If there are, error log every duplicate definition
    for class_definition in class_definitions:
        if class_definition.name in repeated_classes:
            class_definition.valid = False
            error_logger.add(
                class_definition,
                f"Repeated class name: {class_definition.name}"
            )

    return not repeated_classes


# noinspection DuplicatedCode
def _flat_check_no_duplicate_fields(
    concrete_class: ClassDefNode
) -> bool:
    """
    (Hidden)
    Check if there are no duplicated field names in the current class
    (Doesn't care about superclasses for now)
    :param concrete_class:
    :return:
    """
    fields_definitions = concrete_class.fields_definitions + concrete_class.static_fields_defs

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
            field_definition.valid = False
            error_logger.add(
                field_definition.location,
                f"Repeated field name: {field_definition.name}"
            )

    if repeated_fields:
        concrete_class.valid = False
    return not repeated_fields


def _flat_check_field_types(
    concrete_class: ClassDefNode
) -> bool:

    valid_field_types = True
    for f in concrete_class.all_fields_definitions:
        valid_type = validate_type(f.type, concrete_class.generic_params)

        # Validation end: ClassFieldDeclarationNode
        f.valid = valid_type

        if not valid_type:
            valid_field_types = False

    if not valid_field_types:
        concrete_class.valid = False
    return valid_field_types


def _flat_check_no_method_collisions(
    concrete_class: ClassDefNode
) -> bool:
    all_methods = concrete_class.static_methods_defs + concrete_class.methods_defs
    valid_overloads = validate_overloaded_function_definitions(all_methods)
    if not valid_overloads:
        return False

    valid = True
    for static_method in concrete_class.static_methods_defs:
        if not static_method.is_public:
            error_logger.add(
                static_method.location,
                "Static method cannot be non-public"
            )
            static_method.valid = False
            valid = False
        if static_method.is_virtual:
            error_logger.add(
                static_method.location,
                "Static method cannot be virtual"
            )
            static_method.valid = False
            valid = False
        if static_method.is_overload:
            error_logger.add(
                static_method.location,
                "Static method cannot be overloaded"
            )
            static_method.valid = False
            valid = False
    if not valid:
        concrete_class.valid = False
    return valid


def _validate_class_definition(
    concrete_class: ClassDefNode
) -> bool:
    # For now,
    # duplicate classes, fields and methods are checked

    # 1. Check inheritance
    valid_inheritance = validate_class_inheritance(concrete_class)
    if not valid_inheritance:
        concrete_class.valid = False
        return False

    valid_static_methods = [
        validate_static_method_definition(
            concrete_class,
            static_method
        )
        for static_method in concrete_class.methods_defs
    ]

    valid_methods = [
        validate_method_definition(
            concrete_class,
            method
        )
        for method in concrete_class.methods_defs
    ]
    everything_is_valid = all((
        all(valid_methods),
        all(valid_static_methods),
    ))

    # Validation end: ClassDefinitionNode
    concrete_class.valid = everything_is_valid
    return everything_is_valid


def validate_method_definition(
    concrete_class: ClassDefNode,
    method: ClassMethodDeclarationNode
) -> bool:
    valid_return_type = validate_type(method.return_type, concrete_class.generic_params)
    valid_signature = (
        all((validate_type(param, concrete_class.generic_params) for param in method.parameters_signature))
    )
    valid_implementation = validate_scope(
        scope=method.function_body,
        environment=instantiate_environment_from_function_parameters(method.parameters),
        is_loop=False,
        is_function=True,
        is_class=True,
        expected_return_type=method.return_type,
        current_class=concrete_class,
        is_class_nonstatic_method=True,
        outermost_function_scope=True,
    )

    # Validation end: ClassMethodDeclarationNode (1/2)
    valid_method = all((
        valid_return_type,
        valid_signature,
        valid_implementation
    ))
    method.valid = valid_method
    return valid_method


def validate_static_method_definition(
    concrete_class: ClassDefNode,
    method: ClassMethodDeclarationNode
) -> bool:
    valid_return_type = validate_type(method.return_type, concrete_class.generic_params)
    valid_signature = (
        all((validate_type(param, concrete_class.generic_params) for param in method.parameters_signature))
    )
    valid_implementation = validate_scope(
        scope=method.function_body,
        environment=instantiate_environment_from_function_parameters(method.parameters),
        is_loop=False,
        is_function=True,
        is_class=True,
        expected_return_type=method.return_type,
        current_class=concrete_class,
        is_class_nonstatic_method=False,
        outermost_function_scope=True,
    )

    # Validation end: ClassMethodDeclarationNode (2/2)
    valid_method = all((
        valid_return_type,
        valid_signature,
        valid_implementation
    ))
    method.valid = valid_method
    return valid_method
