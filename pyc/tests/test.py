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

    def test_int(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_int.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_int.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_int.out",
            0)

    def test_float(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_float.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_float.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_float.out",
            0)

    def test_string(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_string.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_string.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_string.out",
            0)

    def test_if_statements(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_if_statements.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_if_statements.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_if_statements.out",
            0)

    def test_for_loops(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_for_loops.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_for_loops.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_for_loops.out",
            0)

    def test_while_loops(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_while_loops.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_while_loops.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_while_loops.out",
            0)

    def test_functions(self):
        self.feed_input_and_output_file(
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_functions.pysc",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_functions.in",
            "C:\\Users\\paulc\\Code\\pyc\\pyc\\tests\\test_files\\test_functions.out",
            0)


if __name__ == '__main__':
    unittest.main()
