from lexer import Token, TokenType
from parser import Parser
from error import SemanticError, ErrorCode
from collections import namedtuple
from linked_dict import LinkedDict

Return = namedtuple("Return", "type value")


class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        ret = visitor(node)
        return ret

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.scopes = LinkedDict()

    def visit_UnaryOp(self, node):
        op = node.op.type
        v = self.visit(node.expr)
        if op == TokenType.MINUS:
            return Return(v.type, -self.visit(node.expr).value)
        elif op == TokenType.BIT_NOT:
            if v.type == "float":
                self.error(ErrorCode.MISMATCHED_TYPE, node.op)
            return Return("int", ~self.visit(node.expr).value)
        elif op == TokenType.LOGICAL_NOT:
            return Return("int", int(not int(self.visit(node.expr).value)))

    def visit_BinOp(self, node):
        l = self.visit(node.expr_left)
        r = self.visit(node.expr_right)
        type = "float" if "float" in (l.type, r.type) else "int"
        if node.op.type == TokenType.PLUS:
            return Return(type, l.value + r.value)
        elif node.op.type == TokenType.MINUS:
            return Return(type, l.value - r.value)
        elif node.op.type == TokenType.MUL:
            return Return(type, l.value * r.value)
        elif node.op.type == TokenType.DIV and type == "float":
            return Return(type, l.value / r.value)
        elif node.op.type == TokenType.DIV:
            return Return(type, l.value // r.value)
        elif node.op.type == TokenType.EQUAL:
            return Return("int", int(l.value == r.value))
        elif node.op.type == TokenType.NOT_EQUAL:
            return Return("int", int(l.value != r.value))
        elif node.op.type == TokenType.LESS:
            return Return("int", int(l.value < r.value))
        elif node.op.type == TokenType.GREATER:
            return Return("int", int(l.value > r.value))
        elif node.op.type == TokenType.LESS_EQUAL:
            return Return("int", int(l.value <= r.value))
        elif node.op.type == TokenType.GREATER_EQUAL:
            return Return("int", int(l.value >= r.value))
        elif node.op.type == TokenType.LOGICAL_AND:
            return Return("int", int(bool(l.value) and bool(r.value)))
        elif node.op.type == TokenType.LOGICAL_OR:
            return Return("int", int(bool(l.value) or bool(r.value)))
        if type == "float":
            self.error(ErrorCode.MISMATCHED_TYPE, node.op)
        if node.op.type == TokenType.BIT_AND:
            return Return("int", l.value & r.value)
        elif node.op.type == TokenType.BIT_OR:
            return Return("int", l.value | r.value)
        elif node.op.type == TokenType.BIT_XOR:
            return Return("int", l.value ^ r.value)
        elif node.op.type == TokenType.BIT_LSHIFT:
            return Return("int", l.value << r.value)
        elif node.op.type == TokenType.BIT_RSHIFT:
            return Return("int", l.value >> r.value)
        elif node.op.type == TokenType.MOD:
            return Return("int", l.value % r.value)

    def visit_Num(self, node):
        if node.token.type == TokenType.FLOATC:
            return Return("float", node.value)
        elif node.token.type == TokenType.INTC:
            return Return("int", node.value)

    def visit_DeclFunc(self, node):
        func_type = node.type
        func_name = node.name.value
        func_args = node.args
        func_body = node.body
        if func_name in self.scopes.peek():
            self.error(ErrorCode.DUPLICATE_ID, node.type)
        self.scopes.insert(func_name, (func_type, func_args, func_body))
        return Return("void", None)

    def visit_Block(self, node):
        self.scopes.push()
        for child in node.children:
            self.visit(child)
        print(self.scopes)
        self.scopes.pop()
        return Return("void", None)

    def visit_NoOp(self, node):
        return Return("void", None)

    def visit_Declare(self, node):
        var_type = node.type.value
        var_name = node.left.value
        var_visit = self.visit(node.right)
        if var_name in self.scopes.peek():
            self.error(ErrorCode.DUPLICATE_ID, node.type)
        if var_type == "int" and var_visit.type == "float":
            self.scopes.insert(var_name, Return("int", int(var_visit.value)))
        elif var_type == "float" and var_visit.type == "int":
            self.scopes.insert(var_name, Return("float", float(var_visit.value)))
        elif var_type == var_visit.type:
            self.scopes.insert(var_name, var_visit)
        else:
            self.error(ErrorCode.MISMATCHED_TYPE, var_visit.type)
        return Return("void", None)

    def visit_Assign(self, node):
        var_name = node.left.value
        var_visit = self.visit(node.right)
        if var_name not in self.scopes:
            self.error(ErrorCode.ID_NOT_FOUND, node.left.token)
        if self.scopes.get(var_name).type == "int" and var_visit.type == "float":
            self.scopes.set(var_name, Return("int", int(var_visit.value)))
        elif self.scopes.get(var_name).type == "float" and var_visit.type == "int":
            self.scopes.set(var_name, Return("float", float(var_visit.value)))
        elif self.scopes.get(var_name).type == var_visit.type:
            self.scopes.set(var_name, var_visit)
        else:
            self.error(ErrorCode.MISMATCHED_TYPE, var_visit.type)
        return Return("void", None)

    def visit_Type(self, node):
        var_name = node.value
        if var_name not in self.scopes:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)
        else:
            return self.scopes.get(var_name)

    def interpret(self):
        tree = self.parser.parse()
        self.scopes.push()
        self.visit(tree)
        self.visit(self.scopes.get("main")[2])
        self.scopes.pop()

    def error(self, error_code, token):
        raise SemanticError(f"{error_code.value} -> {token}")
