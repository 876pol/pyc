from tokens import TokenType


class Value(object):
    """
    Class that represents a variable in the program.

    Attributes:
        type (TokenType): the type of variable.
        value (Any): the value of the variable.
    """

    def __init__(self, type: TokenType, value):
        self.type = type
        self.value = value


def build_value(type: TokenType, value) -> Value:
    """
    Builds an instance of the `Value` object from a type and value. This is different from the 
    constructor of the `Value` class because it returns a subclass of `Value`.
    Args:
        type (TokenType): the type of object that will be contained.
        value (Any): the value of the object.
    Returns:
        Value: the value that is built.
    """
    if type == TokenType.INT:
        return Int(type, int(value))
    elif type == TokenType.FLOAT:
        return Float(type, float(value))
    elif type == TokenType.STRING:
        return String(type, str(value))


class Int(Value):
    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.INT): lambda: build_value(TokenType.INT, self.value + obj.value),
            (TokenType.MINUS, TokenType.INT): lambda: build_value(TokenType.INT, self.value - obj.value),
            (TokenType.MUL, TokenType.INT): lambda: build_value(TokenType.INT, self.value * obj.value),
            (TokenType.DIV, TokenType.INT): lambda: build_value(TokenType.INT, self.value / obj.value),
            (TokenType.MOD, TokenType.INT): lambda: build_value(TokenType.INT, self.value % obj.value),
            (TokenType.LOGICAL_AND, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value >= obj.value)),
            (TokenType.BIT_AND, TokenType.INT): lambda: build_value(TokenType.INT, self.value & obj.value),
            (TokenType.BIT_OR, TokenType.INT): lambda: build_value(TokenType.INT, self.value | obj.value),
            (TokenType.BIT_XOR, TokenType.INT): lambda: build_value(TokenType.INT,  self.value ^ obj.value),
            (TokenType.BIT_LSHIFT, TokenType.INT): lambda: build_value(TokenType.INT, self.value << obj.value),
            (TokenType.BIT_RSHIFT, TokenType.INT): lambda: build_value(TokenType.INT, self.value >> obj.value),

            (TokenType.PLUS, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value + obj.value),
            (TokenType.MINUS, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value - obj.value),
            (TokenType.MUL, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value * obj.value),
            (TokenType.DIV, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value >= obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator):
        operations = {
            (TokenType.MINUS): lambda: build_value(TokenType.INT, -self.value),
            (TokenType.LOGICAL_NOT): lambda: build_value(TokenType.INT, bool(not self.value)),
            (TokenType.BIT_NOT): lambda: build_value(TokenType.INT, ~self.value),
        }
        return operations.get((operator), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.INT): lambda: build_value(TokenType.INT, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.INT): lambda: build_value(TokenType.INT, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.INT): lambda: build_value(TokenType.INT, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.INT): lambda: build_value(TokenType.INT, self.value / obj.value),
            (TokenType.MOD_ASSIGN, TokenType.INT): lambda: build_value(TokenType.INT, self.value % obj.value),
            (TokenType.BIT_AND_ASSIGN, TokenType.INT): lambda: build_value(TokenType.INT, self.value & obj.value),
            (TokenType.BIT_OR_ASSIGN, TokenType.INT): lambda: build_value(TokenType.INT, self.value | obj.value),
            (TokenType.BIT_XOR_ASSIGN, TokenType.INT): lambda: build_value(TokenType.INT,  self.value ^ obj.value),
            (TokenType.BIT_LSHIFT_ASSIGN, TokenType.INT): lambda: build_value(TokenType.INT, self.value << obj.value),
            (TokenType.BIT_RSHIFT_ASSIGN, TokenType.INT): lambda: build_value(TokenType.INT, self.value >> obj.value),

            (TokenType.PLUS_ASSIGN, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value / obj.value),
        }
        return operations.get((operator, obj.type), None)

    def cast_operator(self, operator):
        operations = {
            (TokenType.INT): lambda: build_value(TokenType.INT, self.value),
            (TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value),
            (TokenType.STRING): lambda:  build_value(TokenType.STRING, self.value),
        }
        return operations.get((operator), None)


class Float(Value):
    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value + obj.value),
            (TokenType.MINUS, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value - obj.value),
            (TokenType.MUL, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value * obj.value),
            (TokenType.DIV, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.FLOAT): lambda: build_value(TokenType.INT, bool(self.value >= obj.value)),

            (TokenType.PLUS, TokenType.INT): lambda: build_value(TokenType.FLOAT, self.value + obj.value),
            (TokenType.MINUS, TokenType.INT): lambda: build_value(TokenType.FLOAT, self.value - obj.value),
            (TokenType.MUL, TokenType.INT): lambda: build_value(TokenType.FLOAT, self.value * obj.value),
            (TokenType.DIV, TokenType.INT): lambda: build_value(TokenType.FLOAT, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.INT): lambda: build_value(TokenType.INT, bool(self.value >= obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator):
        operations = {
            (TokenType.MINUS): lambda: build_value(TokenType.FLOAT, -self.value),
            (TokenType.LOGICAL_NOT): lambda: build_value(
                TokenType.INT, bool(not self.value)),
        }
        return operations.get((operator), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value / obj.value),

            (TokenType.PLUS_ASSIGN, TokenType.INT): lambda: build_value(TokenType.FLOAT, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.INT): lambda: build_value(TokenType.FLOAT, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.INT): lambda: build_value(TokenType.FLOAT, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.INT): lambda: build_value(TokenType.FLOAT, self.value / obj.value),
        }
        return operations.get((operator, obj.type), None)

    def cast_operator(self, operator):
        operations = {
            (TokenType.INT): lambda: build_value(TokenType.INT, self.value),
            (TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value),
            (TokenType.STRING): lambda:  build_value(TokenType.STRING, self.value),
        }
        return operations.get((operator), None)


class String(Value):
    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.STRING): lambda: build_value(TokenType.STRING, self.value + obj.value),
            (TokenType.EQUAL, TokenType.STRING): lambda: build_value(TokenType.INT, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.STRING): lambda: build_value(TokenType.INT, bool(self.value != obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator):
        operations = {}
        return operations.get((operator), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.STRING): lambda: build_value(TokenType.STRING, self.value + obj.value),
        }
        return operations.get((operator, obj.type), None)

    def cast_operator(self, operator):
        operations = {
            (TokenType.INT): lambda: build_value(TokenType.INT, self.value),
            (TokenType.FLOAT): lambda: build_value(TokenType.FLOAT, self.value),
            (TokenType.STRING): lambda:  build_value(TokenType.STRING, self.value),
        }
        return operations.get((operator), None)


class Function(object):
    def __init__(self, type, args, block):
        self.type = type
        self.args = args
        self.block = block
