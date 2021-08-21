# -----------------------------------------------------------#
#       Imports
# -----------------------------------------------------------#

from .area_registry import AreaRegistry
from .base_registry import BaseRegistry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry, device_registry
from logging import Logger
from typing import List, Union


# -----------------------------------------------------------#
#       DeviceRegistry
# -----------------------------------------------------------#

class DeviceRegistry(BaseRegistry[device_registry.DeviceEntry]):
    #--------------------------------------------#
    #       Constructor
    #--------------------------------------------#

    def __init__(self, hass: HomeAssistant, logger: Logger, areas: AreaRegistry, exclude_devices: List[str] = []):
        super().__init__(hass, logger, {device_id: device for device_id, device in device_registry.async_get(hass).devices.items() if device.id not in exclude_devices and device.disabled_by is None})
        self.areas = areas


    #--------------------------------------------#
    #       Methods
    #--------------------------------------------#

    def get_by_area(self, area: Union[area_registry.AreaEntry, str]) -> List[device_registry.DeviceEntry]:
        if type(area) == str:
            area = self.areas.get_by_id(area) or self.areas.get_by_name(area)

        if area is None:
            return []

        return [device for device in self.registry.values() if device.area_id == area.id]