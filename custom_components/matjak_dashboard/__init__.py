#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

from .const import (
    CONF_SIDEPANEL_ICON,
    CONF_SIDEPANEL_TITLE,
    DASHBOARD_FILENAME,
    DASHBOARD_URL,
    DOMAIN
)
from .filters import JINJA_FILTERS
from .plugin_loader import async_load_plugins, async_unload_plugins
from .yaml_loader import get_yaml_constructors, get_yaml_loader
from homeassistant.config_entries import ConfigEntry
from homeassistant.components import frontend
from homeassistant.components.lovelace.dashboard import LovelaceYAML
from homeassistant.components.lovelace import _register_panel
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import IntegrationError
from homeassistant.util.yaml import loader
from logging import Logger, getLogger
from typing import Any, Dict
import jinja2


#-----------------------------------------------------------#
#       Constants
#-----------------------------------------------------------#

LOGGER = getLogger(__name__)
PLATFORMS = []
UNDO_UPDATE_LISTENER = "undo_update_listener"


#-----------------------------------------------------------#
#       Functions
#-----------------------------------------------------------#

def setup_jinja_filters(jinja: jinja2.Environment) -> None:
    for key, value in JINJA_FILTERS.items():
        jinja.filters[key] = value

def setup_yaml_loader(logger: Logger, hass: HomeAssistant, jinja: jinja2.Environment, config_entry: ConfigEntry) -> None:
    load_yaml = get_yaml_loader(logger, hass, jinja, config_entry)
    loader.load_yaml = load_yaml

    for key, value in get_yaml_constructors(logger, load_yaml).items():
        loader.SafeLineLoader.add_constructor(key, value)


#-----------------------------------------------------------#
#       Integration Setup
#-----------------------------------------------------------#

async def async_setup(hass: HomeAssistant, config: Dict[str, Any]) -> bool:
    if "browser_mod" not in config:
        raise IntegrationError("Integration dependencies not met: Custom component 'browser_mod' is not setup.")

    await async_load_plugins(hass, LOGGER)
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    jinja = jinja2.Environment(loader=jinja2.FileSystemLoader("/"))

    setup_jinja_filters(jinja)
    setup_yaml_loader(LOGGER, hass, jinja, config_entry)

    data = hass.data.setdefault(DOMAIN, {})
    data[config_entry.entry_id] = {
        UNDO_UPDATE_LISTENER: config_entry.add_update_listener(async_update_options)
    }

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, platform)
        )

    sidepanel_icon = config_entry.options.get(CONF_SIDEPANEL_ICON, config_entry.data.get(CONF_SIDEPANEL_ICON))
    sidepanel_title = config_entry.options.get(CONF_SIDEPANEL_TITLE, config_entry.data.get(CONF_SIDEPANEL_TITLE))

    dashboard_config = {
        "mode": "yaml",
        "icon": sidepanel_icon,
        "title": sidepanel_title,
        "filename": DASHBOARD_FILENAME,
        "show_in_sidebar": True,
        "require_admin": False
    }

    hass.data["lovelace"]["dashboards"][DASHBOARD_URL] = LovelaceYAML(hass, DASHBOARD_URL, dashboard_config)
    _register_panel(hass, DASHBOARD_URL, "yaml", dashboard_config, False)

    return True

async def async_update_options(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(config_entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    unload_ok = all(
        [
            await hass.config_entries.async_forward_entry_unload(config_entry, platform)
            for platform in PLATFORMS
        ]
    )

    data = hass.data[DOMAIN]
    data[config_entry.entry_id][UNDO_UPDATE_LISTENER]()

    if unload_ok:
        data.pop(config_entry.entry_id)
        frontend.async_remove_panel(hass, DASHBOARD_URL)
        hass.data["lovelace"]["dashboards"].pop(DASHBOARD_URL)

    return unload_ok

async def async_remove_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    await async_unload_plugins(hass, LOGGER)
    hass.async_create_task(hass.services.async_call("browser_mod", "toast", { "duration": 3000, "message": f"Restart Homeassistant to finalize removal of {DOMAIN}." }))