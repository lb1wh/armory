"""
Utilities
"""

import yaml

def read_config():
    """Read the config file."""
    config = open("../config.yaml")
    data = yaml.load(config, Loader=yaml.FullLoader)
    config.close()
    return data
