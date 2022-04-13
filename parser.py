from lexer import Token, Lexer, TokenType
from error import ParserError, ErrorCode


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
    """The Type node is constructed out of ID TokenType."""
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
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)

    def number(self) -> AST:
        """number : (MINUS | BIT_NOT)* (INTEGER | LPAREN expression RPAREN)"""
        token = self.current_token
        if token.type == TokenType.INTC:
            self.eat(TokenType.INTC)
            return Num(token)
        elif token.type == TokenType.FLOATC:
            self.eat(TokenType.FLOATC)
            return Num(token)
        elif token.type == TokenType.LRPAR:
            self.eat(TokenType.LRPAR)
            node = self.expression()
            self.eat(TokenType.RRPAR)
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(token, self.number())
            return node
        elif token.type == TokenType.BIT_NOT:
            self.eat(TokenType.BIT_NOT)
            node = UnaryOp(token, self.number())
            return node
        elif token.type == TokenType.LOGICAL_NOT:
            self.eat(TokenType.LOGICAL_NOT)
            node = UnaryOp(token, self.number())
            return node
        else:
            node = self.variable()
            return node

    def multiplicative(self) -> AST:
        """multiplication : number ((MUL | DIV) number)*"""
        node = self.number()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV, TokenType.MOD):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            elif token.type == TokenType.MOD:
                self.eat(TokenType.MOD)

            node = BinOp(left=node, op=token, right=self.number())

        return node

    def additive(self) -> AST:
        """
        addition : multiplication ((PLUS | MINUS) multiplication)*
        """
        node = self.multiplicative()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.multiplicative())

        return node          

    def comparative(self) -> AST:
        """
        compare : addition | (addition (EQUAL | NOT_EQUAL | LESS | GREATER | LESS_EQUAL | GREATER_EQUAL) addition)
        """
        node = self.additive()
        op = (TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL)
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
        op = (TokenType.BIT_AND, TokenType.BIT_OR, TokenType.LESS, TokenType.BIT_XOR, TokenType.BIT_LSHIFT, TokenType.BIT_RSHIFT)
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
        op = (TokenType.LOGICAL_AND, TokenType.LOGICAL_OR)
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
        self.eat(TokenType.LCPAR)
        nodes = self.statement_list()
        self.eat(TokenType.RCPAR)
    
        root = Block()
        root.children.extend(nodes)
        return root

    def statement_list(self):
        """
        statement_list : statement SEMI statement_list
        """
        results = []
        while self.current_token.type != TokenType.RCPAR:
            results.append(self.statement())
        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | declaration_statement
        """
        if self.current_token.type == TokenType.LCPAR:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.TYPE:
            node = self.assignment_statement()
            self.eat(TokenType.SEMI)
        elif self.current_token.type in (TokenType.INTC, TokenType.FLOATC):
            node = self.declaration_statement()
            self.eat(TokenType.SEMI)
        elif self.current_token.type == TokenType.SEMI:
            node = self.empty()
            self.eat(TokenType.SEMI)
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        return node

    def declaration_statement(self):
        """
        declaration_statement : INTC variable ASSIGN expr | FLOATC variable ASSIGN expr
        """
        type = self.current_token
        if type.type == TokenType.INTC:
            self.eat(TokenType.INTC)
        elif self.type.type == TokenType.FLOATC:
            self.eat(TokenType.FLOATC)
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expression()
        node = Declare(type, left, token, right)
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expression()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Type(self.current_token)
        self.eat(TokenType.TYPE)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        return node

    def error(self, error_code, token):
        raise ParserError(f"{error_code.value} -> {token}")
