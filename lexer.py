from error import LexerError
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
        self.lineno = line
        self.column = column

    def __str__(self) -> str:
        """String representation of the class instance."""
        return f"Token({self.type}, {repr(self.value)}, position={self.lineno}:{self.column})"

    __repr__ = __str__


# Dictionary that maps token identifiers to symbols. These identifiers 
# and symbols will be added to the TokenType enum class.
SYMBOL = {"PLUS": "+",
    "MINUS": "-",
    "MUL": "*",
    "DIV": "/",
    "MOD": "%",
    "LRPAR": "(",
    "RRPAR": ")",
    "LCPAR": "{",
    "RCPAR": "}",
    "ASSIGN": "=",
    "SEMI": ";",
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
    "BIT_RSHIFT": ">>"}

# Dictionary that maps token identifiers to keywords. These identifiers 
# and keywords will be added to the TokenType enum class.
KEYWORD = {"INTC": "int",
    "FLOATC": "float"}

# Dictionary that maps token identifiers to miscellaneous symbols. These identifiers 
# and miscellaneous symbols will be added to the TokenType enum class.
OTHER = {"EOF": "EOF",
    "TYPE": "TYPE"} # Represents a variable / function.

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


class Lexer:
    """
    Lexer class that parses the input into tokens.

    Attributes:
        text (str): the program source code.
        pos (int): the index of the character that is currently being read.
        current_char (str): the character that `pos` is pointing at.
        line (int): the current line being read.
        column (int): the index of the character on the current line that is being read.
    """
    
    def __init__(self, text: str):
        """
        Inits token class.
        Args:
            text (str): the program source code.
        """
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.column = 1

    def advance(self) -> None:
        """Advance the `pos` pointer and set the `current_char` variable."""
        # Reset the line and column values if the current character is a newline.
        if self.current_char == "\n":
            self.line += 1
            self.column = 0

        # Advance `pos`.
        self.pos += 1

        # Set the current character to None if the end of the input is reached.
        if self.pos > len(self.text) - 1:
            self.current_char = None

        # Otherwise set it to the next character in the input and increment `column`.
        else:
            self.current_char = self.text[self.pos]
            self.column += 1

    def skip_whitespace(self) -> None:
        """Skips the following whitespace in the source code."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_single_comment(self) -> None:
        """Skips a single line comment."""
        while self.current_char is not None and self.current_char != "\n":
            self.advance()
        self.advance()

    def skip_multi_comment(self) -> None:
        """Skips a multiline comment."""
        while self.current_char is not None and (self.current_char != "*" or self.peek() != "/"):
            self.advance()
        self.advance()
        self.advance()

    def get_number(self) -> Token:
        """
        Return a number consumed from the input.
        Returns:
            Token: token containing an int or a float.
        """
        # Keeps reading digits into a string until the current character is not a digit.
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        # Checks if the next character is a floating point number.
        if self.current_char == ".":
            # Read the period.
            result += self.current_char
            self.advance()

            # Keep reading digits.
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            # Return the float token.
            return Token(TokenType.FLOATC, float(result), line=self.line, column=self.column)
        else:
            # Return the int token.
            return Token(TokenType.INTC, int(result), line=self.line, column=self.column)

    def get_variable(self) -> Token:
        """
        Return a variable or keyword consumed from the input.
        Returns:
            Token: the variable or keyword read.
        """
        # Keeps reading alphanumberical characters into a string.
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        # If the character is a keyword, then return the keyword.
        if result in RESERVED_KEYWORDS:
            return Token(RESERVED_KEYWORDS[result], result, line=self.line, column=self.column)

        # Return the token containing a type.
        return Token(TokenType.TYPE, result, line=self.line, column=self.column)

    def peek(self) -> str:
        """
        Peeks into the character that follows `current_char`.
        Returns:
            str: the next character.
        """
        # If the end of the input is reached, return None.
        if self.pos + 1 > len(self.text) - 1:
            return None
        else:
            # Otherwise return the next character.
            return self.text[self.pos + 1]

    def get_next_symbol(self) -> Token:
        """
        Returns a Token corresponding to the next symbol present in the input.
        Returns:
            Token: the next character.
        """
        # Checks if there are over two characters left in the input.
        if self.peek() != None:
            # Read the current character and the next character into a string.
            s = self.current_char + self.peek()

            # If the two character string is a symbol, return the corresponding token.
            if s in SYMBOLS:
                self.advance()
                self.advance()
                return Token(SYMBOLS[s], s, line=self.line, column=self.column)

        
        # Checks if `current_char` is a valid symbol, if so, return a token corresponding to it.
        s = self.current_char
        if s in SYMBOLS:
            self.advance()
            return Token(SYMBOLS[s], s, line=self.line, column=self.column)

        # Throw an error is no symbol is found.
        self.error()
        
        

    def get_next_token(self) -> Token:
        """
        Lexical analyzer. This method is responsible for breaking
        the code apart into tokens.
        Returns:
            Token: the next token.
        """
        # Keeps looping until a token is found.
        while self.current_char is not None:

            # Skips whitespace.
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Skips a single line comment.
            if self.current_char == "/" and self.peek() == "/":
                self.skip_single_comment()
                continue

            # Skips a multi line comment.
            if self.current_char == "/" and self.peek() == "*":
                self.skip_multi_comment()
                continue

            # If the current character is a digit, return a number token.
            if self.current_char.isdigit():
                return self.get_number()

            # If the current character is a letter, return a type or keyword token.
            if self.current_char.isalpha():
                return self.get_variable()

            # Return a symbol.
            return self.get_next_symbol()

        # If there is nothing left in the input, return an EOF token.
        return Token(TokenType.EOF, None, line=self.line, column=self.column)

    def error(self):
        """Throws an error and states the current character, line, and column on which the error happened"""
        raise LexerError(f"Lexer error on '{self.current_char}' -> position={self.line}:{self.column}")
