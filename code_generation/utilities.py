import re


def to_valid_variable_name(input_string: str) -> str:
    cleaned_string = re.sub(r'[^0-9a-zA-Z_]', '_', input_string)
    if not cleaned_string[0].isalpha() and cleaned_string[0] != '_':
        cleaned_string = f'_{cleaned_string}'
    return cleaned_string