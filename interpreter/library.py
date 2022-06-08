"""
ICS3U
Paul Chen
This file holds all the standard library functions that are implemented in the interpreter.
"""

import sys

from ast import FunctionArgument
from error import ReturnException
from tokens import Token, TokenType
from value import build_value


class LibraryFunction(object):
    """
    Class that represents a builtin function.

    Attributes:
        name (str): the name of the function.
        type (TokenType): the return type of the function.
        args (list[FunctionArgument]): the function arguments.
    """
    name = None
    type = None
    args = None

    def run(scopes):
        """The function body."""
        pass


"""
The next three classes are for adding functions to print ints, floats, and strings.
"""


class PrintInt(LibraryFunction):
    name = "printi"
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.INT, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)


class PrintFloat(LibraryFunction):
    name = "printf"
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.FLOAT, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)


class PrintString(LibraryFunction):
    name = "prints"
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.STRING, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)


class PrintList(LibraryFunction):
    name = "printl"
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.LIST, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        def to_printable_list(curr) -> list:
            ret_val = []
            for e in curr:
                if type(e.value) == list:
                    ret_val.append(to_printable_list(e.value))
                else:
                    ret_val.append(e.value)
            return ret_val
        print(to_printable_list(scopes.get("p").value))


def next():
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


class InputInt(LibraryFunction):
    name = "inputi"
    type = TokenType.INT
    args = []

    def run(scopes):
        raise ReturnException(build_value(TokenType.INTL, int(next())))


class InputFloat(LibraryFunction):
    name = "inputf"
    type = TokenType.FLOAT
    args = []

    def run(scopes):
        raise ReturnException(build_value(TokenType.FLOATL, float(next())))


class InputString(LibraryFunction):
    name = "inputs"
    type = TokenType.STRING
    args = []

    def run(scopes):
        raise ReturnException(build_value(TokenType.STRINGL, next()))


class InputLine(LibraryFunction):
    name = "inputline"
    type = TokenType.STRING
    args = []

    def run(scopes):
        raise ReturnException(build_value(TokenType.STRINGL, next_line()))


# Add all functions defined earlier into a dictionary.
LIBRARY_FUNCTIONS = {
    func.name: func
    for func in LibraryFunction.__subclasses__()
}
