"""
ICS3U
Paul Chen
This file holds the `Value` class and declares all possible types used by the interpreter (int, float, string, list).
"""
from typing import Any, Callable, List, Optional, Union

from ast_nodes import BlockStatementNode, BuiltInFunctionCallStatementNode, FunctionArgument, ASTNode
from tokens import TokenType, TokenType as Tt


class Value(object):
    """
    Class that represents a variable in the program.

    Attributes:
        type (TokenType): the type of variable.
        value (Any): the name of the variable.
    """

    default = None

    def __init__(self, token_type: TokenType, value: Any) -> None:
        self.type = token_type
        self.value = value

    def binary_operator(self, operator: TokenType, obj: "Value") -> Optional[Callable]:
        return None

    def unary_operator(self, operator: TokenType) -> Optional[Callable]:
        return None

    def assignment_operator(self, operator: TokenType, obj: "Value") -> Optional[Callable]:
        return None

    def cast_operator(self, operator: TokenType) -> Optional[Callable]:
        return None

    def __str__(self) -> str:
        return f"({self.type}, {self.value})"

    __repr__ = __str__


def build_value(token_type: TokenType, value: Optional[Any] = None) -> Value:
    """
    Builds an instance of the `Value` object from a type and name. This is different from the
    constructor of the `Value` class because it returns a subclass of `Value`.
    Args:
        token_type (TokenType): the type of value that will be contained.
        value (Any): the value held.
    Returns:
        Value: the Value that is built.
    """
    # Return default values.
    if value is None:
        if token_type == Tt.INTL:
            return IntValue(token_type, 0)
        elif token_type == Tt.FLOATL:
            return FloatValue(token_type, 0.0)
        elif token_type == Tt.STRINGL:
            return StringValue(token_type, "")
        elif token_type == Tt.ARRAYL:
            return InitializerListValue(token_type, [])
        else:
            return NullValue(Tt.VOIDL, None)
    # return user-defined values.
    else:
        def check_instance_else_error(_type):
            if not isinstance(value, _type):
                raise ValueError()

        if token_type == Tt.INTL:
            check_instance_else_error(int)
            return IntValue(token_type, value)
        elif token_type == Tt.FLOATL:
            check_instance_else_error(float)
            return FloatValue(token_type, value)
        elif token_type == Tt.STRINGL:
            check_instance_else_error(str)
            return StringValue(token_type, value)
        elif token_type == Tt.ARRAYL:
            check_instance_else_error(list)
            return InitializerListValue(token_type, value)
        else:
            if value is not None:
                raise ValueError()
            return NullValue(Tt.VOIDL, None)


bv = build_value


def object_to_identifier(obj: TokenType) -> TokenType:
    """
    Converts from an object literal to its keyword/identifier (ex. INTL -> INT).
    Args:
        obj (TokenType): the variable to convert.
    Returns:
        TokenType: the new type.
    """
    conversion = {
        Tt.INTL: Tt.INT,
        Tt.FLOATL: Tt.FLOAT,
        Tt.STRINGL: Tt.STRING
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
        Tt: the new type.
    """
    conversion = {
        Tt.INT: Tt.INTL,
        Tt.FLOAT: Tt.FLOATL,
        Tt.STRING: Tt.STRINGL
    }
    if obj not in conversion:
        raise KeyError()
    return conversion.get(obj)


"""The next four class are subclasses of `Value`. They define all the operations that these types can perform."""


class IntValue(Value):
    def binary_operator(self, operator: TokenType, obj: Value) -> Optional[Callable]:
        operations = {
            (Tt.PLUS, Tt.INTL): lambda: bv(Tt.INTL, int(self.value + obj.value)),
            (Tt.MINUS, Tt.INTL): lambda: bv(Tt.INTL, int(self.value - obj.value)),
            (Tt.MUL, Tt.INTL): lambda: bv(Tt.INTL, int(self.value * obj.value)),
            (Tt.DIV, Tt.INTL): lambda: bv(Tt.INTL, int(self.value / obj.value)),
            (Tt.MOD, Tt.INTL): lambda: bv(Tt.INTL, int(self.value % obj.value)),
            (Tt.LOGICAL_AND, Tt.INTL): lambda: bv(Tt.INTL, int(self.value and obj.value)),
            (Tt.LOGICAL_OR, Tt.INTL): lambda: bv(Tt.INTL, int(self.value or obj.value)),
            (Tt.EQUAL, Tt.INTL): lambda: bv(Tt.INTL, int(self.value == obj.value)),
            (Tt.NOT_EQUAL, Tt.INTL): lambda: bv(Tt.INTL, int(self.value != obj.value)),
            (Tt.LESS, Tt.INTL): lambda: bv(Tt.INTL, int(self.value < obj.value)),
            (Tt.GREATER, Tt.INTL): lambda: bv(Tt.INTL, int(self.value > obj.value)),
            (Tt.LESS_EQUAL, Tt.INTL): lambda: bv(Tt.INTL, int(self.value <= obj.value)),
            (Tt.GREATER_EQUAL, Tt.INTL): lambda: bv(Tt.INTL, int(self.value >= obj.value)),
            (Tt.BIT_AND, Tt.INTL): lambda: bv(Tt.INTL, int(self.value & obj.value)),
            (Tt.BIT_OR, Tt.INTL): lambda: bv(Tt.INTL, int(self.value | obj.value)),
            (Tt.BIT_XOR, Tt.INTL): lambda: bv(Tt.INTL, int(self.value ^ obj.value)),
            (Tt.BIT_LSHIFT, Tt.INTL): lambda: bv(Tt.INTL, int(self.value << obj.value)),
            (Tt.BIT_RSHIFT, Tt.INTL): lambda: bv(Tt.INTL, int(self.value >> obj.value)),

            (Tt.PLUS, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value + obj.value)),
            (Tt.MINUS, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value - obj.value)),
            (Tt.MUL, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value * obj.value)),
            (Tt.DIV, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value / obj.value)),
            (Tt.LOGICAL_AND, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value and obj.value)),
            (Tt.LOGICAL_OR, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value or obj.value)),
            (Tt.EQUAL, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value == obj.value)),
            (Tt.NOT_EQUAL, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value != obj.value)),
            (Tt.LESS, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value < obj.value)),
            (Tt.GREATER, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value > obj.value)),
            (Tt.LESS_EQUAL, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value <= obj.value)),
            (Tt.GREATER_EQUAL, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value >= obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator: TokenType) -> Optional[Callable]:
        operations = {
            Tt.MINUS: lambda: bv(Tt.INTL, int(-self.value)),
            Tt.LOGICAL_NOT: lambda: bv(Tt.INTL, int(not self.value)),
            Tt.BIT_NOT: lambda: bv(Tt.INTL, int(~self.value)),
        }
        return operations.get(operator, None)

    def assignment_operator(self, operator: TokenType, obj: Value) -> Optional[Callable]:
        operations = {
            (Tt.PLUS_ASSIGN, Tt.INTL): lambda: bv(Tt.INTL, int(self.value + obj.value)),
            (Tt.MINUS_ASSIGN, Tt.INTL): lambda: bv(Tt.INTL, int(self.value - obj.value)),
            (Tt.MUL_ASSIGN, Tt.INTL): lambda: bv(Tt.INTL, int(self.value * obj.value)),
            (Tt.DIV_ASSIGN, Tt.INTL): lambda: bv(Tt.INTL, int(self.value / obj.value)),
            (Tt.MOD_ASSIGN, Tt.INTL): lambda: bv(Tt.INTL, int(self.value % obj.value)),
            (Tt.BIT_AND_ASSIGN, Tt.INTL): lambda: bv(Tt.INTL, int(self.value & obj.value)),
            (Tt.BIT_OR_ASSIGN, Tt.INTL): lambda: bv(Tt.INTL, int(self.value | obj.value)),
            (Tt.BIT_XOR_ASSIGN, Tt.INTL): lambda: bv(Tt.INTL, int(self.value ^ obj.value)),
            (Tt.BIT_LSHIFT_ASSIGN, Tt.INTL): lambda: bv(Tt.INTL, int(self.value << obj.value)),
            (Tt.BIT_RSHIFT_ASSIGN, Tt.INTL): lambda: bv(Tt.INTL, int(self.value >> obj.value)),

            (Tt.PLUS_ASSIGN, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value + obj.value)),
            (Tt.MINUS_ASSIGN, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value - obj.value)),
            (Tt.MUL_ASSIGN, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value * obj.value)),
            (Tt.DIV_ASSIGN, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value / obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def cast_operator(self, operator: TokenType) -> Optional[Callable]:
        operations = {
            Tt.INT: lambda: bv(Tt.INTL, int(self.value)),
            Tt.FLOAT: lambda: bv(Tt.FLOATL, float(self.value)),
            Tt.STRING: lambda: bv(Tt.STRINGL, str(self.value)),
        }
        return operations.get(operator, None)


class FloatValue(Value):
    def binary_operator(self, operator: TokenType, obj: Value) -> Optional[Callable]:
        operations = {
            (Tt.PLUS, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value + obj.value)),
            (Tt.MINUS, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value - obj.value)),
            (Tt.MUL, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value * obj.value)),
            (Tt.DIV, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value / obj.value)),
            (Tt.LOGICAL_AND, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value and obj.value)),
            (Tt.LOGICAL_OR, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value or obj.value)),
            (Tt.EQUAL, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value == obj.value)),
            (Tt.NOT_EQUAL, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value != obj.value)),
            (Tt.LESS, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value < obj.value)),
            (Tt.GREATER, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value > obj.value)),
            (Tt.LESS_EQUAL, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value <= obj.value)),
            (Tt.GREATER_EQUAL, Tt.FLOATL): lambda: bv(Tt.INTL, int(self.value >= obj.value)),

            (Tt.PLUS, Tt.INTL): lambda: bv(Tt.FLOATL, float(self.value + obj.value)),
            (Tt.MINUS, Tt.INTL): lambda: bv(Tt.FLOATL, float(self.value - obj.value)),
            (Tt.MUL, Tt.INTL): lambda: bv(Tt.FLOATL, float(self.value * obj.value)),
            (Tt.DIV, Tt.INTL): lambda: bv(Tt.FLOATL, float(self.value / obj.value)),
            (Tt.LOGICAL_AND, Tt.INTL): lambda: bv(Tt.INTL, int(self.value and obj.value)),
            (Tt.LOGICAL_OR, Tt.INTL): lambda: bv(Tt.INTL, int(self.value or obj.value)),
            (Tt.EQUAL, Tt.INTL): lambda: bv(Tt.INTL, int(self.value == obj.value)),
            (Tt.NOT_EQUAL, Tt.INTL): lambda: bv(Tt.INTL, int(self.value != obj.value)),
            (Tt.LESS, Tt.INTL): lambda: bv(Tt.INTL, int(self.value < obj.value)),
            (Tt.GREATER, Tt.INTL): lambda: bv(Tt.INTL, int(self.value > obj.value)),
            (Tt.LESS_EQUAL, Tt.INTL): lambda: bv(Tt.INTL, int(self.value <= obj.value)),
            (Tt.GREATER_EQUAL, Tt.INTL): lambda: bv(Tt.INTL, int(self.value >= obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def unary_operator(self, operator: TokenType) -> Optional[Callable]:
        operations = {
            Tt.MINUS: lambda: bv(Tt.FLOATL, float(-self.value)),
            Tt.LOGICAL_NOT: lambda: bv(Tt.INTL, int(not self.value)),
        }
        return operations.get(operator, None)

    def assignment_operator(self, operator: TokenType, obj: Value) -> Optional[Callable]:
        operations = {
            (Tt.PLUS_ASSIGN, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value + obj.value)),
            (Tt.MINUS_ASSIGN, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value - obj.value)),
            (Tt.MUL_ASSIGN, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value * obj.value)),
            (Tt.DIV_ASSIGN, Tt.FLOATL): lambda: bv(Tt.FLOATL, float(self.value / obj.value)),

            (Tt.PLUS_ASSIGN, Tt.INTL): lambda: bv(Tt.FLOATL, float(self.value + obj.value)),
            (Tt.MINUS_ASSIGN, Tt.INTL): lambda: bv(Tt.FLOATL, float(self.value - obj.value)),
            (Tt.MUL_ASSIGN, Tt.INTL): lambda: bv(Tt.FLOATL, float(self.value * obj.value)),
            (Tt.DIV_ASSIGN, Tt.INTL): lambda: bv(Tt.FLOATL, float(self.value / obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def cast_operator(self, operator: TokenType) -> Optional[Callable]:
        operations = {
            Tt.INT: lambda: bv(Tt.INTL, int(self.value)),
            Tt.FLOAT: lambda: bv(Tt.FLOATL, float(self.value)),
            Tt.STRING: lambda: bv(Tt.STRINGL, str(self.value)),
        }
        return operations.get(operator, None)


class StringValue(Value):
    default = ""

    def binary_operator(self, operator: TokenType, obj: Value) -> Optional[Callable]:
        operations = {
            (Tt.PLUS, Tt.STRINGL): lambda: bv(Tt.STRINGL, str(self.value + obj.value)),
            (Tt.EQUAL, Tt.STRINGL): lambda: bv(Tt.INTL, int(self.value == obj.value)),
            (Tt.NOT_EQUAL, Tt.STRINGL): lambda: bv(Tt.INTL, int(self.value != obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def assignment_operator(self, operator: TokenType, obj: Value) -> Optional[Callable]:
        operations = {
            (Tt.PLUS_ASSIGN, Tt.STRINGL): lambda: bv(Tt.STRINGL, str(self.value + obj.value)),
        }
        return operations.get((operator, obj.type), None)

    def cast_operator(self, operator: TokenType) -> Optional[Callable]:
        operations = {
            Tt.INT: lambda: bv(Tt.INTL, int(self.value)),
            Tt.FLOAT: lambda: bv(Tt.FLOATL, float(self.value)),
            Tt.STRING: lambda: bv(Tt.STRINGL, str(self.value)),
        }
        return operations.get(operator, None)


class InitializerListValue(Value):
    pass


class NullValue(Value):
    pass


class Function(object):
    """
    A class that represents a function that will be stored by the interpreter.

    Attributes:
        type (TokenType): the type of the function.
        args (List[Union[FunctionArgument]]): the list of args.
        block (Union[BuiltInFunctionCallStatementNode, BlockStatementNode]): the main body of the function.
    """

    def __init__(self, token_type: TokenType, args: List[Union[FunctionArgument]],
                 block: Union[BuiltInFunctionCallStatementNode, BlockStatementNode]) -> None:
        self.type = token_type
        self.args = args
        self.block = block
