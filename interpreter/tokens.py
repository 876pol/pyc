from enum import Enum


class Token(object):
    """
    Class that represents a token.

    Attributes:
        type (str): the type of token.
        value (object): the value held by the token.
        line (int): the current line being read.
        column (int): the index of the character on the current line that is being read.
    """

    def __init__(self, type: str, value: object, line=-1, column=-1):
        """
        Inits token class.
        Args:
            type (str): the type of token.
            value (object): the value held by the token.
            line (int): the current line being read.
            column (int): the index of the character on the current line that is being read.
        """
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self) -> str:
        """String representation of the class instance."""
        return f"Token({self.type}, {repr(self.value)}, position={self.line}:{self.column})"

    __repr__ = __str__


# Dictionary containing all special symbols and characters. These identifiers
# and keywords will be added to the TokenType enum class.
SYMBOL = {"PLUS": "+",
          "MINUS": "-",
          "MUL": "*",
          "DIV": "/",
          "MOD": "%",
          "LOGICAL_AND": "&&",
          "LOGICAL_OR": "||",
          "LOGICAL_NOT": "!",
          "EQUAL": "==",
          "NOT_EQUAL": "!=",
          "LESS": "<",
          "GREATER": ">",
          "LESS_EQUAL": "<=",
          "GREATER_EQUAL": ">=",
          "BIT_AND": "&",
          "BIT_OR": "|",
          "BIT_XOR": "^",
          "BIT_NOT": "~",
          "BIT_LSHIFT": "<<",
          "BIT_RSHIFT": ">>",
          "ASSIGN": "=",
          "PLUS_ASSIGN": "+=",
          "MINUS_ASSIGN": "-=",
          "MUL_ASSIGN": "*=",
          "DIV_ASSIGN": "/=",
          "MOD_ASSIGN": "%=",
          "BIT_AND_ASSIGN": "&=",
          "BIT_OR_ASSIGN": "|=",
          "BIT_XOR_ASSIGN": "^=",
          "BIT_LSHIFT_ASSIGN": "<<=",
          "BIT_RSHIFT_ASSIGN": ">>=",
          "LRPAR": "(",
          "RRPAR": ")",
          "LCPAR": "{",
          "RCPAR": "}",
          "SEMI": ";",
          "COMMA": ",",
          }

# Dictionary that maps token identifiers to keywords. These identifiers
# and keywords will be added to the TokenType enum class.
KEYWORD = {"INTC": "int",
           "FLOATC": "float",
           "STRING": "string",
           "VOID": "void",
           "IF": "if",
           "ELSE": "else",
           "FOR": "for",
           "WHILE": "while",
           "DO": "do",
           "BREAK": "break",
           "CONTINUE": "continue",
           "RETURN": "return",
           }

# Dictionary that maps token identifiers to miscellaneous symbols. These identifiers
# and miscellaneous symbols will be added to the TokenType enum class.
OTHER = {"EOF": "EOF",
         "TYPE": "TYPE",
         }


class TokenType(Enum):
    """Enum class that contains all the different types of tokens."""
    pass


# Add all the entries from the SYMBOL, KEYWORD, and OTHER dictionaries into the TokenType enum.
for k, v in SYMBOL.items():
    setattr(TokenType, k, v)
for k, v in KEYWORD.items():
    setattr(TokenType, k, v)
for k, v in OTHER.items():
    setattr(TokenType, k, v)

# Map the symbols and keywords to their respective tokens.
# This lets us match them in O(1) time.
SYMBOLS = {v: getattr(TokenType, k)
           for k, v in SYMBOL.items()}
RESERVED_KEYWORDS = {v: getattr(TokenType, k)
                     for k, v in KEYWORD.items()}
