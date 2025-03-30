from typing import TypeAlias
from constants import *

StringType: TypeAlias = str | None
NumberType: TypeAlias = int | float | None
BooleanType: TypeAlias = bool | None
Token: TypeAlias = StringType | NumberType | BooleanType

def lex_string(input_string: str) -> tuple[StringType, str]:
    json_string = ''
    if input_string[0] == JSON_QUOTE:
        input_string = input_string[1:]
    else:
        return None, input_string

    for char in input_string:
        if char == JSON_QUOTE:
            return json_string, input_string[len(json_string) + 1:]
        else:
            json_string += char

    raise Exception("Expected end-of-string quote")

def lex_number(input_string: str) -> tuple[NumberType, str]:
    json_number = ''
    number_chars = [str(d) for d in range(0, 10)] + ['.']

    for char in input_string:
        if char in number_chars:
            json_number += char
        else:
            break

    rest = input_string[len(json_number):]

    # If there is no number
    if not len(json_number):
        return None, input_string

    # If there is a decimal point
    if '.' in json_number:
        return float(json_number), rest

    return int(json_number), rest

def lex_bool(input_string: str) -> tuple[BooleanType, str]:
    string_len = len(input_string)

    if string_len >= TRUE_LEN and input_string[:TRUE_LEN] == 'true':
        return True, input_string[TRUE_LEN:]
    elif string_len >= FALSE_LEN and input_string[:FALSE_LEN] == 'false':
        return False, input_string[FALSE_LEN:]

    return None, input_string

def lex_null(input_string: str) -> tuple[BooleanType, str]:
    string_len = len(input_string)
    if string_len >= NULL_LEN and input_string[:NULL_LEN] == 'null':
        return True, input_string[NULL_LEN:]

    return None, input_string

def lex(input_json: str) -> list[Token]:
    """
    Lexical analyzer that tokenized a JSON-like string into a list of tokens.
    Args:
        input_json (str): The input string to be tokenized
    Returns:
        list[Token]: A list of tokens extracted from the input string
    Raises:
        Exception: If an unexpected character is encountered
    """

    tokens: list[Token] = []
    while len(input_json):

        # 1. Check for string
        json_string, input_json = lex_string(input_json)
        if json_string is not None:
            tokens.append(json_string)
            continue

        # 2. Check for number
        json_number, input_json = lex_number(input_json)
        if json_number is not None:
            tokens.append(json_number)
            continue

        # 3. Check for boolean
        json_bool, input_json = lex_bool(input_json)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        # 4. Check for null
        json_null, input_json = lex_null(input_json)
        if json_null is not None:
            tokens.append(None)
            continue

        if input_json[0] in JSON_WHITESPACE:
            input_json = input_json[1:]
        elif input_json[0] in JSON_SYNTAX:
            tokens.append(input_json[0])
            input_json = input_json[1:]
        else:
            raise Exception("Unexpected character: {}".format(input_json[0]))

    return tokens
