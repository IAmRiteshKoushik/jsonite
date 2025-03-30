from lexer import lex
from constants import *

from typing import TypeAlias

ParsedType: TypeAlias = dict | list

def parse_array(tokens: list) -> tuple[list, list]:
    json_array = []

    t = tokens[0]
    if t == JSON_RIGHTBRACKET:
        return json_array, tokens[1:]

    while True:
        json, tokens = parse(tokens)
        json_array.append(json)

        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after object in array')
        else:
            tokens = tokens[1:]

    raise Exception('Expected end-of-array bracket')

def parse_object(tokens: list) -> tuple[dict, list]:
    json_object = {}

    t = tokens[0]
    if t == JSON_RIGHTBRACE:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]
        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception('Expected string key, got: {}'.format(json_key))

        if tokens[0] != JSON_COLON:
            raise Exception('Expected color after key in object, got: {}'.format(t))

        json_value, tokens = parse(tokens[1:])
        json_object[json_key] = json_value

        t = tokens[0]
        if t == JSON_RIGHTBRACE:
            return json_object, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception('Expected comma after pair in object, got: {}'.format(t))

        tokens = tokens[1:]

    raise Exception('Expected end-of-object brace')

def parse(tokens, is_root = False) -> tuple[ParsedType, list]:
    t = tokens[0]

    if is_root and t != JSON_LEFTBRACE:
        raise Exception('Root must be an object')
    if t == JSON_LEFTBRACKET:
        return parse_array(tokens[1:])
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:])
    else:
        return t, tokens[1:]


# Unifying interface
def from_string(json_str: str) -> ParsedType:
    tokens = lex(json_str)
    return parse(tokens, is_root = True)[0]
