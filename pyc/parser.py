"""
ICS3U
Paul Chen
This file holds the `Parser` class that converts tokens into an abstract syntax tree.
"""

from typing import Callable, List, Tuple, Union

import ast_nodes
from error import ErrorCode, ParserError
from lexer import Lexer
from tokens import Token, TokenType


class Parser(object):
    """
    Parser class that converts tokens into an abstract syntax tree. Most of the docstrings in this
    class use EBNF notation (https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) to
    illustrate the code.

    Attributes:
        lexer (Lexer): the lexer that converts the code into tokens.
        current_token (Token): the current token.
    """

    def __init__(self, lexer: Lexer) -> None:
        """
        Inits parser class.
        Args:
            lexer (Lexer): the lexer that converts the code into tokens.
        """
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat_token(self, token_type: Union[TokenType, Tuple[TokenType, ...]]) -> None:
        """
        Compare the current token type with the passed token type(s), and "eat" the current token
        if they match and assign the next token to the self.current_token, otherwise raise an exception.
        Args:
            token_type (TokenType or tuple[TokenType]): The type of token to eat.
        """
        if (type(token_type) is TokenType and self.current_token.type == token_type) or \
                (type(token_type) is tuple and self.current_token.type in token_type):
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)

    def peek_nth_next_token(self, n: int) -> Token:
        """
        This method reads ahead n tokens, and returns the nth next token.
        """
        return self.lexer.peek_nth_next_token(n)

    def parse_term(self) -> ast_nodes.ASTNode:
        """
        term:
            [MINUS | BIT_NOT | LOGICAL_NOT], ((INT | FLOAT | STRING) |
            (LRPAR, expression, LRPAR)) |
            function_call |
            variable |
            list
            ;
        """
        token = self.current_token
        # If `token` is an int, float, or string.
        if token.type in (TokenType.INTL, TokenType.FLOATL, TokenType.STRINGL):
            self.eat_token(token.type)
            return ast_nodes.ValueLiteralNode(token)

        # If `token` is a unary operator.
        elif token.type in (TokenType.MINUS, TokenType.BIT_NOT, TokenType.LOGICAL_NOT):
            self.eat_token(token.type)
            return ast_nodes.UnaryOperatorNode(token.type, self.parse_term(), token=token)

        # If the next few tokens represent a cast operator.
        elif token.type == TokenType.LRPAR and self.peek_nth_next_token(0).type in (
                TokenType.INT, TokenType.FLOAT, TokenType.STRING):
            self.eat_token(TokenType.LRPAR)
            token.type = self.current_token.type
            self.eat_token(token.type)
            self.eat_token(TokenType.RRPAR)
            return ast_nodes.CastOperatorNode(token.type, self.parse_term(), token=token)

        # If the next few tokens represent an expression wrapped in parentheses.
        elif token.type == TokenType.LRPAR:
            self.eat_token(TokenType.LRPAR)
            node = self.parse_expression()
            self.eat_token(TokenType.RRPAR)
            return node

        # If `token` is a list.
        elif token.type == TokenType.LCPAR:
            return self.parse_initializer_list()

        # If `token` is a function call.
        elif token.type == TokenType.TYPE and self.peek_nth_next_token(0).type == TokenType.LRPAR:
            return self.parse_function_call_statement()

        # If the next token is a variable.
        else:
            return self.parse_variable()

    def parse_initializer_list(self) -> ast_nodes.InitializerListLiteralNode:
        """list: LCPAR, [expression, {COMMA, expression}], RCPAR;"""
        self.eat_token(TokenType.LCPAR)
        list_elements = []
        if self.current_token.type != TokenType.RCPAR:
            list_elements.append(self.parse_expression())
        while self.current_token.type != TokenType.RCPAR:
            self.eat_token(TokenType.COMMA)
            list_elements.append(self.parse_expression())
        self.eat_token(TokenType.RCPAR)
        return ast_nodes.InitializerListLiteralNode(list_elements)

    def parse_variable(self) -> ast_nodes.VariableNode:
        """variable: TYPE, [LSPAR, expression, RSPAR];"""
        token = self.current_token
        self.eat_token(TokenType.TYPE)
        indices = []
        while self.current_token.type == TokenType.LSPAR:
            self.eat_token(TokenType.LSPAR)
            if self.current_token.type != TokenType.RSPAR:
                expr_index = self.parse_expression()
            else:
                expr_index = ast_nodes.NoOperationStatementNode()
            self.eat_token(TokenType.RSPAR)
            indices.append(expr_index)
        return ast_nodes.VariableNode(token.type, token.value, indices, token)

    def operation(self, operations: Tuple[TokenType, ...], lower_prec: Callable) -> ast_nodes.ASTNode:
        """
        Function that handles a series of binary operations with the same precedence (Ex. "*", "/", and "%").
        When it receives an operation with lower precedence, go to the corresponding function.

        Arguments:
            operations (Tuple[TokenType, ...]): operations at current precedence.
            lower_prec (Callable): operation at next lowest precedence.
        """
        num = lower_prec()
        while self.current_token.type in operations:
            token = self.current_token
            self.eat_token(token.type)
            num = ast_nodes.BinaryOperatorNode(num, token.type, lower_prec(), token=token)
        return num

    # The next few lines establish the order of operations:
    # multiplicative -> additive -> comparative -> bitwise -> logical

    def parse_multiplicative_operation(self) -> ast_nodes.ASTNode:
        """multiplicative: term, {(MUL | DIV | MOD), term};"""
        return self.operation((TokenType.MUL, TokenType.DIV, TokenType.MOD), self.parse_term)

    def parse_additive_operation(self) -> ast_nodes.ASTNode:
        """additive: multiplicative, {(PLUS | MINUS), multiplicative};"""
        return self.operation((TokenType.PLUS, TokenType.MINUS), self.parse_multiplicative_operation)

    def parse_comparative_operation(self) -> ast_nodes.ASTNode:
        """comparative: additive, {(EQUAL | NOT_EQUAL | LESS | GREATER | LESS_EQUAL | GREATER_EQUAL), additive};"""
        return self.operation((TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS,
                               TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL),
                              self.parse_additive_operation)

    def parse_bitwise_operation(self) -> ast_nodes.ASTNode:
        """bitwise: comparative, {(BIT_AND | BIT_OR | BIT_XOR | BIT_LSHIFT | BIT_RSHIFT), comparative};"""
        return self.operation((TokenType.BIT_AND, TokenType.BIT_OR, TokenType.LESS,
                               TokenType.BIT_XOR, TokenType.BIT_LSHIFT, TokenType.BIT_RSHIFT),
                              self.parse_comparative_operation)

    def parse_logical_operation(self) -> ast_nodes.ASTNode:
        """logical: bitwise, {(LOGICAL_AND | LOGICAL_OR), bitwise};"""
        return self.operation((TokenType.LOGICAL_AND, TokenType.LOGICAL_OR), self.parse_bitwise_operation)

    # expression: logical;
    # The function `parse_expression` points to the operator with the lowest precedence.
    parse_expression = parse_logical_operation

    def parse_declaration_statement(self) -> ast_nodes.DeclarationStatementNode:
        """declaration_statement: (INT | FLOAT | STRING), variable, [ASSIGN, expression]; """
        token_type = self.current_token.type
        self.eat_token((TokenType.INT, TokenType.FLOAT, TokenType.STRING))
        name = self.parse_variable()
        if self.current_token.type == TokenType.SEMI:
            return ast_nodes.DeclarationStatementNode(token_type, name, ast_nodes.NoOperationStatementNode())
        else:
            self.eat_token(TokenType.ASSIGN)
            expr = self.parse_expression()
            return ast_nodes.DeclarationStatementNode(token_type, name, expr)

    def parse_assignment_statement(self) -> ast_nodes.AssignmentStatementNode:
        """
        assignment_statement
            variable,
            (ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN | BIT_AND_ASSIGN |
            BIT_OR_ASSIGN | BIT_XOR_ASSIGN | BIT_LSHIFT_ASSIGN | BIT_RSHIFT_ASSIGN),
            expression;
        """
        variable = self.parse_variable()
        token = self.current_token

        # Runs if the next token is an assignment statement operator.
        self.eat_token((TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
                        TokenType.MUL_ASSIGN, TokenType.DIV_ASSIGN, TokenType.MOD_ASSIGN,
                        TokenType.BIT_AND_ASSIGN, TokenType.BIT_OR_ASSIGN, TokenType.BIT_XOR_ASSIGN,
                        TokenType.BIT_LSHIFT_ASSIGN, TokenType.BIT_RSHIFT_ASSIGN))
        value = self.parse_expression()
        return ast_nodes.AssignmentStatementNode(variable, token.type, value, token)

    def parse_single_line_statement(self) -> ast_nodes.ASTNode:
        """line_statement: (function_call | assignment_statement | declaration_statement); """
        node = ast_nodes.NoOperationStatementNode()
        if self.current_token.type == TokenType.TYPE and self.peek_nth_next_token(0).type == TokenType.LRPAR:
            node = self.parse_function_call_statement()
        elif self.current_token.type == TokenType.TYPE:
            node = self.parse_assignment_statement()
        elif self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.STRING):
            node = self.parse_declaration_statement()
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        return node

    def parse_statement(self) -> ast_nodes.ASTNode:
        """
        statement:
            (block | while_statement | do_while_statement | for_statement | if_else_statement | SEMI |
            (line_statement, SEMI), break_statement, continue_statement, return_statement);
        """
        if self.current_token.type == TokenType.LCPAR:
            node = self.parse_block_statement()
        elif self.current_token.type == TokenType.IF:
            node = self.parse_if_else_statement()
        elif self.current_token.type == TokenType.FOR:
            node = self.parse_for_loop()
        elif self.current_token.type == TokenType.WHILE:
            node = self.parse_while_loop()
        elif self.current_token.type == TokenType.DO:
            node = self.parse_do_while_loop()
        elif self.current_token.type == TokenType.BREAK:
            node = self.parse_break_statement()
        elif self.current_token.type == TokenType.CONTINUE:
            node = self.parse_continue_statement()
        elif self.current_token.type == TokenType.RETURN:
            node = self.parse_return_statement()
        elif self.current_token.type == TokenType.SEMI:
            node = ast_nodes.NoOperationStatementNode()
            self.eat_token(TokenType.SEMI)
        else:
            node = self.parse_single_line_statement()
            self.eat_token(TokenType.SEMI)
        return node

    def parse_statement_list(self) -> List[ast_nodes.ASTNode]:
        """statement_list: {statement}; """
        results = []
        while self.current_token.type != TokenType.RCPAR:
            results.append(self.parse_statement())
        return results

    def parse_block_statement(self) -> ast_nodes.BlockStatementNode:
        """block: LCPAR, statement_list, RCPAR; """
        self.eat_token(TokenType.LCPAR)
        nodes = self.parse_statement_list()
        self.eat_token(TokenType.RCPAR)
        return ast_nodes.BlockStatementNode(nodes)

    def parse_if_else_statement(self) -> ast_nodes.IfElseStatementNode:
        """
        if_else_statement:
            IF, LRPAR, parse_expression, RRPAR,
                statement,
            {ELSE, IF, LRPAR, parse_expression, RRPAR,
                statement},
            [ELSE,
                statement]
            ; """
        self.eat_token(TokenType.IF)
        self.eat_token(TokenType.LRPAR)
        condition = self.parse_expression()
        self.eat_token(TokenType.RRPAR)
        block = self.parse_statement()
        block_list = [(condition, block)]
        last_block = None
        while self.current_token.type == TokenType.ELSE:
            self.eat_token(TokenType.ELSE)
            if self.current_token.type == TokenType.IF:
                self.eat_token(TokenType.IF)
                self.eat_token(TokenType.LRPAR)
                condition = self.parse_expression()
                self.eat_token(TokenType.RRPAR)
                block = self.parse_statement()
                block_list.append((condition, block))
            else:
                last_block = self.parse_statement()
                break
        return ast_nodes.IfElseStatementNode(block_list, last_block)

    def parse_for_loop(self) -> ast_nodes.ForLoopNode:
        """for_loop: FOR, LRPAR, line_statement, expression, line_statement, RRPAR, block; """
        self.eat_token(TokenType.FOR)
        self.eat_token(TokenType.LRPAR)
        init = self.parse_single_line_statement()
        self.eat_token(TokenType.SEMI)
        expr = self.parse_expression()
        self.eat_token(TokenType.SEMI)
        inc = self.parse_single_line_statement()
        self.eat_token(TokenType.RRPAR)
        block = self.parse_statement()
        return ast_nodes.ForLoopNode(init, expr, inc, block)

    def parse_while_loop(self) -> ast_nodes.WhileLoopNode:
        """while_loop: WHILE, LRPAR, expression, RRPAR, block; """
        self.eat_token(TokenType.WHILE)
        self.eat_token(TokenType.LRPAR)
        expr = self.parse_expression()
        self.eat_token(TokenType.RRPAR)
        block = self.parse_statement()
        return ast_nodes.WhileLoopNode(expr, block)

    def parse_do_while_loop(self) -> ast_nodes.DoWhileLoopNode:
        """do_while_loop: DO, statement, WHILE, LRPAR, expression, RRPAR, SEMI; """
        self.eat_token(TokenType.DO)
        block = self.parse_statement()
        self.eat_token(TokenType.WHILE)
        self.eat_token(TokenType.LRPAR)
        expr = self.parse_expression()
        self.eat_token(TokenType.RRPAR)
        self.eat_token(TokenType.SEMI)
        return ast_nodes.DoWhileLoopNode(expr, block)

    def parse_break_statement(self) -> ast_nodes.BreakStatementNode:
        """break_statement: BREAK, SEMI;"""
        curr_token = self.current_token
        self.eat_token(TokenType.BREAK)
        self.eat_token(TokenType.SEMI)
        return ast_nodes.BreakStatementNode(curr_token)

    def parse_continue_statement(self) -> ast_nodes.ContinueStatementNode:
        """continue_statement: CONTINUE, SEMI;"""
        curr_token = self.current_token
        self.eat_token(TokenType.CONTINUE)
        self.eat_token(TokenType.SEMI)
        return ast_nodes.ContinueStatementNode(curr_token)

    def parse_return_statement(self) -> ast_nodes.ReturnStatementNode:
        """return_statement: RETURN, [expression], SEMI;"""
        curr_token = self.current_token
        self.eat_token(TokenType.RETURN)
        if self.current_token.type == TokenType.SEMI:
            self.eat_token(TokenType.SEMI)
            return ast_nodes.ReturnStatementNode(ast_nodes.NoOperationStatementNode(), curr_token)
        else:
            expr = self.parse_expression()
            self.eat_token(TokenType.SEMI)
            return ast_nodes.ReturnStatementNode(expr, curr_token)

    def parse_function_declaration_statement(self) -> ast_nodes.FunctionDeclarationStatementNode:
        """
        function_declaration:
            (VOID | INT | FLOAT | STRING), variable, LRPAR,
                ([(INT | FLOAT | STRING), variable, [COMMA, ((INT | FLOAT | STRING), variable)]]),
            RRPAR,
            block;
        """
        # Read the type and name of function.
        token_type = self.current_token.type
        self.eat_token((TokenType.VOID, TokenType.INT, TokenType.FLOAT, TokenType.STRING))
        name = self.parse_variable()
        if len(name.indices) != 0:
            self.error(ErrorCode.ARRAY_AS_FUNCTION_RETURN, name.token)

        # Read function args.
        args = []
        self.eat_token(TokenType.LRPAR)

        # If the function args list is not empty.
        if self.current_token.type != TokenType.RRPAR:

            # Reads the first function argument.
            arg_type = self.current_token.type
            self.eat_token((TokenType.INT, TokenType.FLOAT, TokenType.STRING))
            var = self.parse_variable()
            args.append(ast_nodes.FunctionArgument(arg_type, var.name, len(var.indices)))

            # Keeps reading all the other ones.
            while self.current_token.type != TokenType.RRPAR:
                self.eat_token(TokenType.COMMA)
                arg_type = self.current_token.type
                self.eat_token((TokenType.INT, TokenType.FLOAT, TokenType.STRING))
                var = self.parse_variable()
                args.append(ast_nodes.FunctionArgument(arg_type, var.name, len(var.indices)))

        self.eat_token(TokenType.RRPAR)

        # Reads the main function body.
        body = self.parse_block_statement()

        return ast_nodes.FunctionDeclarationStatementNode(token_type, name, args, body)

    def parse_function_call_statement(self) -> ast_nodes.FunctionCallStatementNode:
        """
        function_call: variable, LRPAR, [expression, {COMMA, expression}] RRPAR;
        """
        variable = self.parse_variable()
        self.eat_token(TokenType.LRPAR)

        # Read function arguments.
        args = []
        if self.current_token.type != TokenType.RRPAR:
            args.append(self.parse_expression())
        while self.current_token.type != TokenType.RRPAR:
            self.eat_token(TokenType.COMMA)
            args.append(self.parse_expression())

        self.eat_token(TokenType.RRPAR)
        return ast_nodes.FunctionCallStatementNode(variable.name, args, variable.token)

    def parse_program(self) -> ast_nodes.ProgramNode:
        """program: {function_declaration | declaration_statement}"""
        statements = []
        while self.current_token.type != TokenType.EOF:
            if self.peek_nth_next_token(1).type == TokenType.LRPAR:
                statements.append(self.parse_function_declaration_statement())
            else:
                statements.append(self.parse_declaration_statement())
                self.eat_token(TokenType.SEMI)
        return ast_nodes.ProgramNode(statements)

    def parse(self) -> ast_nodes.ProgramNode:
        """Parses the input into an abstract syntax tree."""
        return self.parse_program()

    def error(self, error_code, token):
        """Throws an error and states the current character, line, and column on which the error happened"""
        raise ParserError(f"{error_code.value} -> {token}")
