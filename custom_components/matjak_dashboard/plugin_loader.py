# -----------------------------------------------------------#
#       Imports
# -----------------------------------------------------------#

from .const import PLUGIN_URL
from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.lovelace.resources import ResourceStorageCollection
from homeassistant.util.yaml import loader
from logging import Logger


# -----------------------------------------------------------#
#       Constants
# -----------------------------------------------------------#

DATA_EXTRA_MODULE_URL = "frontend_extra_module_url"


# -----------------------------------------------------------#
#       Functions
# -----------------------------------------------------------#

async def async_create_resource(hass: HomeAssistant, logger: Logger, url: str) -> None:
    resources: ResourceStorageCollection = hass.data['lovelace']['resources']

    for item in resources.async_items():
        if item["url"].startswith(url):
            return

    if isinstance(resources, ResourceStorageCollection):
        await resources.async_create_item({"res_type": "module", "url": url})
    else:
        add_extra_js_url(hass, url)

async def async_load_plugins(hass: HomeAssistant, logger: Logger) -> None:
    plugin_path = hass.config.path("custom_components/matjak_dashboard/plugins")
    hass.http.register_static_path(PLUGIN_URL, plugin_path, True)

    for filename in loader._find_files(plugin_path, "*.js"):
        await async_create_resource(hass, logger, filename.replace(plugin_path, PLUGIN_URL))

async def async_unload_plugins(hass: HomeAssistant, logger: Logger) -> None:
    resources: ResourceStorageCollection = hass.data['lovelace']['resources']

    for item in resources.async_items():
        if not item["url"].startswith(PLUGIN_URL):
            continue

        await resources.async_delete_item(item["id"])
