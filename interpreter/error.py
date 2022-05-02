from enum import Enum


class ErrorCode(Enum):
    UNEXPECTED_TOKEN = "Unexpected token"
    ID_NOT_FOUND = "Identifier not found"
    DUPLICATE_ID = "Duplicate id found"
    MISMATCHED_TYPE = "Mismatched type"


class LexerError(Exception):
    pass


class ParserError(Exception):
    pass


class SemanticError(Exception):
    pass


class FileError(Exception):
    pass
