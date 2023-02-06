"""
ICS3U
Paul Chen
This file holds the `Interpreter` class that runs an abstract syntax tree.
"""
from typing import Optional, Callable, Union, List

from ast_nodes import NoOperationStatementNode, BuiltInFunctionCallStatementNode, ASTNode, FunctionCallStatementNode, \
    UnaryOperatorNode, BinaryOperatorNode, CastOperatorNode, ValueLiteralNode, InitializerListLiteralNode, \
    VariableNode, DeclarationStatementNode, AssignmentStatementNode, BlockStatementNode, IfElseStatementNode, \
    ForLoopNode, WhileLoopNode, DoWhileLoopNode, FunctionDeclarationStatementNode, BreakStatementNode, \
    ContinueStatementNode, ReturnStatementNode, ProgramNode
from control_exceptions import BreakException, ContinueException, ReturnException
from error import ErrorCode, InterpreterError
from lexer import TokenType
from library import LIBRARY_FUNCTIONS
from linked_dict import LinkedDict
from parser import Parser
from value import build_value, object_to_identifier, Function, identifier_to_object, Value, InitializerListValue, \
    NullValue


class Interpreter(object):
    """
    Interpreter class that reads an abstract syntax tree and runs the program.

    Attributes:
        parser (Parser): the parser that converts tokens into an abstract syntax tree.
        stack (LinkedDict): data structure that holds all variables in all scopes.
    """

    def __init__(self, parser: Parser) -> None:
        """
        Inits interpreter class.
        Args:
            parser (Parser): the parser.
        """
        self.parser = parser
        self.stack = LinkedDict()

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
            self.stack.insert(name, Function(func.type, func.args, BuiltInFunctionCallStatementNode(name)))

        # Visits the root node in the abstract syntax tree.
        self.visit(tree)

        # Throws an error if the main function isn't of type int.
        if self.stack.get("main").type != TokenType.INT:
            self.error(ErrorCode.INVALID_MAIN, None)
        else:  # Otherwise runs the main function with no arguments.
            ret_val = self.visit(FunctionCallStatementNode("main", []))
            return ret_val.value

    def visit(self, node: ASTNode) -> Optional[Value]:
        """
        Visits a node.
        Args:
            node (ASTNode): node to visit.
        Returns:
            Value: the name returned from the node.
        """
        # Runs the corresponding function based on the type of node.
        method_name = "visit_" + type(node).__name__
        visitor: Callable[[ASTNode], Optional[Value]] = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Throws an error if the corresponding visit method does not exist."""
        raise Exception("No visit_{} method".format(type(node).__name__))

    def visit_ValueLiteralNode(self, node: ValueLiteralNode) -> Value:
        """Visits a ValueLiteralNode."""
        return build_value(node.type, node.value)

    def visit_InitializerListLiteralNode(self, node: InitializerListLiteralNode) -> InitializerListValue:
        """Visits an InitializerListLiteralNode."""
        list_elements = [self.visit(expr) for expr in node.value]
        return build_value(TokenType.ARRAYL, list_elements)

    def determine_array_subscript_indices(self, indices: List[ASTNode]) -> Optional[List[Optional[int]]]:
        """
        Determines the subscript indices of a variable. Essentially converts a List[ASTNode] to a List[Optional[int]],
        returning None if the list is invalid. The returned list may contain a NullValue in the case that the code
        contains an empty array subscript operator (ex. int a[] = {1, 2, 3};).
        """
        ret_indices = []
        for i in range(len(indices)):
            index_object = self.visit(indices[i])

            # Index must be an IntValue or a NullValue.
            if index_object.type not in (TokenType.INTL, TokenType.VOIDL):
                return None

            # Appends the index to the list.
            ret_indices.append(index_object.value)
        return ret_indices

    def visit_VariableNode(self, node: VariableNode) -> Value:
        """Visits a VariableNode."""

        # If the variable does not exist, throw an error.
        if node.name not in self.stack:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)

        # If there are no indices to access, return it directly.
        if len(node.indices) == 0:
            return self.stack.get(node.name)

        # Determines the indices of the array to access.
        indices = self.determine_array_subscript_indices(node.indices)
        if indices is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)

        # Obtains the variable from the stack.
        obj = self.stack.get(node.name)

        for i in range(len(indices)):
            # If the object is not an array, or the index is out of bounds, raise an error.
            if obj.type != TokenType.ARRAYL:
                self.error(ErrorCode.MISMATCHED_TYPE, node.token)
            if indices[i] not in range(0, len(obj.value)):
                self.error(ErrorCode.OUT_OF_BOUNDS, node.token)

            # Continue to the next dimension of the array.
            obj = obj.value[indices[i]]

        return obj

    def visit_UnaryOperatorNode(self, node: UnaryOperatorNode) -> Value:
        """Visits a UnaryOperatorNode."""
        expr = self.visit(node.operand)
        value = expr.unary_operator(node.operator)

        # Throws an error if the operation does not exist for a variable type. Ex. -"abc".
        if value is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)

        return value()

    def visit_BinaryOperatorNode(self, node: BinaryOperatorNode) -> Value:
        """Visits a BinaryOperatorNode."""
        left_child = self.visit(node.left_operand)
        right_child = self.visit(node.right_operand)

        value = left_child.binary_operator(node.operator, right_child)
        # Throws an error if the operation does not exist for the two variable types. Ex. 2 / "a".
        if value is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)

        return value()

    def visit_CastOperatorNode(self, node: CastOperatorNode) -> Value:
        """Visits a CastOperatorNode."""
        expr = self.visit(node.operand)
        value = expr.cast_operator(node.operator)

        # Throws an error if the operation does not exist for a variable type.
        if value is None:
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)

        return value()

    def visit_DeclarationStatementNode(self, node: DeclarationStatementNode) -> None:
        # `expression = NullType(TokenType.VOIDL, None)` if no expression is provided (ex. int a[5][5];).
        expression = self.visit(node.expression)

        # Verifies that the variable doesn't already exist.
        if node.variable.name in self.stack.peek():
            self.error(ErrorCode.DUPLICATE_ID, node.variable.token)

        if len(node.variable.indices) == 0:  # If the variable is not an array.
            try:
                self.stack.insert(node.variable.name, build_value(identifier_to_object(node.type), expression.value))
            except ValueError:
                self.error(ErrorCode.MISMATCHED_TYPE, node.variable.token)
        else:  # If the variable is an array.

            # Verifies that the dimensions are valid.
            dimensions = self.determine_array_subscript_indices(node.variable.indices)
            if dimensions is None:
                self.error(ErrorCode.MISMATCHED_TYPE, node.variable.token)
            if any(d is not None and d <= 0 for d in dimensions):
                self.error(ErrorCode.OUT_OF_BOUNDS, node.variable.token)

            def create_multidim_array(index: int = 0) -> Union[List, Value]:
                """Creates a multidimensional array"""
                if index == len(dimensions):
                    return build_value(identifier_to_object(node.type))
                return build_value(TokenType.ARRAYL,
                                   [create_multidim_array(index + 1) for _ in range(dimensions[index])])

            def verify_initializer_list(curr_list: Union[List, Value], index: int = 0) -> bool:
                """
                Verifies that the number of dimensions in the initializer list matches the number given in the
                declaration. Also verifies that all the arrays in the same dimension are the same size.
                """
                if index == len(dimensions):
                    return curr_list.type == identifier_to_object(node.type)
                if curr_list.type == TokenType.ARRAYL and dimensions[index] is None:
                    dimensions[index] = len(curr_list.value)
                return curr_list.type == TokenType.ARRAYL and len(curr_list.value) == dimensions[index] and \
                    all(verify_initializer_list(curr_list.value[j], index + 1) for j in range(dimensions[index]))

            # If no initializer list has been provided.
            if expression.value is None:

                self.stack.insert(node.variable.name, create_multidim_array())
            # If an initializer list has been provided.
            else:

                if verify_initializer_list(expression):
                    self.stack.insert(node.variable.name, expression)
                else:
                    self.error(ErrorCode.MISMATCHED_TYPE, node.variable.token)

    def visit_AssignmentStatementNode(self, node: AssignmentStatementNode) -> None:
        """Visits an AssignmentStatementNode."""
        name = node.variable.name
        val = self.visit(node.expression)

        # Throw an error if the variable has not been declared yet.
        if name not in self.stack:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)

        if len(node.variable.indices) == 0:  # If the variable is not an array.
            # Cannot assign a value to an array.
            if self.stack.get(name).type == TokenType.ARRAYL:
                self.error(ErrorCode.MISMATCHED_TYPE, node.variable.token)

            # Runs if node.operator is a simple assignment operator.
            if node.operator == TokenType.ASSIGN:
                # Set the variable to the new name.
                try:
                    self.stack.set(name, build_value(self.stack.get(name).type, val.value))
                except ValueError:
                    self.error(ErrorCode.MISMATCHED_TYPE, node.variable.token)

            # Runs if node.operator is any other type of assignment operator. Ex. +=, -=...
            else:
                # Gets the variable and applies the operation.
                value = self.stack.get(name).assignment_operator(node.operator, val)

                # Throws an error if the operation is not defined.
                if value is None:
                    self.error(ErrorCode.MISMATCHED_TYPE, node.token)

                # Sets the variable to the new name.
                try:
                    self.stack.set(name, build_value(self.stack.get(name).type, value().value))
                except ValueError:
                    self.error(ErrorCode.MISMATCHED_TYPE, node.variable.token)
        else:  # If the variable is an array.
            # Verifies that the dimensions are valid.
            indices = self.determine_array_subscript_indices(node.variable.indices)
            if indices is None:
                self.error(ErrorCode.MISMATCHED_TYPE, node.token)
            if any(d is None for d in indices):
                self.error(ErrorCode.OUT_OF_BOUNDS, node.token)

            # Current value held in the program.
            curr = self.stack.get(name)
            for i in range(len(indices) - 1):
                # If the object is not an array, or the index is out of bounds, raise an error.
                if curr.type != TokenType.ARRAYL:
                    self.error(ErrorCode.MISMATCHED_TYPE, node.token)
                if indices[i] not in range(0, len(curr.value)):
                    self.error(ErrorCode.OUT_OF_BOUNDS, node.token)

                curr = curr.value[indices[i]]

            # `curr` should be a list that directly holds the element to be modified, as `curr` is an object reference.

            # If `curr` is not an array of non-array objects, or the index is out of bounds, raise an error.
            if curr.type != TokenType.ARRAYL or curr.value[indices[-1]].type == TokenType.ARRAYL:
                self.error(ErrorCode.MISMATCHED_TYPE, node.token)
            if indices[-1] not in range(0, len(curr.value)):
                self.error(ErrorCode.OUT_OF_BOUNDS, node.token)

            # Runs if node.operator is a simple assignment operator.
            if node.operator == TokenType.ASSIGN:
                # Set the variable to the new value.
                try:
                    curr.value[indices[-1]] = build_value(curr.value[indices[-1]].type, val.value)
                except ValueError:
                    self.error(ErrorCode.MISMATCHED_TYPE, node.variable.token)

            # Runs if node.operator is any other type of assignment operator. Ex. +=, -=...
            else:
                # Gets the variable and applies the operation.
                value = curr.value[indices[-1]].assignment_operator(node.operator, val)

                # Throws an error if the operation is not defined.
                if value is None:
                    self.error(ErrorCode.MISMATCHED_TYPE, node.token)

                # Sets the variable to the new name.
                try:
                    curr.value[indices[-1]] = build_value(curr.value[indices[-1]].type, value().value)
                except ValueError:
                    self.error(ErrorCode.MISMATCHED_TYPE, node.variable.token)

    def visit_BlockStatementNode(self, node: BlockStatementNode) -> None:
        """Visits a BlockStatementNode."""
        self.stack.push()
        for statement in node.statements:
            self.visit(statement)
        self.stack.pop()

    def visit_IfElseStatementNode(self, node: IfElseStatementNode) -> None:
        """Visits an IfElseStatementNode."""

        # Visits all the if, and else-if blocks until one of the conditions is satisfied.
        for e in node.conditional:
            if self.visit(e[0]).value:
                self.visit(e[1])
                return

        # Otherwise runs the final else block.
        if node.otherwise is not None:
            self.visit(node.otherwise)

    def visit_ForLoopNode(self, node: ForLoopNode) -> None:
        """Visits a ForLoopNode."""
        self.stack.push()

        # Runs the initialization statement.
        self.visit(node.initialization)

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
        self.stack.pop()

    def visit_WhileLoopNode(self, node: WhileLoopNode) -> None:
        """Visits a WhileLoopNode."""

        # Runs until the condition is False.
        while self.visit(node.condition).value:
            try:  # Visits the looping block.
                self.visit(node.block)
            except BreakException:  # Breaks out of the loop.
                break
            except ContinueException:  # Continues the loop.
                pass

    def visit_DoWhileLoopNode(self, node: DoWhileLoopNode) -> None:
        """Visits a DoWhileLoopNode node."""

        # Runs the block first no matter what.
        try:  # Visits the looping block.
            self.visit(node.block)
        # Breaks out of the loop. In this case there is no loop, so we return.
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

    def visit_BreakStatementNode(self, node: BreakStatementNode):
        """Visits a BreakStatementNode."""
        raise BreakException(node.token)

    def visit_ContinueStatementNode(self, node: ContinueStatementNode):
        """Visits a ContinueStatementNode."""
        raise ContinueException(node.token)

    def visit_ReturnStatementNode(self, node: ReturnStatementNode):
        """Visits a ReturnStatementNode."""
        raise ReturnException(self.visit(node.expression), node.token)

    def visit_FunctionDeclarationStatementNode(self, node: FunctionDeclarationStatementNode) -> None:
        """Visits a FunctionDeclarationStatementNode."""

        # If the function has already been declared.
        if node.variable.name in self.stack.peek():
            self.error(ErrorCode.DUPLICATE_ID, node.variable.token)

        # If the function attempts to return an array.
        if len(node.variable.indices) != 0:
            self.error(ErrorCode.ARRAY_AS_FUNCTION_RETURN, node.variable.token)

        # Otherwise add the function to the scope.
        self.stack.insert(node.variable.name, Function(node.type, node.args, node.body))

    def visit_FunctionCallStatementNode(self, node: FunctionCallStatementNode) -> Optional[Value]:
        """Visits a FunctionCallStatementNode node."""

        # Throws an error if the function has not been defined.
        if node.name not in self.stack:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)

        # Gets the function object.
        function = self.stack.get(node.name)

        # Throws an error if the object is not a function.
        if not isinstance(function, Function):
            self.error(ErrorCode.MISMATCHED_TYPE, node.token)

        # Determines the name for each function argument.
        ret = [self.visit(e) for e in node.args]

        # Temporarily stores the current scope.
        top = self.stack.top

        """
        Creates a new scope from the bottom. Consequently, the code in the 
        function will not have access to variables defined elsewhere.
        """
        self.stack.top = self.stack.bottom
        self.stack.push()

        # Throws an error if the arguments don't line up, otherwise, add them to the current scope.
        if len(function.args) != len(node.args):
            self.error(ErrorCode.MISMATCHED_ARGS, node.token)
        for i in range(len(function.args)):
            # If the argument is an array, verify that the number of array dimensions is valid,
            # and that the type is valid.
            if ret[i].type == TokenType.ARRAYL:
                curr = ret[i]
                for j in range(function.args[i].num_dimensions):
                    if curr.type != TokenType.ARRAYL:
                        self.error(ErrorCode.MISMATCHED_ARGS, node.token)
                    curr = curr.value[j]
                if object_to_identifier(curr.type) != function.args[i].type:
                    self.error(ErrorCode.MISMATCHED_ARGS, node.token)

            # Otherwise, only verify that the type is valid.
            elif object_to_identifier(ret[i].type) != function.args[i].type:
                self.error(ErrorCode.MISMATCHED_ARGS, node.token)

            self.stack.insert(function.args[i].name, ret[i])

        # Declares return name of function, defaults to None.
        ret_val = build_value(TokenType.VOIDL)
        ret_token = None

        # Runs the function block.
        try:
            self.visit(function.block)
        # If there is an uncaught BreakException in the function, throw an error.
        except (BreakException, ContinueException) as ex:
            self.error(ErrorCode.BREAK_OR_CONTINUE_WITHOUT_LOOP, ex.token)
        # If a name has been returned, return set ret_val and ret_token to the returned values.
        except ReturnException as ex:
            ret_val = ex.value
            ret_token = ex.token

        # Resets the scope back to its state prior to running the function.
        self.stack.pop()
        self.stack.top = top

        # If the function type and the return type line up, return the return name.
        if (ret_val.type == TokenType.VOIDL and function.type == TokenType.VOID) or \
                (ret_val.type != TokenType.VOIDL and object_to_identifier(ret_val.type) == function.type):
            return ret_val
        # Otherwise throw an error.
        else:
            self.error(ErrorCode.MISMATCHED_TYPE, ret_token)

    def visit_BuiltInFunctionCallStatementNode(self, node: BuiltInFunctionCallStatementNode) -> None:
        """Visits a BuiltInFunctionCallStatementNode."""
        return LIBRARY_FUNCTIONS[node.name].run(self.stack)

    def visit_ProgramNode(self, node: ProgramNode) -> None:
        """Visits a ProgramNode."""
        for function in node.functions:
            self.visit(function)

    def visit_NoOperationStatementNode(self, node: NoOperationStatementNode) -> NullValue:
        """Visits a NoOperationStatementNode."""
        return build_value(TokenType.VOIDL)

    def error(self, error_code, token):
        """Throws an error and states the current character, line, and column on which the error happened"""
        raise InterpreterError(f"{error_code.value} -> {token}")
