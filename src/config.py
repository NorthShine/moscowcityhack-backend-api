"""
Load sensitive data from the configuration file.
"""

import yaml


def get_config():
    """Get data from config."""
    with open('config.yml', 'r') as config_file:
        return yaml.safe_load(config_file)
