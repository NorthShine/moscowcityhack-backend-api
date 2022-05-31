import yaml


def get_config():
    with open('config.yml', 'r') as config_file:
        return yaml.safe_load(config_file)
