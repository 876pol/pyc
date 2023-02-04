"""
ICS3U
Paul Chen
This file holds the `Interpreter` class that runs an abstract syntax tree.
"""
import value
from ast import BuiltinFunction, AST, FunctionCall, UnaryOperator, BinaryOperator, CastOperator, Val, ListVal, \
    ListRead, ListAssign, Variable, DeclarationStatement, AssignmentStatement, Block, IfElse, ForLoop, WhileLoop, \
    DoWhile, FunctionDeclaration, BreakStatement, ContinueStatement, ReturnStatement, Program
from lexer import TokenType
from error import BreakException, ContinueException, ErrorCode, InterpreterError, ReturnException
from library import LIBRARY_FUNCTIONS
from linked_dict import LinkedDict
from parser import Parser
from value import build_value, object_to_identifier, Function, identifier_to_object, Value


class Interpreter(object):
    """
    Interpreter class that reads an abstract syntax tree and runs the program.

    Attributes:
        parser (Parser): the parser that converts tokens into an abstract syntax tree.
        scopes (LinkedDict): data structure that holds all variables in all scopes.
    """

    def __init__(self, parser: Parser):
        """
        Inits interpreter class.
        Args:
            parser (Parser): the parser.
        """
        self.parser = parser
        self.scopes = LinkedDict()

    def interpret(self) -> int:
        """
        Runs the interpreter.

        Returns:
            int: return code of interpreted program.
        """
        # Runs the parser.
        tree = self.parser.parse()

        # Adds all library functions.
        for name, func in LIBRARY_FUNCTIONS.items():
            self.scopes.insert(name, Function(func.type, func.args, BuiltinFunction(name)))

        # Visits the root node in the abstract syntax tree.
        self.visit(tree)

        # Throws an error if the main function isn't of type int.
        if self.scopes.get("main").type != TokenType.INT:
            self.error(ErrorCode.INVALID_MAIN, None)
        else:  # Otherwise runs the main function with no arguments.
            ret_val = self.visit(FunctionCall("main", []))
            return ret_val.value

    def visit(self, node: AST) -> Value:
        """
        Visits a node.
        Args:
            node (AST): node to visit.
        Returns:
            Value: the value returned from the node.
        """
        # Runs the corresponding function based on the type of node.
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Throws an error if the corresponding visit method does not exist"""
        raise Exception("No visit_{} method".format(type(node).__name__))

    def visit_UnaryOperator(self, node: UnaryOperator):
        """Visits a UnaryOperator node."""
        expr = self.visit(node.expression)
        value = expr.unary_operator(node.operator)

        # Throws an error if the operation does not exist for a variable type. Ex. -"abc".
        if value is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)

        return value()

    def visit_BinaryOperator(self, node: BinaryOperator):
        """Visits a BinaryOperator node."""
        left_child = self.visit(node.expr_left)
        right_child = self.visit(node.expr_right)

        value = left_child.binary_operator(node.operator, right_child)
        # Throws an error if the operation does not exist for the two variable types. Ex. 2 / "a".
        if value is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)

        return value()

    def visit_CastOperator(self, node: CastOperator):
        """Visits a CastOperator node."""
        expr = self.visit(node.expression)
        value = expr.cast_operator(node.operator)

        # Throws an error if the operation does not exist for a variable type.
        if value is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)

        return value()

    def visit_Val(self, node: Val):
        """Visits a Val node."""
        return build_value(node.type, node.value)

    def visit_ListVal(self, node: ListVal):
        """Visits a ListVal node."""
        l = []
        for expr in node.value:
            l.append(self.visit(expr))
        return build_value(TokenType.LISTL, l)

    def visit_ListRead(self, node: ListRead):
        """Visits a ListRead node."""
        index = self.visit(node.expr_index)
        list_obj = self.visit(node.obj)
        if index.type != TokenType.INTL:
            self.error(ErrorCode.MISMATCHED_TYPE, None)
        return list_obj.value[index.value]

    def visit_ListAssign(self, node: ListAssign):
        """Visits a ListAssign node."""
        indices = [self.visit(e) for e in node.expr_index]
        list_obj = self.visit(node.obj)
        expression = self.visit(node.expression)

        # Checks if all the indices to access are ints.
        if any(e.type != TokenType.INTL for e in indices):
            self.error(ErrorCode.MISMATCHED_TYPE, None)

        # Sets `curr` as the 1-D list if the whole list is multidimensional.
        curr = list_obj.value
        for i in range(len(indices) - 1):
            curr = curr[indices[i].value].value

        # Runs if node.operator is a simple assignment operator.
        if node.operator == TokenType.ASSIGN:
            # Set the variable to the new value.
            curr[indices[-1].value] = expression
        # Runs if node.operator is any other type of assignment operator. Ex. +=, -=...
        else:
            # Gets the variable and applies the operation.
            value = curr[indices[-1].value].assignment_operator(
                node.operator, expression)

            # Throws an error if the operation is not defined.
            if value is None:
                self.error(ErrorCode.MISMATCHED_TYPE, node.token)

            # Sets the variable to the new value.
            curr[indices.value] = value()

    def visit_Variable(self, node: Variable):
        """Visits a Variable node."""
        # Throw an error if the variable has not been declared.
        if node.value not in self.scopes:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)
        # Otherwise return the value of the variable.
        else:
            return self.scopes.get(node.value)

    def visit_DeclarationStatement(self, node: DeclarationStatement):
        """Visits a DeclarationStatement node."""
        val = self.visit(node.expression)

        # Throw an error if the variable has already been declared.
        if node.name.value in self.scopes.peek():
            self.error(ErrorCode.DUPLICATE_ID, node.name.token)

        # Add the variable into the current scope.
        self.scopes.insert(node.name.value, build_value(
            identifier_to_object(node.type), val.value))

    def visit_AssignmentStatement(self, node: AssignmentStatement):
        """Visits an AssignmentStatement node."""
        name = node.name.value
        val = self.visit(node.expression)

        # Throw an error if the variable has not been declared yet.
        if name not in self.scopes:
            self.error(ErrorCode.ID_NOT_FOUND, node.name.token)

        # Runs if node.operator is a simple assignment operator.
        if node.operator == TokenType.ASSIGN:
            # Set the variable to the new value.
            self.scopes.set(name, build_value(
                self.scopes.get(name).type, val.value))

        # Runs if node.operator is any other type of assignment operator. Ex. +=, -=...
        else:
            # Gets the variable and applies the operation.
            value = self.scopes.get(name).assignment_operator(node.operator, val)

            # Throws an error if the operation is not defined.
            if value is None:
                self.error(ErrorCode.MISMATCHED_TYPE, node.token)

            # Sets the variable to the new value.
            self.scopes.set(
                name, build_value(self.scopes.get(name).type, value().value))

    def visit_Block(self, node: Block):
        """Visits a Block node."""
        self.scopes.push()
        for child in node.children:
            self.visit(child)
        self.scopes.pop()

    def visit_IfElse(self, node: IfElse):
        """Visits an IfElse node."""

        # Visits all the if, and else if blocks until one of the conditions is satisfied.
        for e in node.conditional:
            if self.visit(e[0]).value:
                self.visit(e[1])
                return

        # Otherwise runs the final else block.
        if node.otherwise is not None:
            self.visit(node.otherwise)

    def visit_ForLoop(self, node: ForLoop):
        """Visits a ForLoop node."""
        self.scopes.push()

        # Runs the init statement.
        self.visit(node.init)

        # Loops until the condition is false.
        while self.visit(node.condition).value:
            try:  # Visits the looping block.
                self.visit(node.block)
            except BreakException:  # Breaks out of the loop.
                break
            except ContinueException:  # Continues the loop.
                pass

            # Runs the increment statement.
            self.visit(node.increment)
        self.scopes.pop()

    def visit_WhileLoop(self, node: WhileLoop):
        """Visits a WhileLoop node."""

        # Runs until the condition is false.
        while self.visit(node.condition).value:
            try:  # Visits the looping block.
                self.visit(node.block)
            except BreakException:  # Breaks out of the loop.
                break
            except ContinueException:  # Continues the loop.
                pass

    def visit_DoWhile(self, node: DoWhile) -> None:
        """Visits a DoWhile node."""

        # Runs the block first no matter what.
        try:  # Visits the looping block.
            self.visit(node.block)
        # Breaks out of the loop. In this case there is no loop so we return.
        except BreakException:
            return
        except ContinueException:  # Continues the loop.
            pass

        # Runs until the condition is false.
        while self.visit(node.condition).value:
            try:  # Visits the looping block.
                self.visit(node.block)
            except BreakException:  # Breaks out of the loop.
                break
            except ContinueException:  # Continues the loop.
                pass

    def visit_FunctionDeclaration(self, node: FunctionDeclaration) -> None:
        """Visits a FunctionDeclaration node."""

        # If the function has already been declared.
        if node.name.value in self.scopes.peek():
            self.error(ErrorCode.DUPLICATE_ID, node.name.token)

        # Otherwise add the function to the scope.
        self.scopes.insert(node.name.value, Function(
            node.type, node.args, node.body))

    # TODO: Change arrays
    # TODO: fix string escape characters
    # TODO: add default values to declaration statement
    # If statements without brackets

    def visit_FunctionCall(self, node: FunctionCall):
        """Visits a FunctionCall node."""

        # Throws an error if the function has not been defined.
        if node.name not in self.scopes:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)

        # Gets the function object.
        function = self.scopes.get(node.name)

        # Throws an error if the object is not a function.
        if not isinstance(function, value.Function):
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)

        # Determines the value for each function argument.
        ret = [self.visit(e) for e in node.args]

        # Temporarily stores the current scope.
        top = self.scopes.top

        """
        Creates a new scope from the bottom. Consequently, the code in the 
        function will not have access to variables defined elsewhere.
        """
        self.scopes.top = self.scopes.bottom
        self.scopes.push()

        # Throws an error if the arguments don't line up, otherwise, add them to the current scope.
        if len(function.args) != len(node.args):
            self.error(ErrorCode.MISMATCHED_ARGS, node.token)
        for i in range(len(function.args)):
            if object_to_identifier(ret[i].type) != function.args[i].type:
                self.error(ErrorCode.MISMATCHED_ARGS, node.token)
            self.scopes.insert(function.args[i].name.value, ret[i])

        # Declares return value of function, defaults to None.
        ret_val = None
        ret_token = None

        # Runs the function block.
        try:
            self.visit(function.block)
        # If there is an uncaught BreakException in the function, throw an error.
        except (BreakException, ContinueException) as ex:
            self.error(ErrorCode.BREAK_OR_CONTINUE_WITHOUT_LOOP, ex.token)
        # If a value has been returned, return set ret_val and ret_token to the returned values.
        except ReturnException as ex:
            ret_val = ex.value
            ret_token = ex.token

        # Resets the scope back to its state prior to running the function.
        self.scopes.pop()
        self.scopes.top = top

        # If the function type and the return type line up, return the return value.
        if (ret_val is None and function.type == TokenType.VOID) or \
                (ret_val is not None and object_to_identifier(ret_val.type) == function.type):
            return ret_val
        # Otherwise throw an error.
        else:
            self.error(ErrorCode.MISMATCHED_TYPE, ret_token)

    def visit_BuiltinFunction(self, node: BuiltinFunction):
        """Visits a BuiltinFunction node."""
        return LIBRARY_FUNCTIONS[node.name].run(self.scopes)

    def visit_BreakStatement(self, node: BreakStatement):
        """Visits a BreakStatement node."""
        raise BreakException(node.token)

    def visit_ContinueStatement(self, node: ContinueStatement):
        """Visits a ContinueStatement node."""
        raise ContinueException(node.token)

    def visit_ReturnStatement(self, node: ReturnStatement):
        """Visits a ReturnStatement node."""
        raise ReturnException(self.visit(node.expression), node.token)

    def visit_Program(self, node: Program):
        """Visits a Program node."""
        for function in node.functions:
            self.visit(function)

    def visit_NoOperation(self, node):
        """Visits a NoOperation node."""
        pass

    def error(self, error_code, token):
        """Throws an error and states the current character, line, and column on which the error happened"""
        raise InterpreterError(f"{error_code.value} -> {token}")
