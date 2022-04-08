from lexer import Token
from parser import Parser
from error import error
from collections import namedtuple

Return = namedtuple("Return", "type value")

class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        ret = visitor(node)
        if ret == None:
            return Return("null", "null")
        return ret

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visit_UnaryOp(self, node):
        op = node.op.type
        v = self.visit(node.expr)
        if op == Token.MINUS:
            return Return(v.type, -self.visit(node.expr).value)

    def visit_BinOp(self, node):
        l = self.visit(node.left)
        r = self.visit(node.right)
        type = "float" if "float" in (l.type, r.type) else "int"
        if node.op.type == Token.PLUS:
            return Return(type, l.value + r.value)
        elif node.op.type == Token.MINUS:
            return Return(type, l.value - r.value)
        elif node.op.type == Token.MUL:
            return Return(type, l.value * r.value)
        elif node.op.type == Token.DIV and type == "float":
            return Return(type, l.value / r.value)
        else:
            return Return(type, l.value // r.value)

    def visit_Num(self, node):
        if node.token.type == Token.FLOATC:
            return Return("float", node.value)
        elif node.token.type == Token.INTC:
            return Return("int", node.value)

    def visit_Block(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Declare(self, node):
        var_type = node.type.value
        var_name = node.left.value
        var_visit = self.visit(node.right)
        if var_name in self.GLOBAL_SCOPE:
            error(f"Redeclaration of {var_name}")
        if var_type == "int" and var_visit.type == "float":
            self.GLOBAL_SCOPE[var_name] = Return("int", int(var_visit.value))
        elif var_type == "float" and var_visit.type == "int":
            self.GLOBAL_SCOPE[var_name] = Return("float", float(var_visit.value))
        elif var_type == var_visit.type:
            self.GLOBAL_SCOPE[var_name] = var_visit
        else:
            error(f"Mismatched types, expected {var_type} found {var_visit.type}")

    def visit_Assign(self, node):
        var_name = node.left.value
        var_visit = self.visit(node.right)
        if var_name not in self.GLOBAL_SCOPE:
            error(f"Unknown symbol: {var_name}")
        if self.GLOBAL_SCOPE[var_name].type == "int" and var_visit.type == "float":
            self.GLOBAL_SCOPE[var_name] = Return("int", int(var_visit.value))
        elif self.GLOBAL_SCOPE[var_name].type == "float" and var_visit.type == "int":
            self.GLOBAL_SCOPE[var_name] = Return("float", float(var_visit.value))
        elif self.GLOBAL_SCOPE[var_name].type == var_visit.type:
            self.GLOBAL_SCOPE[var_name] = var_visit
        else:
            error(f"Mismatched types, expected {self.GLOBAL_SCOPE[var_name].type} found {var_visit.type}")
        

    def visit_Type(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            error(f"Unknown symbol: {repr(var_name)}")
        else:
            return val        

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
