from enum import Enum


class ErrorCode(Enum):
    UNEXPECTED_TOKEN = "Unexpected token"
    ID_NOT_FOUND = "Identifier not found"
    DUPLICATE_ID = "Duplicate id found"
    MISMATCHED_TYPE = "Mismatched type"
    MISMATCHED_ARGS = "Mismatched arguments"
    BREAK_OR_CONTINUE_WITHOUT_LOOP = "Break or continue without loop"


class LexerError(Exception):
    pass


class ParserError(Exception):
    pass


class SemanticError(Exception):
    pass


class FileError(Exception):
    pass


class BreakException(Exception):
    def __init__(self, token):
        self.token = token


class ContinueException(Exception):
    def __init__(self, token):
        self.token = token


class ReturnException(Exception):
    def __init__(self, value, token=None):
        self.value = value
        self.token = token
