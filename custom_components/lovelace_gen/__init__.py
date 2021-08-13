#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

from .const import DOMAIN, CONF_CONFIG
from .filters import JINJA_FILTERS
from .parser import get_yaml_constructors, get_yaml_loader
from homeassistant.core import HomeAssistant
from homeassistant.util.yaml import loader
from logging import Logger, getLogger
from typing import Any, Dict
import jinja2


#-----------------------------------------------------------#
#       Constants
#-----------------------------------------------------------#

LOGGER = getLogger(__name__)


#-----------------------------------------------------------#
#       Functions
#-----------------------------------------------------------#

def setup_jinja_filters(jinja: jinja2.Environment) -> None:
    for key, value in JINJA_FILTERS.items():
        jinja.filters[key] = value

def setup_yaml_loader(logger: Logger, hass: HomeAssistant, jinja: jinja2.Environment, config_path: Dict[str, str]) -> None:
    load_yaml = get_yaml_loader(logger, hass, jinja, config_path)
    loader.load_yaml = load_yaml

    for key, value in get_yaml_constructors(logger, load_yaml).items():
        loader.SafeLineLoader.add_constructor(key, value)


#-----------------------------------------------------------#
#       Integration Setup
#-----------------------------------------------------------#

async def async_setup(hass: HomeAssistant, config: Dict[str, Any]):
    config_path = config.get(DOMAIN, {}).get(CONF_CONFIG, {})
    jinja = jinja2.Environment(loader=jinja2.FileSystemLoader("/"))

    setup_jinja_filters(jinja)
    setup_yaml_loader(LOGGER, hass, jinja, config_path)

    return True




