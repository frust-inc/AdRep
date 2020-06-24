import yaml
import os
import re

HAS_PLACEHOLDER = re.compile(r'{{([\s]*[a-zA-Z0-9_-]+[\s]*)}}')
INNER_STRING = re.compile(r'[a-zA-Z0-9_-]+')


def load_config(path):
    with open(path, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        return _parse_and_replace(config)


def _parse_and_replace(config):
    if isinstance(config, dict):
        config = _parse_dict(config)
    elif isinstance(config, list):
        config = _parse_list(config)
    elif isinstance(config, str):
        config = _replace_with_env_var(config)
    return config


def _parse_dict(dic):
    ret = {}
    for key, value in dic.items():
        if isinstance(value, dict):
            ret[key] = _parse_dict(value)
        elif isinstance(value, list):
            ret[key] = _parse_list(value)
        elif isinstance(value, str):
            ret[key] = _replace_with_env_var(value)
        else:
            ret[key] = value
    return ret


def _parse_list(lis):
    ret = []
    for value in lis:
        if isinstance(value, dict):
            ret.append(_parse_dict(value))
        elif isinstance(value, list):
            ret.append(_parse_list(value))
        elif isinstance(value, str):
            ret.append(_replace_with_env_var(value))
        else:
            ret.append(value)
    return ret


def _replace_with_env_var(value):
    matched = re.match(HAS_PLACEHOLDER, value)
    if matched:
        r = re.search(INNER_STRING, value)
        env_var = r.group()
        return os.environ.get(env_var)
    return value
