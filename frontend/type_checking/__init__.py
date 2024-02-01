"""
Package that behaves as singleton object and validates program typing
For the sake of simplicity and efficiency of development, this package
is implemented in functional style with using cross-module shared variables.
All modules, except entrypoint and function-less one, should begin with underscore
and have all functions beginning with underscore unless it's used in another module.
In such way, the inner implementation of separate type-checkers is separated and hidden
from others.
"""
pass
