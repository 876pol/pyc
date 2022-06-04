from tokens import Token
from lexer import TokenType
from ast import BuiltinFunction
from error import SemanticError, ErrorCode, BreakException, ContinueException, ReturnException
from library import LIBRARY_FUNCTIONS
from linked_dict import LinkedDict
from parser import Parser
from type import Value, bv


class Interpreter(object):
    """
    Interpreter class that reads an abstract syntax tree and runs the program.

    Attributes:
        parser (Parser): the parser that converts tokens into an abstract syntax tree.
        scopes (LinkedDict): data structure that holds all variables in all scopes.
    """

    def __init__(self, parser: Parser):
        """
        Inits interpreter class.
        Args:
            parser (Parser): the parser.
        """
        self.parser = parser
        self.scopes = LinkedDict()

    def interpret(self):
        """Runs the interpreter."""
        # Runs the parser.
        tree = self.parser.parse()

        # Adds all library functions.
        for name, func in LIBRARY_FUNCTIONS.items():
            self.scopes.insert(
                name, (func.type, func.args, BuiltinFunction(name)))

        # Visits the root node in the abstract syntax tree.
        self.visit(tree)
        self.visit(self.scopes.get("main")[2])

    def visit(self, node) -> Value:
        """
        Visits a node.
        Args:
            node (AST): node to visit.
        Returns:
            Value: the value returned from the node.
        """
        # Runs the corresponding function based on the type of node.
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Throws an error if the corresponding visit method does not exist"""
        raise Exception("No visit_{} method".format(type(node).__name__))

    def visit_UnaryOperator(self, node) -> Value:
        """Visits a UnaryOperator node."""
        v = self.visit(node.expression)
        value = bv(v.type, v.value).unary_operator(node.operator)
        if value is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)
        return value()

    def visit_BinaryOperator(self, node) -> Value:
        """Visits a BinaryOperator node."""
        l = self.visit(node.expr_left)
        r = self.visit(node.expr_right)
        value = bv(l.type, l.value).binary_operator(
            node.operator, bv(r.type, r.value))
        if value is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)
        return value()

    def visit_Val(self, node) -> Value:
        """Visits a Val node."""
        return bv(node.type, node.value)

    def visit_Variable(self, node) -> Value:
        """Visits a Variable node."""
        var_name = node.value
        if var_name not in self.scopes:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)
        else:
            return self.scopes.get(var_name)

    def visit_DeclarationStatement(self, node) -> None:
        """Visits a DeclarationStatement node."""
        val = self.visit(node.expression)
        if node.name.value in self.scopes.peek():
            self.error(ErrorCode.DUPLICATE_ID, node.name.token)
        self.scopes.insert(node.name.value, bv(node.type, val.value))

    def visit_AssignmentStatement(self, node) -> None:
        """Visits an AssignmentStatement node."""
        name = node.name.value
        val = self.visit(node.expression)
        if name not in self.scopes:
            self.error(ErrorCode.ID_NOT_FOUND, node.name.token)
        if node.operator == TokenType.ASSIGN:
            self.scopes.set(name, bv(self.scopes.get(name).type, val.value))
        else:
            value = self.scopes.get(
                name).assignment_operator(node.operator, val)
            if value is None:
                self.error(ErrorCode.MISMATCHED_TYPE, node.token)
            self.scopes.set(
                name, bv(self.scopes.get(name).type, value().value))

    def visit_Block(self, node) -> None:
        """Visits a Block node."""
        self.scopes.push()
        for child in node.children:
            self.visit(child)
        self.scopes.pop()

    def visit_IfElse(self, node) -> None:
        """Visits an IfElse node."""
        for e in node.conditional:
            if self.visit(e[0]).value:
                self.visit(e[1])
                return
        if node.otherwise != None:
            self.visit(node.otherwise)

    def visit_ForLoop(self, node) -> None:
        """Visits a ForLoop node."""
        self.scopes.push()
        self.visit(node.init)
        while self.visit(node.condition).value:
            try:
                self.visit(node.block)
            except BreakException:
                break
            except ContinueException:
                pass
            self.visit(node.increment)
        self.scopes.pop()

    def visit_WhileLoop(self, node) -> None:
        """Visits a WhileLoop node."""
        while self.visit(node.condition).value:
            self.visit(node.block)

    def visit_DoWhile(self, node) -> None:
        """Visits a DoWhile node."""
        self.visit(node.block)
        while self.visit(node.condition).value:
            self.visit(node.block)

    def visit_FunctionDeclaration(self, node) -> None:
        """Visits a FunctionDeclaration node."""
        if node.name.value in self.scopes.peek():
            self.error(ErrorCode.DUPLICATE_ID, node.name.token)
        self.scopes.insert(node.name.value, (node.type, node.args, node.body))

    def visit_FunctionCall(self, node):
        """Visits a FunctionCall node."""
        ret = [self.visit(e) for e in node.args]
        top = self.scopes.top
        self.scopes.top = self.scopes.bottom
        self.scopes.push()
        function = self.scopes.get(node.name)
        if len(function[1]) != len(node.args):
            self.error(ErrorCode.MISMATCHED_ARGS, node.token)
        for i in range(len(function[1])):
            if ret[i].type != function[1][i].type:
                self.error(ErrorCode.MISMATCHED_ARGS, node.token)
            self.scopes.insert(function[1][i].name.value, ret[i])
        ret_val = None
        ret_token = None
        try:
            self.visit(function[2])
        except (BreakException, ContinueException) as ex:
            self.error(ErrorCode.BREAK_OR_CONTINUE_WITHOUT_LOOP, ex.token)
        except ReturnException as ex:
            ret_val = ex.value
            ret_token = ex.token
        self.scopes.pop()
        self.scopes.top = top
        if (ret_val == None and function[0] == "void") or (ret_val != None and ret_val.type == function[0]):
            return ret_val
        else:
            self.error(ErrorCode.MISMATCHED_TYPE, ret_token)

    def visit_BuiltinFunction(self, node):
        """Visits a BuiltinFunction node."""
        return LIBRARY_FUNCTIONS[node.name].run(self.scopes)

    def visit_BreakStatement(self, node):
        raise BreakException(node.token)

    def visit_ContinueStatement(self, node):
        raise ContinueException(node.token)

    def visit_ReturnStatement(self, node):
        raise ReturnException(self.visit(node.expression), node.token)

    def visit_Program(self, node):
        """Visits a Program node."""
        for function in node.functions:
            self.visit(function)

    def visit_NoOperation(self, node) -> None:
        """Visits a NoOperation node."""
        pass

    def error(self, error_code, token):
        """Throws an error and states the current character, line, and column on which the error happened"""
        raise SemanticError(f"{error_code.value} -> {token}")
