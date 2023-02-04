"""
ICS3U
Paul Chen
This files holds the code for all custom errors and exceptions
that are used in the interpreter.
"""

from enum import Enum

from tokens import Token
from value import Value


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


class LexerError(Exception):
    """Error that occurs in the lexer."""
    pass


class ParserError(Exception):
    """Error that occurs in the parser."""
    pass


class InterpreterError(Exception):
    """Error that occurs in the interpreter."""
    pass


"""
The following three class aren't really "errors", they're used to 
implement break, continue, and return statements.
"""


class BreakException(Exception):
    """
    Exception that is raised when a break statement is encountered.

    Attributes:
        token (Token): the "break" token, used when printing error messages.
    """

    def __init__(self, token: Token = None):
        self.token = token


class ContinueException(Exception):
    """
    Exception that is raised when a continue statement is encountered.

    Attributes:
        token (Token): the "continue" token, used when printing error messages.
    """

    def __init__(self, token: Token = None):
        self.token = token


class ReturnException(Exception):
    """
    Exception that is raised when a return statement is encountered.

    Attributes:
        value (Value): the value to be returned.
        token (Token): the "return" token, used when printing error messages.
    """

    def __init__(self, value: Value, token: Token = None):
        self.value = value
        self.token = token
