import yaml

def load_config(path):
    with open(path, 'r') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)

