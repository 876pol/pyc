"""
ICS3U
Paul Chen
This file holds the code for an abstract syntax tree that the code will be parsed into.
"""

from typing import List, Optional, Tuple, Union

from tokens import Token, TokenType


class ASTNode(object):
    """Class that represents a node in the abstract syntax tree."""
    pass


class ValueLiteralNode(ASTNode):
    """
    Node that represents a literal value (int, float, or string).

    Attributes:
        type (TokenType): the type of literal value held.
        value (Union[int, float, str]): the value that is being held.
    """

    def __init__(self, token: Token) -> None:
        self.type = token.type
        self.value = token.value


class InitializerListLiteralNode(ASTNode):
    """
    Node that represents an initializer list.

    Attributes:
        value (List[ASTNode]): the list object held by this node.
    """

    def __init__(self, value: List[ASTNode]) -> None:
        self.value = value


class VariableNode(ASTNode):
    """
    Node that represents a variable.

    Attributes:
        type (TokenType): the type of value that will be held.
        name (str): the name of the variable.
        indices (Optional[List[ASTNode]]): a list of indices for this variable (for arrays).
            Ex. `a[0][0]` would give `indices=[0, 0]`.
        token (Optional[Token]): the token that is printed when an error is thrown.
    """

    def __init__(self, token_type: TokenType, name: str, indices: Optional[List[ASTNode]] = None,
                 token: Optional[Token] = None) -> None:
        if indices is None:
            indices = []
        self.type = token_type
        self.name = name
        self.indices = indices
        self.token = token


class UnaryOperatorNode(ASTNode):
    """
    Node that represents a unary operator.

    Attributes:
        operator (TokenType): the operator.
        operand (ASTNode): the operand.
        token (Optional[Token]): the token that is printed when an error is thrown.
    """

    def __init__(self, operator: TokenType, operand: ASTNode, token: Optional[Token] = None) -> None:
        self.operator = operator
        self.operand = operand
        self.token = token


class BinaryOperatorNode(ASTNode):
    """
    Node that represents a binary operator.

    Attributes:
        operator (TokenType): the operator.
        left_operand (ASTNode): the left-side operand.
        right_operand (ASTNode): the right-side operand.
        token (Optional[Token]): the token that is printed when an error is thrown.
    """

    def __init__(self, left: ASTNode, operator: TokenType, right: ASTNode,
                 token: Optional[Token] = None) -> None:
        self.left_operand = left
        self.operator = operator
        self.right_operand = right
        self.token = token


class CastOperatorNode(ASTNode):
    """
    Node that represents a cast operator.

    Attributes:
        operator (TokenType): the operator.
        operand (ASTNode): the operand.
        token (Optional[Token]): the token that is printed when an error is thrown.
    """

    def __init__(self, operator: TokenType, operand: ASTNode, token: Optional[Token] = None) -> None:
        self.operator = operator
        self.operand = operand
        self.token = token


class DeclarationStatementNode(ASTNode):
    """
    Node that represents a declaration statement.

    Attributes:
        type (TokenType): the type of variable that is declared.
        variable (VariableNode): node that holds information about the variable.
        expression (ASTNode): the expression assigned to the variable.
    """

    def __init__(self, token_type: TokenType, variable: VariableNode, expression: ASTNode) -> None:
        self.type = token_type
        self.variable = variable
        self.expression = expression


class AssignmentStatementNode(ASTNode):
    """
    Node that represents an assignment statement.

    Attributes:
        variable (VariableNode): node that holds information about the variable.
        operator (TokenType): the operator.
        expression (ASTNode): the expression assigned to the variable.
        token (Token): the token that is printed when an error is thrown.
    """

    def __init__(self, variable: VariableNode, operator: TokenType, expression: ASTNode,
                 token: Optional[Token] = None) -> None:
        self.variable = variable
        self.operator = operator
        self.expression = expression
        self.token = token


class BlockStatementNode(ASTNode):
    """
    Node that represents a block of code.

    Attributes:
        statements (list[ASTNode]): list of ASTNodes to run.
    """

    def __init__(self, statements: List[ASTNode]) -> None:
        self.statements = statements


class IfElseStatementNode(ASTNode):
    """
    Node that represents an if-else statement.

    Attributes:
        conditional (list[tuple[ASTNode, ASTNode]]): list of conditions and respective blocks of code
            to run. Represents all the `if` and `else if` blocks.
        otherwise (ASTNode): block of code to run if no conditions have been met. This is `None`
            if there is no else block.
    """

    def __init__(self, conditional: List[Tuple[ASTNode, ASTNode]], otherwise: Optional[ASTNode]) -> None:
        self.conditional = conditional
        self.otherwise = otherwise


class ForLoopNode(ASTNode):
    """
    Node that represents a for loop.

    Attributes:
        initialization (ASTNode): statement that runs prior to entering the for loop.
        condition (ASTNode): condition that determines whether the loop continues running after reaching the end.
        increment (ASTNode): statement that runs at the end of a for loop.
        block (ASTNode): code to loop through.
    """

    def __init__(self, initialization: ASTNode, condition: ASTNode, increment: ASTNode, block: ASTNode) -> None:
        self.initialization = initialization
        self.condition = condition
        self.increment = increment
        self.block = block


class WhileLoopNode(ASTNode):
    """
    Node that represents a while loop.

    Attributes:
        condition (ASTNode): condition that determines whether the loop continues running after reaching the end.
        block (ASTNode): code to loop through.
    """

    def __init__(self, condition: ASTNode, block: ASTNode) -> None:
        self.condition = condition
        self.block = block


class DoWhileLoopNode(ASTNode):
    """
    Node that represents a do-while loop.

    Attributes:
        condition (ASTNode): condition that determines whether the loop continues running after reaching the end.
        block (ASTNode): code to loop through.
    """

    def __init__(self, condition: ASTNode, block: ASTNode) -> None:
        self.condition = condition
        self.block = block


class BreakStatementNode(ASTNode):
    """
    Node the represents a break statement.

    Attributes:
        token (Optional[Token]): the "break" token, used when printing error messages.
    """

    def __init__(self, token: Optional[Token] = None) -> None:
        self.token = token


class ContinueStatementNode(ASTNode):
    """
    Node the represents a continue statement.

    Attributes:
        token (Optional[Token]): the "continue" token, used when printing error messages.
    """

    def __init__(self, token: Optional[Token] = None) -> None:
        self.token = token


class ReturnStatementNode(ASTNode):
    """
    Node that represents a return statement.

    Attributes:
        expression (ASTNode): the expression whose value will be returned.
        token (Optional[Token]): the "return" token, used when printing error messages.
    """

    def __init__(self, expression: ASTNode, token: Optional[Token] = None) -> None:
        self.expression = expression
        self.token = token


class FunctionArgument:
    """
    Class to store information about a function argument.

    Attributes:
        token_type (TokenType): the type of the function argument.
        name (str): the name of the function argument.
        num_dimensions (int): the number of dimensions held by the function argument (needed for arrays).
    """

    def __init__(self, token_type: TokenType, name: str, num_dimensions: int = 0):
        self.type = token_type
        self.name = name
        self.num_dimensions = num_dimensions


class FunctionDeclarationStatementNode(ASTNode):
    """
    Node that represents a function declaration statement.

    Attributes:
        token_type (TokenType): the return type of the function.
        variable (VariableNode): node that holds information about the variable.
        args (List[FunctionArgument]): list of arguments that the function will take.
        body (BlockStatementNode): main body of the function.
    """

    def __init__(self, token_type: TokenType, variable: VariableNode, args: List[FunctionArgument],
                 body: BlockStatementNode) -> None:
        self.type = token_type
        self.variable = variable
        self.args = args
        self.body = body


class FunctionCallStatementNode(ASTNode):
    """
    Node that represents a function call statement.

    Attributes:
        name (str): the name of the function.
        args (List[ASTNode]): list of arguments to put into the function.
        token (Optional[Token]): the token that is printed when an error is thrown.
    """

    def __init__(self, name: str, args: List[ASTNode], token: Optional[Token] = None) -> None:
        self.name = name
        self.args = args
        self.token = token


class BuiltInFunctionCallStatementNode(ASTNode):
    """
    Node that represents a built-in function call statement.

    Attributes:
        name (str): the name of the function.
    """

    def __init__(self, name: str) -> None:
        self.name = name


class ProgramNode(ASTNode):
    """
    Node that represents the program.

    Attributes:
        functions (list[Union[FunctionDeclarationStatementNode, DeclarationStatementNode]]): list of function
            declarations and global variable declarations that make up the program.
    """

    def __init__(self, functions: List[Union[FunctionDeclarationStatementNode, DeclarationStatementNode]]) -> None:
        self.functions = functions


class NoOperationStatementNode(ASTNode):
    """Node that does nothing."""
    pass
