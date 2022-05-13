from token import TokenType
    
class Value(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value


def bv(type: TokenType, value) -> Value:
    """
    Builds an instance of the `Value` object from a type and value. This is different from the 
    constructor of the `Value` class because it returns a subclass of `Value`.
    Args:
        type (TokenType): the type of object that will be contained.
        value (Any): the value of the object.
    Returns:
        Value: the value that is built.
    """
    if type == TokenType.INTC:
        return Int(type, int(value))
    elif type == TokenType.FLOATC:
        return Float(type, float(value))
    elif type == TokenType.STRING:
        return String(type, str(value))


class Int(Value):
    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value + obj.value),
            (TokenType.MINUS, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value - obj.value),
            (TokenType.MUL, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value * obj.value),
            (TokenType.DIV, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value / obj.value),
            (TokenType.MOD, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value % obj.value),
            (TokenType.LOGICAL_AND, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value >= obj.value)),
            (TokenType.BIT_AND, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value & obj.value),
            (TokenType.BIT_OR, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value | obj.value),
            (TokenType.BIT_XOR, TokenType.INTC) : lambda : bv(TokenType.INTC,  self.value ^ obj.value),
            (TokenType.BIT_LSHIFT, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value << obj.value),
            (TokenType.BIT_RSHIFT, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value >> obj.value),
            
            (TokenType.PLUS, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value + obj.value),
            (TokenType.MINUS, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value - obj.value),
            (TokenType.MUL, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value * obj.value),
            (TokenType.DIV, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value >= obj.value))
        }
        return operations.get((operator, obj.type), None)
            
    def unary_operator(self, operator):
        operations = {
            (TokenType.MINUS): lambda : bv(TokenType.INTC, -self.value),
            (TokenType.LOGICAL_NOT): lambda : bv(TokenType.INTC, bool(not self.value)),
            (TokenType.BIT_NOT): lambda : bv(TokenType.INTC, ~self.value)
        }
        return operations.get((operator), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value / obj.value),
            (TokenType.MOD_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value % obj.value),
            (TokenType.BIT_AND_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value & obj.value),
            (TokenType.BIT_OR_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value | obj.value),
            (TokenType.BIT_XOR_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.INTC,  self.value ^ obj.value),
            (TokenType.BIT_LSHIFT_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value << obj.value),
            (TokenType.BIT_RSHIFT_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.INTC, self.value >> obj.value),

            (TokenType.PLUS_ASSIGN, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value / obj.value),
        }
        return operations.get((operator, obj.type), None)
    

class Float(Value):
    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value + obj.value),
            (TokenType.MINUS, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value - obj.value),
            (TokenType.MUL, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value * obj.value),
            (TokenType.DIV, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.FLOATC) : lambda : bv(TokenType.INTC, bool(self.value >= obj.value)),
            
            (TokenType.PLUS, TokenType.INTC) : lambda : bv(TokenType.FLOATC, self.value + obj.value),
            (TokenType.MINUS, TokenType.INTC) : lambda : bv(TokenType.FLOATC, self.value - obj.value),
            (TokenType.MUL, TokenType.INTC) : lambda : bv(TokenType.FLOATC, self.value * obj.value),
            (TokenType.DIV, TokenType.INTC) : lambda : bv(TokenType.FLOATC, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.INTC) : lambda : bv(TokenType.INTC, bool(self.value >= obj.value))
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator):
        operations = {
            (TokenType.MINUS): lambda : bv(TokenType.FLOATC, -self.value),
            (TokenType.LOGICAL_NOT): lambda : bv(TokenType.INTC, bool(not self.value))
        }
        return operations.get((operator), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.FLOATC) : lambda : bv(TokenType.FLOATC, self.value / obj.value),
            
            (TokenType.PLUS_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.FLOATC, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.FLOATC, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.FLOATC, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.INTC) : lambda : bv(TokenType.FLOATC, self.value / obj.value),
        }
        return operations.get((operator, obj.type), None)


class String(Value):
    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.STRING) : lambda : bv(TokenType.STRING, self.value + obj.value),
            (TokenType.EQUAL, TokenType.STRING) : lambda : bv(TokenType.INTC, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.STRING) : lambda : bv(TokenType.INTC, bool(self.value != obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator):
        operations = {}
        return operations.get((operator), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.STRING) : lambda : bv(TokenType.STRING, self.value + obj.value),
        }
        return operations.get((operator, obj.type), None)