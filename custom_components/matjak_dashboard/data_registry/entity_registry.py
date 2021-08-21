# -----------------------------------------------------------#
#       Imports
# -----------------------------------------------------------#

from ..const import (
    CONF_DEVICE_CLASS
)
from .area_registry import AreaRegistry
from .base_registry import BaseRegistry
from .device_registry import DeviceRegistry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry, device_registry, entity_registry
from logging import Logger
from typing import List, Union


# -----------------------------------------------------------#
#       EntityRegistry
# -----------------------------------------------------------#

class EntityRegistry(BaseRegistry[entity_registry.RegistryEntry]):
    #--------------------------------------------#
    #       Constructor
    #--------------------------------------------#

    def __init__(self, hass: HomeAssistant, logger: Logger, areas: AreaRegistry, devices: DeviceRegistry, exclude_entities: List[str] = []):
        super().__init__(hass, logger, {entity_id: entity for entity_id, entity in entity_registry.async_get(hass).entities.items() if entity_id not in exclude_entities and entity.disabled_by is None})
        self.areas = areas
        self.devices = devices


    #--------------------------------------------#
    #       Methods
    #--------------------------------------------#

    def get_by_area(self, area: Union[area_registry.AreaEntry, str], domain: Union[str, List[str], None] = None) -> List[entity_registry.RegistryEntry]:
        if type(area) == str:
            area = self.areas.get_by_id(area) or self.areas.get_by_name(area)

        if area is None:
            return []

        entities = [entity for entity in self.registry.values() if entity.area_id == area.id]
        devices = self.devices.get_by_area(area)

        for device in devices:
            for entity in [entity for entity in self.registry.values() if entity.device_id == device.id]:
                if entity.area_id is None:
                    entities.append(entity)

        if domain:
            entities = self._get_by_domain(entities, *([domain] if type(domain) == str else domain))

        return entities

    def get_by_domain(self, *domains: str) -> List[entity_registry.RegistryEntry]:
        return self._get_by_domain(self.registry.values(), *domains)

    def get_by_device_class(self, *device_classes: str) -> List[entity_registry.RegistryEntry]:
        result = []

        for entity in self.registry.values():
            state = self.hass.states.get(entity.entity_id)
            device_class = entity.device_class if state is None else state.attributes.get(CONF_DEVICE_CLASS, None)

            if device_class and device_class in device_classes:
                result.append(entity)

        return result


    #--------------------------------------------#
    #       Private Methods
    #--------------------------------------------#

    def _get_by_domain(self, entities: List[entity_registry.RegistryEntry], *domains: str) -> List[entity_registry.RegistryEntry]:
        return [entity for entity in entities if entity.domain in domains]