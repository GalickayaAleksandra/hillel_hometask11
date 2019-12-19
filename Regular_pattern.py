import re


def pattern_dates(text):
    pattern = '\d{2}-\d{2}-\d{4}'
    full_dates = re.findall(pattern, text)
    return full_dates


def pattern_float_numbers(text):
    pattern = '^\d*\.\d+$'
    numbers = re.findall(pattern, text)
    return numbers
