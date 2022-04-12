from error import error

class Token:
    """Class that represents a token.

    Attributes:
        type (str): the type of token.
        value (object): the value held by the token.
    """

    def __init__(self, type: str, value: object):
        """
        Inits token class.
        Args
            type (str): the type of token.
            value (object): the value held by the token.
        """
        self.type = type
        self.value = value

# List of all possible tokens
for token in ["INTC", "FLOATC", "PLUS", "MINUS", "MUL", "DIV", "LRPAR", "RRPAR", "LCPAR", "RCPAR", "ASSIGN", "TYPE", \
    "SEMI", "EOF", "SINGLE_COMMENT", "LMULTI_COMMENT", "RMULTI_COMMENT", "INT", "FLOAT", "LOGICAL_AND", \
    "LOGICAL_OR", "LOGICAL_NOT", "EQUAL", "NOT_EQUAL", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL", \
    "BIT_AND", "BIT_OR", "BIT_XOR", "BIT_NOT", "BIT_LSHIFT", "BIT_RSHIFT"]:
    setattr(Token, token, token)

# Dictionary that holds a list of keywords
RESERVED_KEYWORDS = {
    "int": Token(Token.INTC, "int"),
    "float": Token(Token.FLOATC, "float")
}

SYMBOLS = {
    "+": Token(Token.PLUS, "+"),
    "-": Token(Token.MINUS, "-"),
    "*": Token(Token.MUL, "*"),
    "/": Token(Token.DIV, "/"),
    "(": Token(Token.LRPAR, "("),
    ")": Token(Token.RRPAR, ")"),
    "{": Token(Token.LCPAR, "{"),
    "}": Token(Token.RCPAR, "}"),
    "=": Token(Token.ASSIGN, "="),
    ";": Token(Token.SEMI, ";"),
    "&&": Token(Token.LOGICAL_AND, "&&"),
    "||": Token(Token.LOGICAL_OR, "||"),
    "!": Token(Token.LOGICAL_NOT, "!"),
    "==": Token(Token.EQUAL, "=="),
    "!=": Token(Token.NOT_EQUAL, "!="),
    "<": Token(Token.LESS, "<"),
    ">": Token(Token.GREATER, ">"),
    "<=": Token(Token.LESS_EQUAL, "<="),
    ">=": Token(Token.GREATER_EQUAL, ">="),
    "&": Token(Token.BIT_AND, "&"),
    "|": Token(Token.BIT_OR, "|"),
    "^": Token(Token.BIT_XOR, "^"),
    "~": Token(Token.BIT_NOT, "~"),
    "<<": Token(Token.BIT_LSHIFT, "<<"),
    ">>": Token(Token.BIT_RSHIFT, ">>")

}

class Lexer:
    """
    Lexer class that parses the input into tokens.

    Attributes:
        text (str): the program source code.
        pos (int): the index of the character that is currently being read.
        current_char (str): the character that `pos` is pointing at.
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

    def advance(self) -> None:
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self) -> None:
        """Skips the following whitespace in the source code."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_single_comment(self) -> None:
        while self.current_char is not None and self.current_char != "\n":
            self.advance()
        self.advance()

    def skip_multi_comment(self) -> None:
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
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
    
        if self.current_char == ".":
            result += self.current_char
            self.advance()
    
            while (
                self.current_char is not None and
                self.current_char.isdigit()
            ):
                result += self.current_char
                self.advance()
    
            token = Token(Token.FLOATC, float(result))
        else:
            token = Token(Token.INTC, int(result))
    
        return token

    def get_variable(self) -> Token:
        """
        Return a variable or keyword consumed from the input.
        Returns:
            Token: the variable or keyword read.
        """
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result, Token(Token.TYPE, result))
        return token

    def peek(self) -> str:
        """
        Peeks into the character that follows `current_char`.
        Returns:
            str: the next character.
        """
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def get_next_symbol(self) -> Token:
        if self.peek() != None:
            s = self.current_char + self.peek()
            if s in SYMBOLS:
                self.advance()
                self.advance()
                return SYMBOLS[s]
        s = self.current_char
        if s in SYMBOLS:
            self.advance()
            return SYMBOLS[s]
        error(f"Token not recognized: {self.current_char}")
        
        

    def get_next_token(self) -> Token:
        """
        Lexical analyzer. This method is responsible for breaking
        the code apart into tokens.
        Returns:
            Token: the next token.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == "/" and self.peek() == "/":
                self.skip_single_comment()
                continue

            if self.current_char == "/" and self.peek() == "*":
                self.skip_multi_comment()
                continue

            if self.current_char.isdigit():
                return self.get_number()

            if self.current_char.isalpha():
                return self.get_variable()

            return self.get_next_symbol()

        return Token(Token.EOF, None)
