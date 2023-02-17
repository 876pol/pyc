"""
ICS3U
Paul Chen
This file holds all the standard library functions that are implemented in the interpreter.
"""

import sys

from ast_nodes import FunctionArgument
from control_exceptions import ReturnException
from tokens import TokenType
from value import build_value


class LibraryFunction(object):
    """
    Class that represents a built-in function.

    Attributes:
        name (str): the name of the function.
        type (TokenType): the return type of the function.
        args (list[FunctionArgument]): the function arguments.
    """
    name = None
    type = None
    args = None

    @staticmethod
    def run(scopes):
        """The function body."""
        pass


class Print(LibraryFunction):
    """Library function that allows for printing a string (other datatypes can be printed through casting)."""
    name = "print"
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.STRING, "p")]

    @staticmethod
    def run(stack):
        print(bytes(stack.get("p").value, "utf-8").decode("unicode_escape"), end="", flush=True)
        raise ReturnException(build_value(TokenType.VOIDL))


def next_token():
    """Reads a token from stdin."""
    token = ""
    while True:
        c = sys.stdin.read(1)
        if not c.isspace():
            token += c
            break
    while True:
        c = sys.stdin.read(1)
        if c.isspace():
            break
        token += c
    return token


def next_line():
    """Reads up to the next newline in stdin."""
    line = ""
    while True:
        c = sys.stdin.read(1)
        if c == "\n":
            break
        line += c
    return line


"""
The next four classes are for adding functions to take ints, floats, and strings as input.
"""


class Scan(LibraryFunction):
    name = "scan"
    type = TokenType.STRING
    args = []

    @staticmethod
    def run(stack):
        raise ReturnException(build_value(TokenType.STRINGL, next_token()))


class GetLine(LibraryFunction):
    name = "getline"
    type = TokenType.STRING
    args = []

    @staticmethod
    def run(stack):
        raise ReturnException(build_value(TokenType.STRINGL, next_line()))


# Add all functions defined earlier into a dictionary.
LIBRARY_FUNCTIONS = {
    func.name: func
    for func in LibraryFunction.__subclasses__()
}
