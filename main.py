from os import listdir, getcwd
from sys import argv
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from error import FileError

# Main function
def main():
    # Check if the user provided a source file.
    if len(argv) <= 1:
        FileError("Error: No source file provided")
        return

    # Check if the provided source files exists.
    cwd = getcwd()
    dir_files = listdir(cwd)
    if argv[1] not in dir_files:
        FileError("Error: No source file found")
        return

    # Read the source code into a variable.
    file = open(argv[1], "r")
    code = file.read()

    # Starts the interpreter.
    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()


if __name__ == "__main__":
    main()
