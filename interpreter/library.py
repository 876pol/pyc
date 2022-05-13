from ast import FunctionArgument
from token import Token, TokenType

class LibraryFunction(object):
    type = None
    args = None

    def run(scopes):
        pass


class printi(LibraryFunction):
    type = TokenType.FUNCTION
    args = [FunctionArgument(TokenType.INTC, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)     


class printf(LibraryFunction):
    type = TokenType.FUNCTION
    args = [FunctionArgument(TokenType.FLOATC, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)    
        
        
class prints(LibraryFunction):
    type = TokenType.FUNCTION
    args = [FunctionArgument(TokenType.STRING, Token(TokenType.TYPE, "p"))]

    def run(scopes):
        print(scopes.get("p").value)     


FUNCTIONS = {
    func.__name__ : func
    for func in LibraryFunction.__subclasses__()
}