from interpreter import Interpreter
from os import listdir, getcwd
from sys import argv
from lexer import Lexer
from parser import Parser


def main():
    cwd = getcwd()
    dir_files = listdir(cwd)
    if len(argv) <= 1:
        print("Error: No source file provided")
        return
    if argv[1] not in dir_files:
        print("Error: No source file found")
        return
    file = open(argv[1], "r")
    code = file.read()
    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(result)


if __name__ == "__main__":
    main()
