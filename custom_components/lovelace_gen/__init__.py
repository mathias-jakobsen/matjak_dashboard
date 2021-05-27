#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

from jinja2.environment import Environment
from .const import DOMAIN, CONF_CONFIG
from .data_registry import DataRegistry
from .filters import JINJA_FILTERS
from .parser import get_parser
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

def setup_jinja_filters(jinja: Environment) -> None:
    for key, value in JINJA_FILTERS.items():
        jinja.filters[key] = value

def setup_parser(logger: Logger, hass: HomeAssistant, jinja: Environment, config_paths: Dict[str, str], data_registry: DataRegistry) -> None:
    parser, parser_constructors = get_parser(logger, hass, jinja, config_paths, data_registry)
    loader.load_yaml = parser
    for key, value in parser_constructors.items():
        loader.SafeLineLoader.add_constructor(key, value)


#-----------------------------------------------------------#
#       Integration Setup
#-----------------------------------------------------------#

async def async_setup(hass: HomeAssistant, config: Dict[str, Any]):
    config_paths = config.get(DOMAIN, {}).get(CONF_CONFIG, {})
    data_registry = DataRegistry(LOGGER, hass)
    jinja = jinja2.Environment(loader=jinja2.FileSystemLoader("/"))

    setup_jinja_filters(jinja)
    setup_parser(LOGGER, hass, jinja, config_paths, data_registry)

    return True




