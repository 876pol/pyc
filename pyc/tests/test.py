import io
import sys
import unittest

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


class TestInterpreter(unittest.TestCase):
    def feed_input_and_output_file(self, code_file, input_file, output_file, exit_code):
        code = open(code_file, "r")
        program_input = open(input_file, "r")
        expected_output = open(output_file, "r")

        sys.stdin = io.StringIO(program_input.read())
        sys.stdout = io.StringIO()
        lexer = Lexer(code.read())
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()

        self.assertEqual(sys.stdout.getvalue(), expected_output.read())
        self.assertEqual(result, exit_code)

        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        code.close()
        program_input.close()
        expected_output.close()

    def test_io(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_io.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_io.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_io.out",
            0)

    def test_variables_expressions(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_variables_expressions.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_variables_expressions.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_variables_expressions.out",
            0)

    def test_control_structures(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_control_structures.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_control_structures.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_control_structures.out",
            0)

    def test_functions(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_functions.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_functions.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_functions.out",
            0)


if __name__ == '__main__':
    unittest.main()

