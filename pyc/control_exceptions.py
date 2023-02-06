"""
ICS3U
Paul Chen
This file holds the code for the `BreakException`, `ContinueException`, and `ReturnException` classes, which are used
to implement break, continue, and return statements.
"""

from typing import Optional

from tokens import Token
from value import Value


class BreakException(Exception):
    """
    Exception that is raised when a break statement is encountered.

    Attributes:
        token (Optional[Token]): the "break" token, used when printing error messages.
    """

    def __init__(self, token: Optional[Token] = None) -> None:
        self.token = token


class ContinueException(Exception):
    """
    Exception that is raised when a continue statement is encountered.

    Attributes:
        token (Optional[Token]): the "continue" token, used when printing error messages.
    """

    def __init__(self, token: Optional[Token] = None) -> None:
        self.token = token


class ReturnException(Exception):
    """
    Exception that is raised when a return statement is encountered.

    Attributes:
        value (Value): the value to be returned.
        token (Optional[Token]): the "return" token, used when printing error messages.
    """

    def __init__(self, value: Value, token: Optional[Token] = None) -> None:
        self.value = value
        self.token = token
