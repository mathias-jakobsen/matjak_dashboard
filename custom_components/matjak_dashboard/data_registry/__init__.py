# -----------------------------------------------------------#
#       Imports
# -----------------------------------------------------------#

from ..const import (
    CONF_EXCLUDE_AREAS,
    CONF_EXCLUDE_DEVICES,
    CONF_EXCLUDE_ENTITIES
)
from .area_registry import AreaRegistry
from .device_registry import DeviceRegistry
from .entity_registry import EntityRegistry
from homeassistant.core import HomeAssistant
from logging import Logger
from typing import Any, Dict


# -----------------------------------------------------------#
#       Functions
# -----------------------------------------------------------#

def get_registry(hass: HomeAssistant, logger: Logger, config: Dict[str, Any]):
    exclude_areas = config.get(CONF_EXCLUDE_AREAS, [])
    exclude_devices = config.get(CONF_EXCLUDE_DEVICES, [])
    exclude_entities = config.get(CONF_EXCLUDE_ENTITIES, [])

    areas = AreaRegistry(hass, logger, exclude_areas)
    devices = DeviceRegistry(hass, logger, areas, exclude_devices)
    entities = EntityRegistry(hass, logger, areas, devices, exclude_entities)

    return {
        "areas": areas,
        "devices": devices,
        "entities": entities
    }