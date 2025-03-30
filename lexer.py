from typing import TypeAlias
c = __import__("constants.py")

StringType: TypeAlias = str | None
NumberType: TypeAlias = int | float | None
BooleanType: TypeAlias = bool | None
Token: TypeAlias = StringType | NumberType | BooleanType

def lex_string(input_string: str) -> tuple[StringType, str]:
    json_string = ''
    if input_string[0] == c.JSON_QUOTE:
        input_string = input_string[1:]
    else:
        return None, input_string

    for char in input_string:
        if char == c.JSON_QUOTE:
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

    if string_len >= c.TRUE_LEN and input_string[:c.TRUE_LEN] == 'true':
        return True, input_string[c.TRUE_LEN:]
    elif string_len >= c.FALSE_LEN and input_string[:c.FALSE_LEN] == 'false':
        return False, input_string[c.FALSE_LEN:]

    return None, input_string

def lex_null(input_string: str) -> tuple[BooleanType, str]:
    string_len = len(input_string)
    if string_len >= c.NULL_LEN and input_string[:c.NULL_LEN] == 'null':
        return True, input_string[c.NULL_LEN:]

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
        json_string, string = lex_string(input_json)
        if json_string is not None:
            tokens.append(json_string)
            continue

        # 2. Check for number
        json_number, string = lex_number(input_json)
        if json_number is not None:
            tokens.append(json_number)
            continue

        # 3. Check for boolean
        json_bool, string = lex_bool(input_json)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        # 4. Check for null
        json_null, string = lex_null(input_json)
        if json_null is not None:
            tokens.append(None)
            continue

        if string[0] in c.JSON_WHITESPACE:
            string = string[1:]
        elif string[0] in c.JSON_SYNTAX:
            tokens.append(string[0])
            string = string[1:]
        else:
            raise Exception("Unexpected character: {}".format(string[0]))

    return tokens
