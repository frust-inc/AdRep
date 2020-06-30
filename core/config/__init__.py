import yaml
import os
import re

HAS_PLACEHOLDER = re.compile(r'{{([\s]*(SECRET|ENV)[:][a-zA-Z0-9_-]+[\s]*)}}')
INNER_STRING = re.compile(r'(SECRET|ENV)[:][a-zA-Z0-9_-]+')


class ConfigLoader():
    def __init__(self, path, secret_manager=None):
        self.path = path
        self.secret_manager = secret_manager

    def load(self):
        with open(self.path, 'r') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
            return self._parse_and_replace(config)

    def _parse_and_replace(self, config):
        if isinstance(config, dict):
            config = self._parse_dict(config)
        elif isinstance(config, list):
            config = self._parse_list(config)
        elif isinstance(config, str):
            config = self._replace_str(config)
        return config

    def _parse_dict(self, dic):
        ret = {}
        for key, value in dic.items():
            if isinstance(value, dict):
                ret[key] = self._parse_dict(value)
            elif isinstance(value, list):
                ret[key] = self._parse_list(value)
            elif isinstance(value, str):
                ret[key] = self._replace_str(value)
            else:
                ret[key] = value
        return ret

    def _parse_list(self, lis):
        ret = []
        for value in lis:
            if isinstance(value, dict):
                ret.append(self._parse_dict(value))
            elif isinstance(value, list):
                ret.append(self._parse_list(value))
            elif isinstance(value, str):
                ret.append(self._replace_str(value))
            else:
                ret.append(value)
        return ret

    def _replace_str(self, value):
        matched = re.match(HAS_PLACEHOLDER, value)
        if matched:
            r = re.search(INNER_STRING, value)
            group = r.group()
            var_type, var = group.split(":")
            if var_type == "SECRET":
                if not self.secret_manager:
                    raise Exception(
                        "secret manager must be configured if you specify SECRET type in config."
                    )
                return self.secret_manager.get(var)
            elif var_type == "ENV":
                return os.environ.get(var)
        return value
