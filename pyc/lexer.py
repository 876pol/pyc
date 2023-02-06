"""
ICS3U
Paul Chen
This file holds the `Lexer` class that converts the code into tokens.
"""

from error import LexerError
from tokens import RESERVED_KEYWORDS, SYMBOLS, Token, TokenType
from collections import deque
from typing import Optional


class Lexer(object):
    """
    Lexer class that parses the input into tokens.

    Attributes:
        text (str): the program source code.
        pos (int): the index of the character that is currently being read.
        current_char (str): the character that `pos` is pointing at.
        line (int): the current line being read.
        column (int): the index of the character on the current line that is being read.
        buffer (deque[Token]): list of Tokens that have been read (during look-ahead) but have not been consumed.
    """

    def __init__(self, text: str) -> None:
        """
        Inits lexer class.
        Args:
            text (str): the program source code.
        """
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1
        self.column = 1
        self.buffer = deque()

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

    def peek(self) -> Optional[str]:
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
            return Token(TokenType.FLOATL, float(result), line=self.line, column=self.column)
        else:
            # Return the int token.
            return Token(TokenType.INTL, int(result), line=self.line, column=self.column)

    def get_string(self) -> Token:
        """
        Return a string literal consumed from the input.
        Returns:
            Token: token containing a string literal.
        """
        # Read the opening quotation mark.
        self.advance()

        # Keep reading characters until the current character is another quotation mark.
        result = ""
        while self.current_char is not None and self.current_char != "\"":
            result += self.current_char
            self.advance()

        # Read the closing quotation mark.
        if self.current_char == "\"":
            self.advance()

        # Return the string token.
        return Token(TokenType.STRINGL, result, line=self.line, column=self.column)

    def get_variable(self) -> Token:
        """
        Return a variable or keyword consumed from the input.
        Returns:
            Token: the variable or keyword read.
        """
        # Keeps reading alphanumerical characters into a string.
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()

        # If the character is a keyword, then return the keyword.
        if result in RESERVED_KEYWORDS:
            return Token(RESERVED_KEYWORDS[result], result, line=self.line, column=self.column)

        # Return the token containing a type.
        return Token(TokenType.TYPE, result, line=self.line, column=self.column)

    def get_next_symbol(self) -> Token:
        """
        Returns a Token corresponding to the next symbol present in the input.
        Returns:
            Token: the next character.
        """
        # Checks if there are over two characters left in the input.
        if self.peek() is not None:
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

    def load_next_token_into_buffer(self) -> None:
        """
        This method loads the next token from the code, and appends it to the end of the buffer.
        """
        # Keeps looping until a token is found.
        while self.current_char is not None:

            # Skips whitespace.
            if self.current_char.isspace():
                self.skip_whitespace()

            # Skips a single line comment.
            elif self.current_char == "/" and self.peek() == "/":
                self.skip_single_comment()

            # Skips a multi line comment.
            elif self.current_char == "/" and self.peek() == "*":
                self.skip_multi_comment()

            # If the current character is a quotation mark, store a string token into the buffer.
            elif self.current_char == "\"":
                self.buffer.append(self.get_string())

            # If the current character is a digit, store a number token into the buffer.
            elif self.current_char.isdigit():
                self.buffer.append(self.get_number())

            # If the current character is a letter, store a type or keyword token into the buffer.
            elif self.current_char.isalpha() or self.current_char == "_":
                self.buffer.append(self.get_variable())

            # Store a symbol into the buffer.
            else:
                self.buffer.append(self.get_next_symbol())

        # If there is nothing left in the input, store an EOF token into the buffer.
        self.buffer.append(Token(TokenType.EOF, None, line=self.line, column=self.column))

    def get_next_token(self) -> Token:
        """
        This method reads the next token from the code, consuming it and returning it.
        """
        if len(self.buffer) == 0:
            self.load_next_token_into_buffer()
        return self.buffer.popleft()

    def peek_nth_next_token(self, n: int) -> Token:
        """
        This method reads ahead `n + 1` tokens, and returns the `n + 1`th next token.
        """
        while len(self.buffer) == 0 or (len(self.buffer) <= n and self.buffer[-1].type != TokenType.EOF):
            self.load_next_token_into_buffer()
        if n < len(self.buffer):
            return self.buffer[n]
        return self.buffer[-1]

    def error(self) -> None:
        """Throws an error and states the current character, line, and column on which the error happened"""
        raise LexerError(
            f"Lexer error on '{self.current_char}' -> position={self.line}:{self.column}")
