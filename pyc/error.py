"""
ICS3U
Paul Chen
This files holds the code for all the errors that are used in the interpreter.
"""

from enum import Enum


class ErrorCode(Enum):
    """Enum for various types of errors that the interpreter may encounter."""
    UNEXPECTED_TOKEN = "Unexpected token"
    ID_NOT_FOUND = "Identifier not found"
    DUPLICATE_ID = "Duplicate id found"
    MISMATCHED_TYPE = "Mismatched type"
    MISMATCHED_ARGS = "Mismatched arguments"
    BREAK_OR_CONTINUE_WITHOUT_LOOP = "Break or continue without loop"
    INVALID_MAIN = "Invalid main function"
    OUT_OF_BOUNDS = "Out of bounds"
    ARRAY_AS_FUNCTION_RETURN = "Array as function return"


class LexerError(Exception):
    """Error that occurs in the lexer."""
    pass


class ParserError(Exception):
    """Error that occurs in the parser."""
    pass


class InterpreterError(Exception):
    """Error that occurs in the interpreter."""
    pass
