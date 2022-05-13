from lexer import TokenType
from ast import BuiltinFunction
from error import SemanticError, ErrorCode
from library import FUNCTIONS
from linked_dict import LinkedDict
from type import Value, bv
    

class Interpreter(object):
    def __init__(self, parser):
        self.parser = parser
        self.scopes = LinkedDict()

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))

    def visit_UnaryOperator(self, node) -> Value:
        v = self.visit(node.expression)
        value = bv(v.type, v.value).unary_operator(node.operator)
        if value is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)
        return value()

    def visit_BinaryOperator(self, node) -> Value:
        l = self.visit(node.expr_left)
        r = self.visit(node.expr_right)
        value = bv(l.type, l.value).binary_operator(node.operator, bv(r.type, r.value))
        if value is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)
        return value()

    def visit_Val(self, node) -> Value:
        return bv(node.type, node.value)

    def visit_Variable(self, node) -> Value:
        var_name = node.value
        if var_name not in self.scopes:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)
        else:
            return self.scopes.get(var_name)
            
    def visit_NoOperation(self, node) -> None:
        pass
        
    def visit_DeclarationStatement(self, node) -> None:
        val = self.visit(node.expression)
        if node.name.value in self.scopes.peek():
            self.error(ErrorCode.DUPLICATE_ID, node.name.token)
        self.scopes.insert(node.name.value, bv(node.type, val.value))

    def visit_AssignmentStatement(self, node) -> None:
        name = node.name.value
        val = self.visit(node.expression)
        if name not in self.scopes:
            self.error(ErrorCode.ID_NOT_FOUND, node.name.token)
        if node.operator == TokenType.ASSIGN:
            self.scopes.set(name, bv(self.scopes.get(name).type, val.value))
        else:
            value = self.scopes.get(name).assignment_operator(node.operator, val)
            if value is None:
                self.error(ErrorCode.MISMATCHED_TYPE, node.token)
            self.scopes.set(name, bv(self.scopes.get(name).type, value().value))
        return

    def visit_Block(self, node) -> None:
        self.scopes.push()
        for child in node.children:
            self.visit(child)
        self.scopes.pop()

    def visit_IfElse(self, node) -> None:
        for e in node.conditional:
            if self.visit(e[0]).value:
                self.visit(e[1])
                return
        if node.otherwise != None:
            self.visit(node.otherwise)

    def visit_ForLoop(self, node) -> None:
        self.visit(node.init)
        while self.visit(node.condition).value:
            self.visit(node.block)
            self.visit(node.increment)

    def visit_WhileLoop(self, node) -> None:
        while self.visit(node.condition).value:
            self.visit(node.block)

    def visit_DoWhile(self, node) -> None:
        self.visit(node.block)
        while self.visit(node.condition).value:
            self.visit(node.block)

    def visit_FunctionDeclaration(self, node) -> None:
        if node.name.value in self.scopes.peek():
            self.error(ErrorCode.DUPLICATE_ID, node.name.token)
        self.scopes.insert(node.name.value, (node.type, node.args, node.body))

    def visit_FunctionCall(self, node):
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
        self.visit(function[2])
        self.scopes.pop()
        self.scopes.top = top

    def visit_BuiltinFunction(self, node):
        FUNCTIONS[node.name].run(self.scopes)

    def visit_Program(self, node):
        for function in node.functions:
            self.visit(function)

    def interpret(self):
        tree = self.parser.parse()
        for name, func in FUNCTIONS.items():
            self.scopes.insert(name, (func.type, func.args, BuiltinFunction(name)))
        self.visit(tree)
        self.visit(self.scopes.get("main")[2])

    def error(self, error_code, token):
        """Throws an error and states the current character, line, and column on which the error happened"""
        raise SemanticError(f"{error_code.value} -> {token}")
