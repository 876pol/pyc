"""
ICS3U
Paul Chen
This file is the main entry point into the program.
"""

import sys

from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


# Main function
def main():
    # Check if the user provided a source file.
    if len(sys.argv) <= 1:
        raise FileNotFoundError("No source file provided")
    
    if sys.argv[1] == "-c":
        # Pulls source code from command line argument.
        if len(sys.argv) <= 2:
            raise FileNotFoundError("No code provided")
        code = sys.argv[2]
    else:
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
