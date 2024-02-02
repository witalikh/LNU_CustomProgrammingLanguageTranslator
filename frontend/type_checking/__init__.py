"""
Package that behaves as singleton object and validates program typing
For the sake of simplicity and efficiency of development, this package
is implemented in functional style with using cross-module shared variables.
All modules, except entrypoint and function-less one, should begin with underscore
and have all functions beginning with underscore unless it's used in another module.
In such way, the inner implementation of separate type-checkers is separated and hidden
from others.
"""

# Code conventions:
# check => returns boolean and some value, possibly error logs
# match => returns boolean, without error logging
# validate => returns boolean, with error logging
# get => gets value or None, with error logging
#
# If function is not gonna be imported anywhere,
# make it private inside a module
