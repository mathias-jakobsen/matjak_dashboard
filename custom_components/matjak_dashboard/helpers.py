#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

from homeassistant.core import HomeAssistant
from homeassistant.util.yaml import loader
from typing import Callable


#-----------------------------------------------------------#
#       Functions
#-----------------------------------------------------------#

def get_button_card_template_list(hass: HomeAssistant, load_yaml: Callable) -> bool:
    result = []
    path = hass.config.path("custom_components/matjak_dashboard/lovelace/templates/button_card/")

    for filename in loader._find_files(path, "*.yaml"):
        templates = load_yaml(filename)

        if isinstance(templates, dict):
            result = result + list(templates.keys())

    return result

