#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

from .const import DOMAIN, CONF_CONFIG
from .filters import JINJA_FILTERS
from .parser import get_yaml_constructors, get_yaml_loader
from .registry import Registry
from homeassistant.core import HomeAssistant
from homeassistant.util.yaml import loader
from logging import Logger, getLogger
from typing import Any, Dict
import jinja2

from homeassistant.components.lovelace.dashboard import LovelaceYAML
from homeassistant.components.lovelace import _register_panel


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

def setup_yaml_loader(logger: Logger, hass: HomeAssistant, jinja: jinja2.Environment, config_paths: Dict[str, str], registry: Registry) -> None:
    load_yaml = get_yaml_loader(logger, hass, jinja, config_paths, registry)
    loader.load_yaml = load_yaml

    for key, value in get_yaml_constructors(logger, load_yaml).items():
        loader.SafeLineLoader.add_constructor(key, value)


#-----------------------------------------------------------#
#       Integration Setup
#-----------------------------------------------------------#

async def async_setup(hass: HomeAssistant, config: Dict[str, Any]):
    config_paths = config.get(DOMAIN, {}).get(CONF_CONFIG, {})
    jinja = jinja2.Environment(loader=jinja2.FileSystemLoader("/"))
    registry = Registry(LOGGER, hass)

    setup_jinja_filters(jinja)
    setup_yaml_loader(LOGGER, hass, jinja, config_paths, registry)

    url = "test-test"
    config = {
        "mode": "yaml",
        "icon": "mdi:view-dashboard",
        "title": "Test",
        "filename": "custom_components/lovelace_gen/lovelace/ui-lovelace.yaml",
        "show_in_sidebar": True,
        "require_admin": False,
    }

    hass.data["lovelace"]["dashboards"][url] = LovelaceYAML(hass, url, config)
    _register_panel(hass, url, "yaml", config, False)

    return True




