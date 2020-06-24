import logging
import yaml
import os
import re


HAS_PLACEHOLDER = re.compile(r'{{([\s]*[a-zA-Z0-9_-]+[\s]*)}}')
INNER_STRING = re.compile(r'[a-zA-Z0-9_-]+')


def load_config(path):
    with open(path, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        logging.debug("Original config: {}".format(config))
        if type(config) == dict:
            config = parse_dict(config)
        elif type(config) == list:
            config = parse_list(config)
        elif type(config) == str:
            config = replace_with_env_var(config)
        logging.debug("Replaced config: {}".format(config))
        return config


def parse_dict(dic):
    ret = {}
    for key, value in dic.items():
        if type(value) == dict:
            ret[key] = parse_dict(value)
        elif type(value) == list:
            ret[key] = parse_list(value)
        elif type(value) == str:
            ret[key] = replace_with_env_var(value)
        else:
            ret[key] = value
    return ret


def parse_list(lis):
    ret = []
    for value in lis:
        if type(value) == dict:
            ret.append(parse_dict(value))
        elif type(value) == list:
            ret.append(parse_list(value))
        elif type(value) == str:
            ret.append(replace_with_env_var(value))
        else:
            ret.append(value)
    return ret


def replace_with_env_var(value):
    matched = re.match(HAS_PLACEHOLDER, value)
    if matched:
        r = re.search(INNER_STRING, value)
        env_var = r.group()
        return os.environ.get(env_var)
    return value
