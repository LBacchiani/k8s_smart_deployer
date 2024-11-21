import re


def to_valid_variable_name(input_string: str) -> str:
    cleaned_string = re.sub(r'[^0-9a-zA-Z_]', '_', input_string)
    if not cleaned_string[0].isalpha() and cleaned_string[0] != '_':
        cleaned_string = f'_{cleaned_string}'
    return cleaned_string

def to_dns_name(image_name: str) -> str:
    transformed_name = re.sub(r'[^a-zA-Z0-9]+', '-', image_name)
    transformed_name = transformed_name.strip('-')
    transformed_name = transformed_name.lower()
    return transformed_name
