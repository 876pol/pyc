from ast import FunctionArgument
from tokens import Token, TokenType
from type import bv
from error import BreakException, ContinueException, ReturnException


class LibraryFunction(object):
    type = None
    args = None

    def run(scopes):
        pass


class printi(LibraryFunction):
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.INTC, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)


class printf(LibraryFunction):
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.FLOATC, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)


class prints(LibraryFunction):
    type = TokenType.VOID
    args = [FunctionArgument(TokenType.STRING, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)


class InputTokenizer:
    def __init__(self):
        self.tokens = []
        self.curr_ind = 0

    def next(self):
        while self.curr_ind >= len(self.tokens):
            self.curr_ind = 0
            self.tokens = input().split()
        self.curr_ind += 1
        return self.tokens[self.curr_ind - 1]


tokenizer = InputTokenizer()


class inputi(LibraryFunction):
    type = TokenType.INTC
    args = []

    def run(scopes):
        raise ReturnException(bv(TokenType.INTC, int(tokenizer.next())))


class inputf(LibraryFunction):
    type = TokenType.FLOATC
    args = []

    def run(scopes):
        raise ReturnException(bv(TokenType.FLOATC, float(tokenizer.next())))


class inputs(LibraryFunction):
    type = TokenType.STRING
    args = []

    def run(scopes):
        raise ReturnException(bv(TokenType.STRING, tokenizer.next()))


LIBRARY_FUNCTIONS = {
    func.__name__: func
    for func in LibraryFunction.__subclasses__()
}
