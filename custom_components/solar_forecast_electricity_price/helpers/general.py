from homeassistant.config_entries import ConfigEntry
from typing import Any

def get_parameter(config_entry: ConfigEntry, parameter: str, default_val: Any = None):
    """Get parameter from OptionsFlow or ConfigFlow"""
    if parameter in config_entry.options.keys():
        return config_entry.options.get(parameter)
    if parameter in config_entry.data.keys():
        return config_entry.data.get(parameter)
    return default_val
