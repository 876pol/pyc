from lexer import Token
from parser import Parser
from error import error
from collections import namedtuple
from chained_dict import ChainedDict

Return = namedtuple("Return", "type value")

class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        ret = visitor(node)
        if ret == None:
            return Return("null", None)
        return ret

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.scopes = ChainedDict()

    def visit_UnaryOp(self, node):
        op = node.op.type
        v = self.visit(node.expr)
        if op == Token.MINUS:
            return Return(v.type, -self.visit(node.expr).value)
        elif op == Token.BIT_NOT:
            if v.type == "float":
                error("Mismatched types, expected INTC found FLOATC")
            return Return("int", ~self.visit(node.expr).value)
        elif op == Token.LOGICAL_NOT:
            return Return("int", int(not int(self.visit(node.expr).value)))

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
        elif node.op.type == Token.DIV:
            return Return(type, l.value // r.value)
        elif node.op.type == Token.EQUAL:
            return Return("int", int(l.value == r.value))
        elif node.op.type == Token.NOT_EQUAL:
            return Return("int", int(l.value != r.value))
        elif node.op.type == Token.LESS:
            return Return("int", int(l.value < r.value))
        elif node.op.type == Token.GREATER:
            return Return("int", int(l.value > r.value))
        elif node.op.type == Token.LESS_EQUAL:
            return Return("int", int(l.value <= r.value))
        elif node.op.type == Token.GREATER_EQUAL:
            return Return("int", int(l.value >= r.value))
        elif node.op.type == Token.LOGICAL_AND:
            return Return("int", int(bool(l.value) and bool(r.value)))
        elif node.op.type == Token.LOGICAL_OR:
            return Return("int", int(bool(l.value) or bool(r.value)))
        if type == "float":
            error("Mismatched types, expected INTC found FLOATC")
        if node.op.type == Token.BIT_AND:
            return Return("int", l.value & r.value)
        elif node.op.type == Token.BIT_OR:
            return Return("int", l.value | r.value)
        elif node.op.type == Token.BIT_XOR:
            return Return("int", l.value ^ r.value)
        elif node.op.type == Token.BIT_LSHIFT:
            return Return("int", l.value << r.value)
        elif node.op.type == Token.BIT_RSHIFT:
            return Return("int", l.value >> r.value)
        

    def visit_Num(self, node):
        if node.token.type == Token.FLOATC:
            return Return("float", node.value)
        elif node.token.type == Token.INTC:
            return Return("int", node.value)

    def visit_Block(self, node):
        self.scopes.push()
        for child in node.children:
            self.visit(child)
        print(self.scopes)
        self.scopes.pop()

    def visit_NoOp(self, node):
        pass

    def visit_Declare(self, node):
        var_type = node.type.value
        var_name = node.left.value
        var_visit = self.visit(node.right)
        if var_name in self.scopes.dicts[-1]:
            error(f"Redeclaration of {var_name}")
        if var_type == "int" and var_visit.type == "float":
            self.scopes.insert(var_name, Return("int", int(var_visit.value)))
        elif var_type == "float" and var_visit.type == "int":
            self.scopes.insert(var_name, Return("float", float(var_visit.value)))
        elif var_type == var_visit.type:
            self.scopes.insert(var_name, var_visit)
        else:
            error(f"Mismatched types, expected {var_type} found {var_visit.type}")

    def visit_Assign(self, node):
        var_name = node.left.value
        var_visit = self.visit(node.right)
        if var_name not in self.scopes:
            error(f"Unknown symbol: {var_name}")
        if self.scopes.get(var_name).type == "int" and var_visit.type == "float":
            self.scopes.set(var_name, Return("int", int(var_visit.value)))
        elif self.scopes.get(var_name).type == "float" and var_visit.type == "int":
            self.scopes.set(var_name, Return("float", float(var_visit.value)))
        elif self.scopes.get(var_name).type == var_visit.type:
            self.scopes.set(var_name, var_visit)
        else:
            error(f"Mismatched types, expected {self.scopes.get(var_name).type} found {var_visit.type}")
        

    def visit_Type(self, node):
        var_name = node.value
        if var_name not in self.scopes:
            error(f"Unknown symbol: {repr(var_name)}")
        else:
            return self.scopes.get(var_name)        

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
