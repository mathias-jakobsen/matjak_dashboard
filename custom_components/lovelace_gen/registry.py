# -----------------------------------------------------------#
#       Imports
# -----------------------------------------------------------#

from __future__ import annotations
from .const import (
    CONF_AREA_ID,
    CONF_DEVICE_CLASS,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_EXCLUDE_AREAS,
    CONF_EXCLUDE_ENTITIES,
    CONF_ICON,
    CONF_ID,
    CONF_NAME,
    DEFAULT_AREA_ICON,
    DEFAULT_AREA_ICONS
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry, device_registry, entity_registry
from typing import Any, Dict, List


# -----------------------------------------------------------#
#       Functions
# -----------------------------------------------------------#

def get_registry(hass: HomeAssistant, config: Dict[str, Any]) -> list:
    exclude_areas = config.get(CONF_EXCLUDE_AREAS, [])
    exclude_entities = config.get(CONF_EXCLUDE_ENTITIES, [])

    areas = Areas(hass, exclude_areas)
    devices = Devices(hass, areas, [])
    entities = Entities(hass, areas, devices, exclude_entities)

    return {
        "areas": areas,
        "devices": devices,
        "entities": entities
    }

def slots_to_dict(obj: Dict[str, Any]):
    return { key: getattr(obj, key, None) for key in obj.__slots__ }


# -----------------------------------------------------------#
#       Class - Areas
# -----------------------------------------------------------#

class Areas:
    def __init__(self, hass: HomeAssistant, exclude_areas: list):
        self.hass = hass
        self.registry = { area_id: self._to_dict(area) for area_id, area in sorted(area_registry.async_get(self.hass).areas.items()) if area.name not in exclude_areas}

    def __iter__(self):
        for area in self.registry.values():
            yield area

    def get_by_id(self, id: str):
        area = self.registry.get(id, None)
        return area

    def get_by_name(self, name: str):
        area = next(filter(lambda area: area[CONF_NAME] == name, self.registry.values()), None)
        return area

    def _get_icon(self, area: area_registry.AreaEntry):
        icons = [icon.lower() for icon in DEFAULT_AREA_ICONS.keys()]
        return DEFAULT_AREA_ICONS[area.name] if area.name.lower() in icons else DEFAULT_AREA_ICON

    def _to_dict(self, area: area_registry.AreaEntry):
        return {
            **slots_to_dict(area),
            CONF_ICON: self._get_icon(area)
        }


# -----------------------------------------------------------#
#       Class - Devices
# -----------------------------------------------------------#

class Devices:
    def __init__(self, hass: HomeAssistant, areas: Areas, exclude_devices: list):
        self.areas = areas
        self.exclude_devices = exclude_devices
        self.hass = hass
        self.registry = { device_id: slots_to_dict(device) for device_id, device in sorted(device_registry.async_get(self.hass).devices.items()) if device_id not in exclude_devices}

    def __iter__(self):
        for device in self.registry.values():
            yield device

    def get_by_area(self, area_id_or_name: str):
        area = self.areas.get_by_id(area_id_or_name) or self.areas.get_by_name(area_id_or_name)

        if area is None:
            return []

        return [device for device in self.registry.values() if device[CONF_AREA_ID] == area[CONF_ID]]

    def get_by_id(self, id: str):
        device = self.registry.get(id, None)
        return device


# -----------------------------------------------------------#
#       Class - Entities
# -----------------------------------------------------------#

class Entities:
    def __init__(self, hass: HomeAssistant, areas: Areas, devices: Devices, exclude_entities: list):
        self.areas = areas
        self.devices = devices
        self.exclude_entities = exclude_entities
        self.hass = hass
        self.registry = { entity_id: self._to_dict(entity) for entity_id, entity in sorted(entity_registry.async_get(self.hass).entities.items()) if entity_id not in exclude_entities}

    def __iter__(self):
        for entity in self.registry.values():
            yield entity

    def get_by_area(self, area_id_or_name: str, domain: str = None):
        area = self.areas.get_by_id(area_id_or_name) or self.areas.get_by_name(area_id_or_name)

        if area is None:
            return []

        entities = [entity for entity in self.registry.values() if entity[CONF_AREA_ID] == area[CONF_ID]]

        for device in self.devices.get_by_area(area[CONF_ID]):
            for entity in [entity for entity in self.registry.values() if entity[CONF_DEVICE_ID] == device[CONF_ID]]:
                if entity[CONF_AREA_ID] is None:
                    entities.append(entity)

        if domain is not None:
            entities = self._get_by_domain(entities, *([domain] if type(domain) == str else [domain]))

        return entities

    def get_by_device_class(self, *device_classes: str):
        entities = []

        for entity_id, entity in self.registry.items():
            state = self.hass.states.get(entity_id)

            if state:
                device_class = state.attributes.get(CONF_DEVICE_CLASS, None)

                if device_class and device_class in device_classes:
                    entities.append(entity)

        return entities

    def get_by_domain(self, *domains: str):
        return self._get_by_domain(self.registry.values(), *domains)

    def get_by_id(self, id: str):
        entity = self.registry.get(id, None)
        return entity

    def _get_by_domain(self, entities: List[str], *domains: str):
        entities = filter(lambda entity: entity[CONF_DOMAIN] in domains, entities)
        return list(entities)

    def _to_dict(self, entity: entity_registry.RegistryEntry):
        state = self.hass.states.get(entity.entity_id) or {}
        entity_dict = slots_to_dict(entity)

        if state:
            entity_dict[CONF_DEVICE_CLASS] = state.attributes.get(CONF_DEVICE_CLASS, entity.device_class)
            entity_dict[CONF_ICON] = state.attributes.get(CONF_ICON, entity.icon)
            entity_dict[CONF_NAME] = state.attributes.get(CONF_NAME, entity.name)

        return entity_dict