from lexer import Lexer
from tokens import TokenType
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
        # If `token` is a constant
        if token.type in (TokenType.INTC, TokenType.FLOATC, TokenType.STRING):
            self.eat(token.type)
            return ast.Val(token)
        elif token.type == TokenType.LRPAR:  # If `token` is an expression with parentheses
            self.eat(TokenType.LRPAR)
            node = self.expression()
            self.eat(TokenType.RRPAR)
            return node
        # If `token` is a unary operator
        elif token.type in (TokenType.MINUS, TokenType.BIT_NOT, TokenType.LOGICAL_NOT):
            self.eat(token.type)
            return ast.UnaryOperator(token.type, self.term(), token=token)
        else:  # If `token` is a variable or function call
            variable = self.variable()
            if self.current_token.type != TokenType.LRPAR:
                return variable
            self.eat(TokenType.LRPAR)
            args = []
            if self.current_token.type != TokenType.RRPAR:
                args.append(self.expression())
            while self.current_token.type != TokenType.RRPAR:
                self.eat(TokenType.COMMA)
                args.append(self.expression())
            self.eat(TokenType.RRPAR)
            return ast.FunctionCall(variable.value, args, variable.token)

    def variable(self) -> ast.AST:
        """Reads the next token and checks if it is a TYPE."""
        node = ast.Variable(self.current_token.type,
                            self.current_token.value, token=self.current_token)
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
            num = ast.BinaryOperator(
                num, token.type, lower_prec(), token=token)
        return num

    # The next few lines establish the order of operations: multiplicative -> additive -> comparative -> bitwise -> logical

    def multiplicative(self) -> ast.AST:
        """multiplicative : term, {(MUL | DIV | MOD), term};"""
        return self.operation(
            (TokenType.MUL, TokenType.DIV, TokenType.MOD), self.term)

    def additive(self) -> ast.AST:
        """additive : multiplicative, {(PLUS | MINUS), multiplicative};"""
        return self.operation(
            (TokenType.PLUS, TokenType.MINUS), self.multiplicative)

    def comparative(self) -> ast.AST:
        """comparative : additive, {(EQUAL | NOT_EQUAL | LESS | GREATER | LESS_EQUAL | GREATER_EQUAL), additive};"""
        return self.operation((TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS,
                               TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL), self.additive)

    def bitwise(self) -> ast.AST:
        """bitwise : comparative, {(BIT_AND | BIT_OR | BIT_XOR | BIT_LSHIFT | BIT_RSHIFT), comparative};"""
        return self.operation((TokenType.BIT_AND, TokenType.BIT_OR, TokenType.LESS,
                               TokenType.BIT_XOR, TokenType.BIT_LSHIFT, TokenType.BIT_RSHIFT), self.comparative)

    def logical(self) -> ast.AST:
        """logical : bitwise, {(LOGICAL_AND | LOGICAL_OR), bitwise};"""
        return self.operation(
            (TokenType.LOGICAL_AND, TokenType.LOGICAL_OR), self.bitwise)

    # expression : logical; the function `expression` points to the operator with the lowest precedence.
    expression = logical

    def declaration_statement(self) -> ast.AST:
        """declaration_statement: (INTC | FLOATC | STRING), variable, ASSIGN, expression; """
        type = self.current_token.type
        self.eat((TokenType.INTC, TokenType.FLOATC, TokenType.STRING))
        name = self.variable()
        self.eat(TokenType.ASSIGN)
        expr = self.expression()
        return ast.DeclarationStatement(type, name, expr)

    def function_declaration(self) -> ast.AST:
        """function_declaration: (VOID, INTC, FLOATC, STRING), variable, LRPAR, ([(INTC | FLOATC | STRING), variable, [COMMA, ((INTC | FLOATC | STRING), variable)]]), RRPAR, block; """
        type = self.current_token.type
        self.eat((TokenType.VOID, TokenType.INTC,
                 TokenType.FLOATC, TokenType.STRING))
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
        """assignment_statement_or_function_call: (variable, (ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN | BIT_AND_ASSIGN | BIT_OR_ASSIGN | BIT_XOR_ASSIGN | BIT_LSHIFT_ASSIGN | BIT_RSHIFT_ASSIGN), expression) | (variable, LRPAR, [expression, {COMMA, expression}] RRPAR); """
        variable = self.variable()
        token = self.current_token
        if token.type in (TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, TokenType.MUL_ASSIGN, TokenType.DIV_ASSIGN, TokenType.MOD_ASSIGN,
                          TokenType.BIT_AND_ASSIGN, TokenType.BIT_OR_ASSIGN, TokenType.BIT_XOR_ASSIGN, TokenType.BIT_LSHIFT_ASSIGN, TokenType.BIT_RSHIFT_ASSIGN):
            self.eat((TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, TokenType.MUL_ASSIGN, TokenType.DIV_ASSIGN, TokenType.MOD_ASSIGN,
                     TokenType.BIT_AND_ASSIGN, TokenType.BIT_OR_ASSIGN, TokenType.BIT_XOR_ASSIGN, TokenType.BIT_LSHIFT_ASSIGN, TokenType.BIT_RSHIFT_ASSIGN))
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
        """line_statement: (assignment_statement_or_function_call | declaration_statement); """
        if self.current_token.type == TokenType.TYPE:
            node = self.assignment_statement_or_function_call()
        elif self.current_token.type in (TokenType.INTC, TokenType.FLOATC, TokenType.STRING):
            node = self.declaration_statement()
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        return node

    def statement(self) -> ast.AST:
        """statement: (block | while_statement | do_while_statement | for_statement | ifelse_statement | SEMI | (line_statement, SEMI), break_statement); """
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
        elif self.current_token.type == TokenType.BREAK:
            node = self.break_statement()
        elif self.current_token.type == TokenType.CONTINUE:
            node = self.continue_statement()
        elif self.current_token.type == TokenType.RETURN:
            node = self.return_statement()
        elif self.current_token.type == TokenType.SEMI:
            node = self.empty()
            self.eat(TokenType.SEMI)
        else:
            node = self.line_statement()
            self.eat(TokenType.SEMI)
        return node

    def statement_list(self) -> ast.AST:
        """statement_list: {statement}; """
        results = []
        while self.current_token.type != TokenType.RCPAR:
            results.append(self.statement())
        return results

    def if_else_statement(self) -> ast.AST:
        """if_else_statement: IF, LRPAR, expression, RRPAR, block, {ELSE, IF, LRPAR, expression, RRPAR, block}, [ELSE, block]; """
        self.eat(TokenType.IF)
        self.eat(TokenType.LRPAR)
        condition = self.expression()
        self.eat(TokenType.RRPAR)
        block = self.block()
        block_list = [(condition, block)]
        last_block = None
        while self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            if self.current_token.type == TokenType.IF:
                self.eat(TokenType.IF)
                self.eat(TokenType.LRPAR)
                condition = self.expression()
                self.eat(TokenType.RRPAR)
                block = self.block()
                block_list.append((condition, block))
            elif self.current_token.type == TokenType.LCPAR:
                last_block = self.block()
                break
            else:
                self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        return ast.IfElse(block_list, last_block)

    def for_loop(self) -> ast.AST:
        """for_loop: FOR, LRPAR, line_statement, expression, line_statement, RRPAR, block; """
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
        """while_loop: WHILE, LRPAR, expression, RRPAR, block; """
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LRPAR)
        expr = self.expression()
        self.eat(TokenType.RRPAR)
        block = self.block()
        return ast.WhileLoop(expr, block)

    def do_while_loop(self) -> ast.AST:
        """do_while_loop: DO, block, WHILE, LRPAR, expression, RRPAR, SEMI; """
        self.eat(TokenType.DO)
        block = self.block()
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LRPAR)
        expr = self.expression()
        self.eat(TokenType.RRPAR)
        self.eat(TokenType.SEMI)
        return ast.DoWhile(expr, block)

    def break_statement(self) -> ast.AST:
        curr_token = self.current_token
        self.eat(TokenType.BREAK)
        self.eat(TokenType.SEMI)
        return ast.BreakStatement(curr_token)

    def continue_statement(self) -> ast.AST:
        curr_token = self.current_token
        self.eat(TokenType.CONTINUE)
        self.eat(TokenType.SEMI)
        return ast.ContinueStatement(curr_token)

    def return_statement(self) -> ast.AST:
        curr_token = self.current_token
        self.eat(TokenType.RETURN)
        if self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            return ast.ReturnStatement(ast.NoOperation(), curr_token)
        else:
            expr = self.expression()
            self.eat(TokenType.SEMI)
            return ast.ReturnStatement(expr, curr_token)

    def block(self) -> ast.AST:
        """block: LCPAR, statement_list, RCPAR; """
        self.eat(TokenType.LCPAR)
        nodes = self.statement_list()
        self.eat(TokenType.RCPAR)
        return ast.Block(nodes)

    def program(self) -> ast.AST:
        """program: {function_declaration}"""
        functions = []
        while self.current_token.type != TokenType.EOF:
            functions.append(self.function_declaration())
        return ast.Program(functions)

    def parse(self) -> ast.AST:
        """Parses the input into an abstract syntax tree."""
        return self.program()

    def error(self, error_code, token):
        """Throws an error and states the current character, line, and column on which the error happened"""
        raise ParserError(f"{error_code.value} -> {token}")
