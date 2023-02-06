"""
ICS3U
Paul Chen
This file creates the `Token` class and declares all tokens and keywords used by the interpreter.
"""

from enum import Enum
from typing import Optional, Union


class Token(object):
    """
    Class that represents a token.

    Attributes:
        type (TokenType): the type of token.
        value (Optional[Union[int, float, str]]): the name held by the token.
        line (int): the current line being read.
        column (int): the index of the character on the current line that is being read.
    """

    def __init__(self, token_type: "TokenType", value: Optional[Union[int, float, str]], line: int = -1,
                 column: int = -1) -> None:
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self) -> str:
        """String representation of the class instance."""
        return f"Token({self.type}, {repr(self.value)}, position={self.line}:{self.column})"

    __repr__ = __str__


class TokenType(Enum):
    """Class holding all the types of tokens read by the lexer."""

    # Symbols.
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    LOGICAL_AND = "&&"
    LOGICAL_OR = "||"
    LOGICAL_NOT = "!"
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS = "<"
    GREATER = ">"
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    BIT_AND = "&"
    BIT_OR = "|"
    BIT_XOR = "^"
    BIT_NOT = "~"
    BIT_LSHIFT = "<<"
    BIT_RSHIFT = ">>"
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    MUL_ASSIGN = "*="
    DIV_ASSIGN = "/="
    MOD_ASSIGN = "%="
    BIT_AND_ASSIGN = "&="
    BIT_OR_ASSIGN = "|="
    BIT_XOR_ASSIGN = "^="
    BIT_LSHIFT_ASSIGN = "<<="
    BIT_RSHIFT_ASSIGN = ">>="
    LRPAR = "("
    RRPAR = ")"
    LSPAR = "["
    RSPAR = "]"
    LCPAR = "{"
    RCPAR = "}"
    SEMI = ";"
    COMMA = ","

    # Keywords.
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    VOID = "void"
    IF = "if"
    ELSE = "else"
    FOR = "for"
    WHILE = "while"
    DO = "do"
    BREAK = "break"
    CONTINUE = "continue"
    RETURN = "return"

    # Other.
    EOF = "EOF"
    TYPE = "TYPE"
    INTL = "INTL"
    FLOATL = "FLOATL"
    STRINGL = "STRINGL"
    ARRAYL = "ARRAYL"
    VOIDL = "VOIDL"


# Map the symbols and keywords to their respective tokens.
# This lets us match them in O(1) time.
SYMBOLS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MUL,
    "/": TokenType.DIV,
    "%": TokenType.MOD,
    "&&": TokenType.LOGICAL_AND,
    "||": TokenType.LOGICAL_OR,
    "!": TokenType.LOGICAL_NOT,
    "==": TokenType.EQUAL,
    "!=": TokenType.NOT_EQUAL,
    "<": TokenType.LESS,
    ">": TokenType.GREATER,
    "<=": TokenType.LESS_EQUAL,
    ">=": TokenType.GREATER_EQUAL,
    "&": TokenType.BIT_AND,
    "|": TokenType.BIT_OR,
    "^": TokenType.BIT_XOR,
    "~": TokenType.BIT_NOT,
    "<<": TokenType.BIT_LSHIFT,
    ">>": TokenType.BIT_RSHIFT,
    "=": TokenType.ASSIGN,
    "+=": TokenType.PLUS_ASSIGN,
    "-=": TokenType.MINUS_ASSIGN,
    "*=": TokenType.MUL_ASSIGN,
    "/=": TokenType.DIV_ASSIGN,
    "%=": TokenType.MOD_ASSIGN,
    "&=": TokenType.BIT_AND_ASSIGN,
    "|=": TokenType.BIT_OR_ASSIGN,
    "^=": TokenType.BIT_XOR_ASSIGN,
    "<<=": TokenType.BIT_LSHIFT_ASSIGN,
    ">>=": TokenType.BIT_RSHIFT_ASSIGN,
    "(": TokenType.LRPAR,
    ")": TokenType.RRPAR,
    "[": TokenType.LSPAR,
    "]": TokenType.RSPAR,
    "{": TokenType.LCPAR,
    "}": TokenType.RCPAR,
    ";": TokenType.SEMI,
    ",": TokenType.COMMA
}

RESERVED_KEYWORDS = {
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "string": TokenType.STRING,
    "void": TokenType.VOID,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "for": TokenType.FOR,
    "while": TokenType.WHILE,
    "do": TokenType.DO,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "return": TokenType.RETURN
}
