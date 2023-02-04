"""
ICS3U
Paul Chen
This file holds the `Value` class and declares all possible types used by the interpreter (int, float, string, list).
"""
from ast import AST
from tokens import TokenType


class Value(object):
    """
    Class that represents a variable in the program.

    Attributes:
        type (TokenType): the type of variable.
        value (Any): the value of the variable.
    """

    default = None

    def __init__(self, _type: TokenType, value):
        self.type = _type
        self.value = value

    def binary_operator(self, operator, obj):
        return None

    def unary_operator(self, operator):
        return None

    def assignment_operator(self, operator, obj):
        return None

    def cast_operator(self, operator):
        return None

    def __str__(self) -> str:
        return f"({self.type}, {self.value})"

    __repr__ = __str__


def build_value(_type: TokenType, value=None) -> Value:
    """
    Builds an instance of the `Value` object from a type and value. This is different from the 
    constructor of the `Value` class because it returns a subclass of `Value` (Int, Float, or String).
    Args:
        _type (TokenType): the type of object that will be contained.
        value (Any): the value of the object.
    Returns:
        Value: the value that is built.
    """
    if value is None:
        if _type == TokenType.INTL:
            return Int(_type, 0)
        elif _type == TokenType.FLOATL:
            return Float(_type, 0.0)
        elif _type == TokenType.STRINGL:
            return String(_type, "")
    else:
        if _type == TokenType.INTL:
            return Int(_type, int(value))
        elif _type == TokenType.FLOATL:
            return Float(_type, float(value))
        elif _type == TokenType.STRINGL:
            return String(_type, str(value))


def object_to_identifier(obj: TokenType) -> TokenType:
    """
    Converts from an object literal to its keyword/identifier (ex. INTL -> INT).
    Args:
        obj (TokenType): the variable to convert.
    Returns:
        TokenType: the new type.
    """
    conversion = {
        TokenType.INTL: TokenType.INT,
        TokenType.FLOATL: TokenType.FLOAT,
        TokenType.STRINGL: TokenType.STRING,
        TokenType.LISTL: TokenType.LIST,
    }
    if obj not in conversion:
        raise KeyError()
    return conversion.get(obj)


def identifier_to_object(obj: TokenType) -> TokenType:
    """
    Converts from a keyword/identifier to an object literal. It's the opposite of the previous function.
    Args:
        obj (TokenType): the type to convert.
    Returns:
        TokenType: the new type.
    """
    conversion = {
        TokenType.INT: TokenType.INTL,
        TokenType.FLOAT: TokenType.FLOATL,
        TokenType.STRING: TokenType.STRINGL,
        TokenType.LIST: TokenType.LISTL,
    }
    if obj not in conversion:
        raise KeyError()
    return conversion.get(obj)


"""The next four class are subclasses of `Value`. They define all the operations that these types can perform."""


class Int(Value):
    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value + obj.value),
            (TokenType.MINUS, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value - obj.value),
            (TokenType.MUL, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value * obj.value),
            (TokenType.DIV, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value / obj.value),
            (TokenType.MOD, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value % obj.value),
            (TokenType.LOGICAL_AND, TokenType.INTL): lambda: build_value(TokenType.INTL,
                                                                         bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL,
                                                                           bool(self.value >= obj.value)),
            (TokenType.BIT_AND, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value & obj.value),
            (TokenType.BIT_OR, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value | obj.value),
            (TokenType.BIT_XOR, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value ^ obj.value),
            (TokenType.BIT_LSHIFT, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value << obj.value),
            (TokenType.BIT_RSHIFT, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value >> obj.value),

            (TokenType.PLUS, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value + obj.value),
            (TokenType.MINUS, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value - obj.value),
            (TokenType.MUL, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value * obj.value),
            (TokenType.DIV, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.FLOATL): lambda: build_value(TokenType.INTL,
                                                                           bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.FLOATL): lambda: build_value(TokenType.INTL,
                                                                          bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL,
                                                                          bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL,
                                                                             bool(self.value >= obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator):
        operations = {
            (TokenType.MINUS): lambda: build_value(TokenType.INTL, -self.value),
            (TokenType.LOGICAL_NOT): lambda: build_value(TokenType.INTL, bool(not self.value)),
            (TokenType.BIT_NOT): lambda: build_value(TokenType.INTL, ~self.value),
        }
        return operations.get((operator), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value / obj.value),
            (TokenType.MOD_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value % obj.value),
            (TokenType.BIT_AND_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value & obj.value),
            (TokenType.BIT_OR_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value | obj.value),
            (TokenType.BIT_XOR_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value ^ obj.value),
            (TokenType.BIT_LSHIFT_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value << obj.value),
            (TokenType.BIT_RSHIFT_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value >> obj.value),

            (TokenType.PLUS_ASSIGN, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value / obj.value),
        }
        return operations.get((operator, obj.type), None)

    def cast_operator(self, operator):
        operations = {
            (TokenType.INT): lambda: build_value(TokenType.INTL, self.value),
            (TokenType.FLOAT): lambda: build_value(TokenType.FLOATL, self.value),
            (TokenType.STRING): lambda: build_value(TokenType.STRINGL, self.value),
        }
        return operations.get((operator), None)


class Float(Value):
    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value + obj.value),
            (TokenType.MINUS, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value - obj.value),
            (TokenType.MUL, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value * obj.value),
            (TokenType.DIV, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.FLOATL): lambda: build_value(TokenType.INTL,
                                                                           bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.FLOATL): lambda: build_value(TokenType.INTL,
                                                                          bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL,
                                                                          bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL,
                                                                             bool(self.value >= obj.value)),

            (TokenType.PLUS, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value + obj.value),
            (TokenType.MINUS, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value - obj.value),
            (TokenType.MUL, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value * obj.value),
            (TokenType.DIV, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.INTL): lambda: build_value(TokenType.INTL,
                                                                         bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL,
                                                                           bool(self.value >= obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator):
        operations = {
            (TokenType.MINUS): lambda: build_value(TokenType.FLOATL, -self.value),
            (TokenType.LOGICAL_NOT): lambda: build_value(
                TokenType.INTL, bool(not self.value)),
        }
        return operations.get((operator), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value / obj.value),

            (TokenType.PLUS_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value + obj.value),
            (TokenType.MINUS_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value - obj.value),
            (TokenType.MUL_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value * obj.value),
            (TokenType.DIV_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value / obj.value),
        }
        return operations.get((operator, obj.type), None)

    def cast_operator(self, operator):
        operations = {
            (TokenType.INT): lambda: build_value(TokenType.INTL, self.value),
            (TokenType.FLOAT): lambda: build_value(TokenType.FLOATL, self.value),
            (TokenType.STRING): lambda: build_value(TokenType.STRINGL, self.value),
        }
        return operations.get((operator), None)


class String(Value):
    default = ""

    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.STRINGL): lambda: build_value(TokenType.STRINGL, self.value + obj.value),
            (TokenType.EQUAL, TokenType.STRINGL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.STRINGL): lambda: build_value(TokenType.INTL,
                                                                          bool(self.value != obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.STRINGL): lambda: build_value(TokenType.STRINGL, self.value + obj.value),
        }
        return operations.get((operator, obj.type), None)

    def cast_operator(self, operator):
        operations = {
            (TokenType.INT): lambda: build_value(TokenType.INTL, self.value),
            (TokenType.FLOAT): lambda: build_value(TokenType.FLOATL, self.value),
            (TokenType.STRING): lambda: build_value(TokenType.STRINGL, self.value),
        }
        return operations.get((operator), None)


class List(object):
    """
    TODO: change
    """

    def __init__(self, value):
        self.value = value

        curr = value
        while isinstance(curr, List):
            if len(curr.value) == 0:
                raise TypeError()
            curr = curr.value[0]
        self.type = curr.type

        def verify(obj):
            if len(obj) == 0:
                raise TypeError()
            if all(isinstance(element, List) for element in obj):
                for element in obj:
                    verify(element.value)
            elif not all(isinstance(element, Value) and element.type == self.type for element in obj):
                raise TypeError()

        verify(self.value)

    @staticmethod
    def from_dimensions(_type: TokenType, dimensions: list[int]):
        for d in dimensions:
            if d <= 0:
                raise TypeError()

        def generate(index):
            if index == len(dimensions):
                return build_value(_type)
            return List([generate(index + 1) for _ in range(dimensions[index + 1])])

        return generate(0)

    def access(self, indices: list[int]):
        curr = self.value
        for i in indices:
            curr = curr[i].value
        return curr

    def assign(self, indices: list[int], obj, operator: TokenType):
        curr = self.value
        for i in range(len(indices) - 1):
            curr = curr[indices[i]].value
        if operator == TokenType.ASSIGN:
            def assign_and_verify(old, new):
                if len(old) != len(new):
                    raise TypeError()
                for i in range(len(old)):
                    if isinstance(old[i], List) and isinstance(new[i], List):
                        assign_and_verify(old[i], new[i])
                    elif isinstance(new[i], Value) and new[i].type == self.type:
                        old[i] = new[i]
                    else:
                        raise TypeError()

            assign_and_verify(curr[indices[-1]], obj)

        else:
            if isinstance(curr[indices[-1]], List):
                return False
            value = curr[indices[-1]].assignment_operator(operator, obj)
            if value is None:
                return False
            curr[indices[-1]] = value()


class Function(object):
    """
    A class that represents a function that will be stored by the interpreter.

    Attributes:
        type (TokenType): the type of the function.
        args (list): the list of args.
        block (AST): the main body of the function.
    """

    def __init__(self, _type: TokenType, args: list, block: AST):
        self.type = _type
        self.args = args
        self.block = block
