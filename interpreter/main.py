import os
import sys

from error import FileError
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


# Main function
def main():
    # Check if the user provided a source file.
    if len(sys.argv) <= 1:
        raise FileError("No source file provided")

    # Check if the provided source files exists.
    cwd = os.getcwd()
    dir_files = os.listdir(cwd)
    if sys.argv[1] not in dir_files:
        raise FileError("No source file found")

    # Read the source code into a variable.
    file = open(sys.argv[1], "r")
    code = file.read()

    # Starts the interpreter.
    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    exit_code = interpreter.interpret()
    exit(exit_code)


if __name__ == "__main__":
    main()
