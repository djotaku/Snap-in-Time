"""Load the config file."""

import json

from xdgenvpy import XDGPedanticPackage  # type: ignore


def import_config() -> dict:
    """Import config file.

    :returns: A dictionary containing configs
    :raises: FileNotFoundError
    """
    xdg = XDGPedanticPackage('snapintime')
    try:
        with open(f"{xdg.XDG_CONFIG_HOME}/config.json") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("Could not find config file.")
        raise
