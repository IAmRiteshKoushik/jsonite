from typing import TypeAlias
c = __import__("constants.py")

Token: TypeAlias = str | None

def lex_string(input_string: str) -> tuple[None, str]:
    return None, input_string 

def lex_number(input_string: str) -> tuple[None, str]:
    return None, input_string 

def lex_bool(input_string: str) -> tuple[None, str]:
    return None, input_string 

def lex_null(input_string: str) -> tuple[None, str]:
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

        # 4. 
            
        if string[0] in c.JSON_WHITESPACE:
            string = string[1:]
        elif string[0] in c.JSON_SYNTAX:
            tokens.append(string[0])
            string = string[1:]
        else:
            raise Exception("Unexpected character: {}".format(string[0]))

    return tokens
