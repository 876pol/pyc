from ast import FunctionArgument
from tokens import Token, TokenType
from type import build_value
from error import ReturnException
import sys


class LibraryFunction(object):
    """
    Class that represents a builtin function.

    Attributes:
        type (TokenType): the return type of the function.
        args (list[FunctionArgument]): the function arguments.
    """
    type = None
    args = None

    def run(scopes):
        """The function body."""
        pass


"""
The next three classes are for adding functions to print ints, floats, and strings.
"""


class printi(LibraryFunction):
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.INT, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)


class printf(LibraryFunction):
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.FLOAT, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)


class prints(LibraryFunction):
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.STRING, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)


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


class inputi(LibraryFunction):
    type = TokenType.INT
    args = []

    def run(scopes):
        raise ReturnException(build_value(TokenType.INT, int(next())))


class inputf(LibraryFunction):
    type = TokenType.FLOAT
    args = []

    def run(scopes):
        raise ReturnException(build_value(TokenType.FLOAT, float(next())))


class inputs(LibraryFunction):
    type = TokenType.STRING
    args = []

    def run(scopes):
        raise ReturnException(build_value(TokenType.STRING, next()))


class inputl(LibraryFunction):
    type = TokenType.STRING
    args = []

    def run(scopes):
        raise ReturnException(build_value(TokenType.STRING, next_line()))


# Add all functions defined earlier into a dictionary.
LIBRARY_FUNCTIONS = {
    func.__name__: func
    for func in LibraryFunction.__subclasses__()
}
