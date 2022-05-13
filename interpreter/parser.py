from lexer import Lexer
from token import TokenType
from error import ParserError, ErrorCode
import ast

class Parser(object):
    """
    Parser class that converts tokens into an abstract syntax tree.

    Attributes:
        lexer (Lexer): the lexer that converts the code into tokens.
        current_token (Token): the current token.
    """
    def __init__(self, lexer: Lexer):
        """
        Inits parser class.
        Args:
            lexer (Lexer): the lexer that converts the code into tokens.
        """
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type: TokenType):
        """
        Compare the current token type with the passed token type(s), and "eat" the current token 
        if they match and assign the next token to the self.current_token, otherwise raise an exception.
        Args:
            token_type (TokenType or tuple[TokenType]): The type of token to eat.
        """
        if (type(token_type) is str and self.current_token.type == token_type) or \
            (type(token_type) is tuple and self.current_token.type in token_type):
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)

    def empty(self):
        """Node that does nothing."""
        return ast.NoOperation()

    def term(self) -> ast.AST:
        """number : ([MINUS | BIT_NOT | LOGICAL_NOT], ((INTC | FLOATC | STRING) | (LRPAR, expression, LRPAR))) | variable;"""
        token = self.current_token
        if token.type in (TokenType.INTC, TokenType.FLOATC, TokenType.STRING): # If `token` is a constant
            self.eat(token.type)
            return ast.Val(token)
        elif token.type == TokenType.LRPAR: # If `token` is an expression with parentheses
            self.eat(TokenType.LRPAR)
            node = self.expression()
            self.eat(TokenType.RRPAR)
            return node
        elif token.type in (TokenType.MINUS, TokenType.BIT_NOT, TokenType.LOGICAL_NOT): # If `token` is a unary operator
            self.eat(token.type)
            return ast.UnaryOperator(token.type, self.term(), token=token)
        else: # If `token` is a variable
            return self.variable()

    def variable(self):
        """Reads the next token and checks if it is a TYPE."""
        node = ast.Variable(self.current_token.type, self.current_token.value, token=self.current_token)
        self.eat(TokenType.TYPE)
        return node

    def operation(self, operations: tuple, lower_prec) -> ast.AST:
        """
        Function that handles a series of binary operations with the same precedence (Ex. "*", "/", and "%").
        When it receives an operation with lower precedence, go to the corresponding function.
        """
        num = lower_prec()
        while self.current_token.type in operations:
            token = self.current_token
            self.eat(token.type)
            num = ast.BinaryOperator(num, token.type, lower_prec(), token=token)
        return num

    # The next few lines establish the order of operations: multiplicative -> additive -> comparative -> bitwise -> logical

    """multiplicative : term, {(MUL | DIV | MOD), term};"""
    multiplicative = lambda self: self.operation((TokenType.MUL, TokenType.DIV, TokenType.MOD), self.term)

    """additive : multiplicative, {(PLUS | MINUS), multiplicative};"""
    additive = lambda self: self.operation((TokenType.PLUS, TokenType.MINUS), self.multiplicative)

    """comparative : additive, {(EQUAL | NOT_EQUAL | LESS | GREATER | LESS_EQUAL | GREATER_EQUAL), additive};"""
    comparative = lambda self: self.operation((TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL), self.additive)

    """bitwise : comparative, {(BIT_AND | BIT_OR | BIT_XOR | BIT_LSHIFT | BIT_RSHIFT), comparative};"""
    bitwise = lambda self: self.operation((TokenType.BIT_AND, TokenType.BIT_OR, TokenType.LESS, TokenType.BIT_XOR, TokenType.BIT_LSHIFT, TokenType.BIT_RSHIFT), self.comparative)

    """logical : bitwise, {(LOGICAL_AND | LOGICAL_OR), bitwise};"""
    logical = lambda self: self.operation((TokenType.LOGICAL_AND, TokenType.LOGICAL_OR), self.bitwise)

    """
    expression : logical;
    The function `expression` always points to the operator with the lowest precedence.
    """
    expression = logical

    def declaration_statement(self) -> ast.AST:
        """declaration_statement : (INTC | FLOATC | STRING), variable, ASSIGN, expression;"""
        type = self.current_token.type
        self.eat((TokenType.INTC, TokenType.FLOATC, TokenType.STRING))
        name = self.variable()
        self.eat(TokenType.ASSIGN)
        expr = self.expression()
        return ast.DeclarationStatement(type, name, expr)

    def function_declaration(self) -> ast.AST:
        """function_declaration : FUNCTION, variable, LRPAR, ([(INTC | FLOATC | STRING), variable, [COMMA, ((INTC | FLOATC | STRING), variable)]]), RRPAR, block;"""
        type = self.current_token.type
        self.eat(TokenType.FUNCTION)
        name = self.variable()
        self.eat(TokenType.LRPAR)
        args = []
        if self.current_token.type != TokenType.RRPAR:
            arg_type = self.current_token.type
            self.eat((TokenType.INTC, TokenType.FLOATC, TokenType.STRING))
            var = self.variable()
            args.append(ast.FunctionArgument(arg_type, var.token))
            while self.current_token.type != TokenType.RRPAR:
                self.eat(TokenType.COMMA)
                arg_type = self.current_token.type
                self.eat((TokenType.INTC, TokenType.FLOATC, TokenType.STRING))
                var = self.variable()
                args.append(ast.FunctionArgument(arg_type, var.token))
        self.eat(TokenType.RRPAR)
        body = self.block()
        return ast.FunctionDeclaration(type, name, args, body)        

    def assignment_statement_or_function_call(self) -> ast.AST:
        """assignment_statement_or_function_call : (variable, (ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN | BIT_AND_ASSIGN | BIT_OR_ASSIGN | BIT_XOR_ASSIGN | BIT_LSHIFT_ASSIGN | BIT_RSHIFT_ASSIGN), expression) | (variable, LRPAR, [expression, {COMMA, expression}] RRPAR);"""
        variable = self.variable()
        token = self.current_token
        if token.type in (TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, TokenType.MUL_ASSIGN, TokenType.DIV_ASSIGN, TokenType.MOD_ASSIGN, TokenType.BIT_AND_ASSIGN, TokenType.BIT_OR_ASSIGN, TokenType.BIT_XOR_ASSIGN, TokenType.BIT_LSHIFT_ASSIGN, TokenType.BIT_RSHIFT_ASSIGN):   
            self.eat((TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, TokenType.MUL_ASSIGN, TokenType.DIV_ASSIGN, TokenType.MOD_ASSIGN, TokenType.BIT_AND_ASSIGN, TokenType.BIT_OR_ASSIGN, TokenType.BIT_XOR_ASSIGN, TokenType.BIT_LSHIFT_ASSIGN, TokenType.BIT_RSHIFT_ASSIGN))
            value = self.expression()
            return ast.AssignmentStatement(variable, token.type, value, token)
        else:
            self.eat(TokenType.LRPAR)
            args = []
            if self.current_token.type != TokenType.RRPAR:
                args.append(self.expression())
            while self.current_token.type != TokenType.RRPAR:
                self.eat(TokenType.COMMA)
                args.append(self.expression())
            self.eat(TokenType.RRPAR)
            return ast.FunctionCall(variable.value, args, variable.token)


    def line_statement(self) -> ast.AST:
        """line_statement : (assignment_statement_or_function_call | declaration_statement);"""
        if self.current_token.type == TokenType.TYPE:
            node = self.assignment_statement_or_function_call()
        elif self.current_token.type in (TokenType.INTC, TokenType.FLOATC, TokenType.STRING):
            node = self.declaration_statement()
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        return node

    def statement(self) -> ast.AST:
        """statement : (block | while_statement | do_while_statement | for_statement | ifelse_statement | SEMI | (line_statement, SEMI));"""
        if self.current_token.type == TokenType.LCPAR:
            node = self.block()
        elif self.current_token.type == TokenType.IF:
            node = self.if_else_statement()
        elif self.current_token.type == TokenType.FOR:
            node = self.for_loop()
        elif self.current_token.type == TokenType.WHILE:
            node = self.while_loop()
        elif self.current_token.type == TokenType.DO:
            node = self.do_while_loop()
        elif self.current_token.type == TokenType.SEMI:
            node = self.empty()
            self.eat(TokenType.SEMI)
        else:
            node = self.line_statement()
            self.eat(TokenType.SEMI)
        return node

    def statement_list(self) -> ast.AST:
        """statement_list : {statement};"""
        results = []
        while self.current_token.type != TokenType.RCPAR:
            results.append(self.statement())
        return results


    def if_else_statement(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LRPAR)
        con1 = self.expression()
        self.eat(TokenType.RRPAR)
        block1 = self.block()
        mid = [(con1, block1)]
        end = None
        while self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            if self.current_token.type == TokenType.IF:
                self.eat(TokenType.IF)
                self.eat(TokenType.LRPAR)
                con = self.expression()
                self.eat(TokenType.RRPAR)
                block = self.block()
                mid.append((con, block))
            elif self.current_token.type == TokenType.LCPAR:
                end = self.block()
                break
            else:
                self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        return ast.IfElse(mid, end)
        

    def for_loop(self) -> ast.AST:
        """for_loop : FOR, LRPAR, line_statement, expression, line_statement, RRPAR, block;"""
        self.eat(TokenType.FOR)
        self.eat(TokenType.LRPAR)
        init = self.line_statement()
        self.eat(TokenType.SEMI)
        expr = self.expression()
        self.eat(TokenType.SEMI)
        inc = self.line_statement()
        self.eat(TokenType.RRPAR)
        block = self.block()
        return ast.ForLoop(init, expr, inc, block)

    def while_loop(self) -> ast.AST:
        """while_loop : WHILE, LRPAR, expression, RRPAR, block;"""
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LRPAR)
        expr = self.expression()
        self.eat(TokenType.RRPAR)
        block = self.block()
        return ast.WhileLoop(expr, block)

    def do_while_loop(self) -> ast.AST:
        """do_while_loop : DO, block, WHILE, LRPAR, expression, RRPAR, SEMI;"""
        self.eat(TokenType.DO)
        block = self.block()
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LRPAR)
        expr = self.expression()
        self.eat(TokenType.RRPAR)
        self.eat(TokenType.SEMI)
        return ast.DoWhile(expr, block)

    def block(self) -> ast.AST:
        """block: LCPAR, statement_list, RCPAR;"""
        self.eat(TokenType.LCPAR)
        nodes = self.statement_list()
        self.eat(TokenType.RCPAR)
        return ast.Block(nodes)

    def program(self) -> ast.AST:
        """program : {function_declaration}"""
        functions = []
        while self.current_token.type == TokenType.FUNCTION:
            functions.append(self.function_declaration())
        return ast.Program(functions)

    def parse(self) -> ast.AST:
        """Parses the input into an abstract syntax tree."""
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        return node

    def error(self, error_code, token):
        """Throws an error and states the current character, line, and column on which the error happened"""
        raise ParserError(f"{error_code.value} -> {token}")
