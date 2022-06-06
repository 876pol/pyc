from collections import namedtuple

from tokens import Token, TokenType


class AST(object):
    """Class that represents a node in the abstract syntax tree."""
    pass


class UnaryOperator(AST):
    """
    Node that represents a unary operator.

    Attributes:
        operator (TokenType): the operator.
        expression (AST): expression that returns a value.
        token (Token): the token that is printed when an error is thrown.
    """

    def __init__(self, operator: TokenType, expression: AST, token: Token = None):
        self.operator = operator
        self.expression = expression
        self.token = token


class BinaryOperator(AST):
    """
    Node that represents a binary operator.

    Attributes:
        operator (TokenType): the operator.
        expr_left, expr_right (AST): the two expressions that the operator will act upon.
        token (Token): the token that is printed when an error is thrown.
    """

    def __init__(self, expr_left: AST, operator: TokenType, expr_right: AST, token: Token = None):
        self.expr_left = expr_left
        self.operator = operator
        self.expr_right = expr_right
        self.token = token


class CastOperator(AST):
    """
    Node that represents a cast operator.

    Attributes:
        operator (TokenType): the operator.
        expression (AST): expression that returns a value.
        token (Token): the token that is printed when an error is thrown.
    """

    def __init__(self, operator: TokenType, expression: AST, token: Token = None):
        self.operator = operator
        self.expression = expression
        self.token = token


class Val(AST):
    """
    Node that represents a value (int, float, or string literal).

    Attributes:
        type (TokenType): the type of value held.
        value (Any): the value that is being held by the type.
    """

    def __init__(self, token: Token):
        self.type = token.type
        self.value = token.value


class Variable(AST):
    """
    Node that represents a variable.

    Attributes:
        type (TokenType): the type of value that will be held.
        value (object): the value that is being held by the variable.
        token (Token): the token that is printed when an error is thrown.
    """

    def __init__(self, type: TokenType, value: object, token: Token = None):
        self.type = type
        self.value = value
        self.token = token


class DeclarationStatement(AST):
    """
    Node that represents a declaration statement.

    Attributes:
        type (TokenType): the type of variable that is declared.
        name (Variable): the name of the variable.
        expression (AST): the value that the variable will be assigned to.
    """

    def __init__(self, type: TokenType, name: Variable, expression: AST):
        self.type = type
        self.name = name
        self.expression = expression


class AssignmentStatement(AST):
    """
    Node that represents an assignment statement.

    Attributes:
        name (Variable): the name of the variable.
        operator (TokenType): the operator.
        expression (AST): the expression that the variable will be assigned to.
        token (Token): the token that is printed when an error is thrown.
    """

    def __init__(self, name: Variable, operator: TokenType, expression: AST, token: Token = None):
        self.name = name
        self.operator = operator
        self.expression = expression
        self.token = token


class Block(AST):
    """
    Node that represents a block of code.

    Attributes:
        children (list[AST]): list of AST nodes to run.
    """

    def __init__(self, children: list):
        self.children = children


class IfElse(AST):
    """
    Node that represents an if-else statement.

    Attributes:
        conditional (list[tuple[AST, Block]]): list of conditions and respective blocks of code 
        to run. Represents all the if and else if blocks.
        otherwise (Block): block of code to run if no conditions have been met. This is `None` 
        if there is no else block.
    """

    def __init__(self, conditional: list, otherwise: Block):
        self.conditional = conditional
        self.otherwise = otherwise


class ForLoop(AST):
    """
    Node that represents a for loop.

    Attributes:
        init (AST): code that initializes a value.
        condition (AST): keeps running the loop while `condition` is true.
        increment (AST): runs this code every time the loop finishes.
        block (Block): code to loop through.
    """

    def __init__(self, init: AST, condition: AST, increment: AST, block: Block):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.block = block


class WhileLoop(AST):
    """
    Node that represents a while loop.

    Attributes:
        condition (AST): keeps running the loop while `condition` is true.
        block (Block): code to loop through.
    """

    def __init__(self, condition: AST, block: Block):
        self.condition = condition
        self.block = block


class DoWhile(AST):
    """
    Node that represents a do-while loop.

    Attributes:
        condition (AST): keeps running the loop while `condition` is true.
        block (Block): code to loop through.
    """

    def __init__(self, condition: AST, block: Block):
        self.condition = condition
        self.block = block


FunctionArgument = namedtuple("FunctionArgument", "type name")


class FunctionDeclaration(AST):
    """
    Node that represents a function declaration.

    Attributes:
        type (TokenType): the return value of the function.
        name (Variable): the name of the function.
        args (list[FunctionArgument]): arguments that the function will take.
        body (Block): main body of the function.
    """

    def __init__(self, type: TokenType, name: Variable, args: list, body: Block):
        self.type = type
        self.name = name
        self.args = args
        self.body = body


class FunctionCall(AST):
    """
    Node that represents a function call.

    Attributes:
        name (str): the name of the function.
        args (list[FunctionArgument]): arguments to put into the function.
        token (Token): the token that is printed when an error is thrown.
    """

    def __init__(self, name: str, args: list, token: Token = None):
        self.name = name
        self.args = args
        self.token = token


class BuiltinFunction(AST):
    """
    Node that represents a builtin function.

    Attributes:
        name (str): the name of the function.
    """

    def __init__(self, name: str):
        self.name = name


class BreakStatement(AST):
    """
    Node the represents a break statement.

    Attributes:
        token (Token): the "break" token, used when printing error messages.
    """

    def __init__(self, token: Token = None):
        self.token = token


class ContinueStatement(AST):
    """
    Node the represents a continue statement.

    Attributes:
        token (Token): the "continue" token, used when printing error messages.
    """

    def __init__(self, token: Token = None):
        self.token = token


class ReturnStatement(AST):
    """
    Node that represents a return statement.

    Attributes:
        expression (AST): the expression to return.
        token (Token): the "return" token, used when printing error messages.
    """

    def __init__(self, expression: AST, token: Token = None):
        self.expression = expression
        self.token = token


class Program(AST):
    """
    Node that represents the program.

    Attributes:
        functions (list[FunctionDeclaration]): list of functions in the program.
    """

    def __init__(self, functions: list):
        self.functions = functions


class NoOperation(AST):
    """Node that does nothing."""
    pass
