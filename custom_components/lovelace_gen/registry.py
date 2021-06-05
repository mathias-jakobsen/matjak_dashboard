#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

from homeassistant.const import CONF_NAME
from .const import CONF_ICON, DEFAULT_AREA_ICON, DEFAULT_AREA_ICONS
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry, device_registry, entity_registry
from logging import Logger


#-----------------------------------------------------------#
#       Functions
#-----------------------------------------------------------#

def slots_to_dict(obj: dict):
    return { key: getattr(obj, key, None) for key in obj.__slots__ }


#-----------------------------------------------------------#
#       Class - Areas
#-----------------------------------------------------------#

class Areas:
    def __init__(self, logger: Logger, hass: HomeAssistant):
        self.logger = logger
        self.hass = hass
        self.registry = area_registry.async_get(self.hass)

    def __iter__(self):
        for area in self.registry.areas.values():
            yield self._to_dict(area)

    def get_by_id(self, id: str):
        area = self.registry.async_get_area(id)
        return self._to_dict(area) if area is not None else None

    def get_by_name(self, name: str):
        area = self.registry.async_get_area_by_name(name)
        return self._to_dict(area) if area is not None else None

    def _get_icon(self, area: area_registry.AreaEntry):
        icons = [icon.lower() for icon in DEFAULT_AREA_ICONS.keys()]
        return DEFAULT_AREA_ICONS[area.name] if area.name.lower() in icons else DEFAULT_AREA_ICON

    def _to_dict(self, area: area_registry.AreaEntry):
        return {
            **slots_to_dict(area),
            CONF_ICON: self._get_icon(area)
        }


#-----------------------------------------------------------#
#       Class - Devices
#-----------------------------------------------------------#

class Devices:
    def __init__(self, logger: Logger, hass: HomeAssistant, areas: Areas):
        self.areas = areas
        self.logger = logger
        self.hass = hass
        self.registry = device_registry.async_get(self.hass)

    def __iter__(self):
        for device in self.registry.devices.values():
            yield slots_to_dict(device)

    def get_by_area(self, area_id_or_name: str):
        area = self.areas.registry.async_get_area(area_id_or_name) or self.areas.registry.async_get_area_by_name(area_id_or_name)

        if area is None:
            return []

        return [slots_to_dict(device) for device in device_registry.async_entries_for_area(self.registry, area.id)]

    def get_by_id(self, id: str):
        device = self.registry.async_get(id)
        return slots_to_dict(device) if device is not None else None


#-----------------------------------------------------------#
#       Class - Entities
#-----------------------------------------------------------#

class Entities:
    def __init__(self, logger: Logger, hass: HomeAssistant, areas: Areas, devices: Devices):
        self.areas = areas
        self.devices = devices
        self.logger = logger
        self.hass = hass
        self.registry = entity_registry.async_get(self.hass)

    def __iter__(self):
        for entity in self.registry.entities.values():
            yield self._to_dict(entity)

    def get_by_area(self, area_id_or_name: str):
        area = self.areas.registry.async_get_area(area_id_or_name) or self.areas.registry.async_get_area_by_name(area_id_or_name)

        if area is None:
            return []

        entities = entity_registry.async_entries_for_area(self.registry, area.id)
        devices = device_registry.async_entries_for_area(self.devices.registry, area.id)

        for device in devices:
            for entity in entity_registry.async_entries_for_device(self.registry, device.id):
                if entity.area_id is None:
                    entities.append(entity)

        return [self._to_dict(entity) for entity in entities]

    def get_by_device_class(self, *device_classes: str):
        entities = filter(lambda entity: entity.device_class in device_classes, self.registry.entities.values())
        return [self._to_dict(entity) for entity in entities]

    def get_by_domain(self, *domains: str):
        entities = filter(lambda entity: entity.domain in domains, self.registry.entities.values())
        return [self._to_dict(entity) for entity in entities]

    def get_by_id(self, id: str):
        entity = self.registry.async_get(id)
        return self._to_dict(entity) if entity is not None else None

    def _to_dict(self, entity: entity_registry.RegistryEntry):
        return {
            **slots_to_dict(entity),
            CONF_ICON: entity.icon or entity.original_icon,
            CONF_NAME: entity.name or entity.original_name
        }


#-----------------------------------------------------------#
#       Class - Registry
#-----------------------------------------------------------#

class Registry:
    def __init__(self, logger: Logger, hass: HomeAssistant):
        self.areas = Areas(logger, hass)
        self.devices = Devices(logger, hass, self.areas)
        self.entities = Entities(logger, hass, self.areas, self.devices)
        self.logger = logger
        self.hass = hass