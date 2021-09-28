import re


def reformat_name(name):
    return name.replace('-', ' ')


def snake_to_camel(string):
    spl = string.split('_')
    return ''.join([spl[0]] + [word.title() for word in spl[1:]])


def camel_to_snake(s: str):
    spl = re.sub(r'([A-Z])', r'_\1', s)
    return spl.lower()


def reformat_keys(d, f=snake_to_camel):
    reformatted_d = {}
    if isinstance(d, dict):
        for k, v in d.items():
            replace_val = None
            if isinstance(v, dict):
                replace_val = reformat_keys(v)
            elif isinstance(v, list):
                replace_val = [reformat_keys(v2) for v2 in v]
            else:
                replace_val = v
            reformatted_d[f(k)] = replace_val
        return reformatted_d
    else:
        return d


def camel_case_keys(d_snake):
    return reformat_keys(d_snake, snake_to_camel)


def snake_case_keys(d_camel):
    return reformat_keys(d_camel, camel_to_snake)