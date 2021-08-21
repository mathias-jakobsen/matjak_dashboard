# -----------------------------------------------------------#
#       Imports
# -----------------------------------------------------------#

from ..const import (
    DEFAULT_AREA_ICON,
    DEFAULT_AREA_ICONS
)
from .base_registry import BaseRegistry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry
from logging import Logger
from typing import List, Union


# -----------------------------------------------------------#
#       AreaRegistry
# -----------------------------------------------------------#

class AreaRegistry(BaseRegistry[area_registry.AreaEntry]):
    #--------------------------------------------#
    #       Constructor
    #--------------------------------------------#

    def __init__(self, hass: HomeAssistant, logger: Logger, exclude_areas: List[str] = []):
        super().__init__(hass, logger, {area_id: area for area_id, area in area_registry.async_get(hass).areas.items() if len(set([area.id, area.name]).intersection(exclude_areas)) == 0})


    #--------------------------------------------#
    #       Methods
    #--------------------------------------------#

    def get_area_icon(self, area_entry: area_registry.AreaEntry) -> str:
        return DEFAULT_AREA_ICONS.get(area_entry.name, DEFAULT_AREA_ICON)

    def get_by_name(self, name: str) -> Union[area_registry.AreaEntry, None]:
        return next((area for area in self.registry.values() if area.name == name), None)