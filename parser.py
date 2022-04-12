from lexer import Token, Lexer
from error import error


class AST:
    """Class that represents a node in the abstract syntax tree."""
    pass


class UnaryOp(AST):
    """
    Node that represents a unary operator.
    Attributes:
        
    """
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class BinOp(AST):
    """Node that represents a binary operator."""
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Block(AST):
    """Represents a 'BEGIN ... END' block"""
    def __init__(self):
        self.children = []


class Declare(AST):
    def __init__(self, type, left, op, right):
        self.type = type
        self.left = left
        self.token = self.op = op
        self.right = right


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Type(AST):
    """The Type node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            error(f"Expected {repr(token_type)}, recieved {repr(self.current_token.type)}")

    def number(self) -> AST:
        """number : (MINUS | BIT_NOT)* (INTEGER | LPAREN expression RPAREN)"""
        token = self.current_token
        if token.type == Token.INTC:
            self.eat(Token.INTC)
            return Num(token)
        elif token.type == Token.FLOATC:
            self.eat(Token.FLOATC)
            return Num(token)
        elif token.type == Token.LRPAR:
            self.eat(Token.LRPAR)
            node = self.expression()
            self.eat(Token.RRPAR)
            return node
        elif token.type == Token.MINUS:
            self.eat(Token.MINUS)
            node = UnaryOp(token, self.number())
            return node
        elif token.type == Token.BIT_NOT:
            self.eat(Token.BIT_NOT)
            node = UnaryOp(token, self.number())
            return node
        elif token.type == Token.LOGICAL_NOT:
            self.eat(Token.LOGICAL_NOT)
            node = UnaryOp(token, self.number())
            return node
        else:
            node = self.variable()
            return node

    def multiplicative(self) -> AST:
        """multiplication : number ((MUL | DIV) number)*"""
        node = self.number()

        while self.current_token.type in (Token.MUL, Token.DIV):
            token = self.current_token
            if token.type == Token.MUL:
                self.eat(Token.MUL)
            elif token.type == Token.DIV:
                self.eat(Token.DIV)

            node = BinOp(left=node, op=token, right=self.number())

        return node

    def additive(self) -> AST:
        """
        addition : multiplication ((PLUS | MINUS) multiplication)*
        """
        node = self.multiplicative()

        while self.current_token.type in (Token.PLUS, Token.MINUS):
            token = self.current_token
            if token.type == Token.PLUS:
                self.eat(Token.PLUS)
            elif token.type == Token.MINUS:
                self.eat(Token.MINUS)

            node = BinOp(left=node, op=token, right=self.multiplicative())

        return node          

    def comparative(self) -> AST:
        """
        compare : addition | (addition (EQUAL | NOT_EQUAL | LESS | GREATER | LESS_EQUAL | GREATER_EQUAL) addition)
        """
        node = self.additive()
        op = (Token.EQUAL, Token.NOT_EQUAL, Token.LESS, Token.GREATER, Token.LESS_EQUAL, Token.GREATER_EQUAL)
        token = self.current_token
        if token.type in op:
            for type in op:
                if token.type == type:
                    self.eat(type)
                    node = BinOp(left=node, op=token, right=self.additive())
                    return node
        else:
            return node

    def bitwise(self) -> AST:
        """
        compare : comparative | (comparative (BIT_AND | BIT_OR | BIT_XOR | BIT_LSHIFT | BIT_RSHIFT) comparative)
        """
        node = self.comparative()
        op = (Token.BIT_AND, Token.BIT_OR, Token.LESS, Token.BIT_XOR, Token.BIT_LSHIFT, Token.BIT_RSHIFT)
        token = self.current_token
        while token.type in op:
            for type in op:
                if token.type == type:
                    self.eat(type)
                    node = BinOp(left=node, op=token, right=self.comparative())
                    token = self.current_token
                    break
        return node

    def logical(self) -> AST:
        node = self.bitwise()
        op = (Token.LOGICAL_AND, Token.LOGICAL_OR)
        token = self.current_token
        while token.type in op:
            for type in op:
                if token.type == type:
                    self.eat(type)
                    node = BinOp(left=node, op=token, right=self.bitwise())
                    token = self.current_token
                    break
        return node

    def expression(self) -> AST:
        return self.logical()

    def program(self):
        """program : compound_statement DOT"""
        node = self.compound_statement()
        return node

    def compound_statement(self):
        """
        compound_statement: BEGIN statement_list END
        """
        self.eat(Token.LCPAR)
        nodes = self.statement_list()
        self.eat(Token.RCPAR)
    
        root = Block()
        root.children.extend(nodes)
        return root

    def statement_list(self):
        """
        statement_list : statement SEMI statement_list
        """
        results = []
        while self.current_token.type != Token.RCPAR:
            results.append(self.statement())
        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | declaration_statement
        """
        if self.current_token.type == Token.LCPAR:
            node = self.compound_statement()
        elif self.current_token.type == Token.TYPE:
            node = self.assignment_statement()
            self.eat(Token.SEMI)
        elif self.current_token.type in (Token.INTC, Token.FLOATC):
            node = self.declaration_statement()
            self.eat(Token.SEMI)
        elif self.current_token.type == Token.SEMI:
            node = self.empty()
            self.eat(Token.SEMI)
        else:
            error(f"Expected LCPAR, TYPE, SEMI, received {self.current_token.type}")
        return node

    def declaration_statement(self):
        """
        declaration_statement : INTC variable ASSIGN expr | FLOATC variable ASSIGN expr
        """
        if self.current_token.type == Token.INTC:
            type = Token(Token.INTC, "int")
            self.eat(Token.INTC)
        elif self.current_token.type == Token.FLOATC:
            type = Token(Token.FLOAT, "float")
            self.eat(Token.FLOATC)
        else:
            error(f"Expected INT, FLOAT, received {self.current_token.type}")
        left = self.variable()
        token = self.current_token
        self.eat(Token.ASSIGN)
        right = self.expression()
        node = Declare(type, left, token, right)
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(Token.ASSIGN)
        right = self.expression()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Type(self.current_token)
        self.eat(Token.TYPE)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def parse(self):
        node = self.program()
        if self.current_token.type != Token.EOF:
            error(f"Expected EOF, recieved {self.current_token.type}")
        return node
