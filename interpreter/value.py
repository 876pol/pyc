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

    def __init__(self, type: TokenType, value):
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f"({self.type}, {self.value})"

    __repr__ = __str__


def build_value(type: TokenType, value) -> Value:
    """
    Builds an instance of the `Value` object from a type and value. This is different from the 
    constructor of the `Value` class because it returns a subclass of `Value` (Int, Float, String, or List).
    Args:
        type (TokenType): the type of object that will be contained.
        value (Any): the value of the object.
    Returns:
        Value: the value that is built.
    """
    if type == TokenType.INTL:
        return Int(type, int(value))
    elif type == TokenType.FLOATL:
        return Float(type, float(value))
    elif type == TokenType.STRINGL:
        return String(type, str(value))
    elif type == TokenType.LISTL:
        return List(type, list(value))


def normal_to_identifier(obj: TokenType) -> TokenType:
    """
    Converts the type of an object to an identifier (ex. INTL -> INT).
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


def identifier_to_normal(obj: TokenType) -> TokenType:
    """
    Converts the type of an identifier and its object type. It's the opposite of the previous function.
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
            (TokenType.LOGICAL_AND, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value >= obj.value)),
            (TokenType.BIT_AND, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value & obj.value),
            (TokenType.BIT_OR, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value | obj.value),
            (TokenType.BIT_XOR, TokenType.INTL): lambda: build_value(TokenType.INTL,  self.value ^ obj.value),
            (TokenType.BIT_LSHIFT, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value << obj.value),
            (TokenType.BIT_RSHIFT, TokenType.INTL): lambda: build_value(TokenType.INTL, self.value >> obj.value),

            (TokenType.PLUS, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value + obj.value),
            (TokenType.MINUS, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value - obj.value),
            (TokenType.MUL, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value * obj.value),
            (TokenType.DIV, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value >= obj.value)),
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
            (TokenType.BIT_XOR_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.INTL,  self.value ^ obj.value),
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
            (TokenType.STRING): lambda:  build_value(TokenType.STRINGL, self.value),
        }
        return operations.get((operator), None)


class Float(Value):
    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value + obj.value),
            (TokenType.MINUS, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value - obj.value),
            (TokenType.MUL, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value * obj.value),
            (TokenType.DIV, TokenType.FLOATL): lambda: build_value(TokenType.FLOATL, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.FLOATL): lambda: build_value(TokenType.INTL, bool(self.value >= obj.value)),

            (TokenType.PLUS, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value + obj.value),
            (TokenType.MINUS, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value - obj.value),
            (TokenType.MUL, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value * obj.value),
            (TokenType.DIV, TokenType.INTL): lambda: build_value(TokenType.FLOATL, self.value / obj.value),
            (TokenType.LOGICAL_AND, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value and obj.value)),
            (TokenType.LOGICAL_OR, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value or obj.value)),
            (TokenType.EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value != obj.value)),
            (TokenType.LESS, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value < obj.value)),
            (TokenType.GREATER, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value > obj.value)),
            (TokenType.LESS_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value <= obj.value)),
            (TokenType.GREATER_EQUAL, TokenType.INTL): lambda: build_value(TokenType.INTL, bool(self.value >= obj.value)),
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
            (TokenType.STRING): lambda:  build_value(TokenType.STRINGL, self.value),
        }
        return operations.get((operator), None)


class String(Value):
    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.STRINGL): lambda: build_value(TokenType.STRINGL, self.value + obj.value),
            (TokenType.EQUAL, TokenType.STRINGL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.STRINGL): lambda: build_value(TokenType.INTL, bool(self.value != obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator):
        operations = {}
        return operations.get((operator), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.STRINGL): lambda: build_value(TokenType.STRINGL, self.value + obj.value),
        }
        return operations.get((operator, obj.type), None)

    def cast_operator(self, operator):
        operations = {
            (TokenType.INT): lambda: build_value(TokenType.INTL, self.value),
            (TokenType.FLOAT): lambda: build_value(TokenType.FLOATL, self.value),
            (TokenType.STRING): lambda:  build_value(TokenType.STRINGL, self.value),
        }
        return operations.get((operator), None)


class List(Value):
    def add_element_return(self, obj):
        ret_val = list(self.value)
        ret_val.append(obj)
        return ret_val

    def binary_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS, TokenType.INTL): lambda: build_value(TokenType.LISTL, self.add_element_return(obj)),
            (TokenType.PLUS, TokenType.FLOATL): lambda: build_value(TokenType.LISTL, self.add_element_return(obj)),
            (TokenType.PLUS, TokenType.STRINGL): lambda: build_value(TokenType.LISTL, self.add_element_return(obj)),
            (TokenType.PLUS, TokenType.LISTL): lambda: build_value(TokenType.LISTL, self.add_element_return(obj)),
            (TokenType.EQUAL, TokenType.LISTL): lambda: build_value(TokenType.INTL, bool(self.value == obj.value)),
            (TokenType.NOT_EQUAL, TokenType.LISTL): lambda: build_value(TokenType.INTL, bool(self.value != obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator):
        operations = {}
        return operations.get((operator), None)

    def assignment_operator(self, operator, obj):
        operations = {
            (TokenType.PLUS_ASSIGN, TokenType.INTL): lambda: build_value(TokenType.LISTL, self.add_element_return(obj)),
            (TokenType.PLUS_ASSIGN, TokenType.FLOATL): lambda: build_value(TokenType.LISTL, self.add_element_return(obj)),
            (TokenType.PLUS_ASSIGN, TokenType.STRINGL): lambda: build_value(TokenType.LISTL, self.add_element_return(obj)),
            (TokenType.PLUS_ASSIGN, TokenType.LISTL): lambda: build_value(TokenType.LISTL, self.add_element_return(obj)),
        }
        return operations.get((operator, obj.type), None)


class Function(object):
    """
    A class that represents a function that will be stored by the interpreter.

    Attributes:
        type (TokenType): the type of the function.
        args (list): the list of args.
        block (AST): the main body of the function.
    """

    def __init__(self, type: TokenType, args: list, block: AST):
        self.type = type
        self.args = args
        self.block = block
