from sys import stderr

def error(message: str):
    print(message, file=stderr)
    raise Exception("here") # for debugging
    exit(1)
