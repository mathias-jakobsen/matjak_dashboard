
#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

from homeassistant.core import HomeAssistant
from homeassistant.helpers.area_registry import async_get as async_get_area_registry
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from logging import Logger


class DataRegistry:
    #-----------------------------------------------------------#
    #       Constructor
    #-----------------------------------------------------------#

    def __init__(self, logger: Logger, hass: HomeAssistant):
        self.hass = hass
        self.logger = logger


    #-----------------------------------------------------------#
    #       Public Methods
    #-----------------------------------------------------------#

    def get(self):
        areas = self._get_areas()
        entities = self._get_entities()
        entities_by_domain = self._get_entities_by_domain()

        return {
            "areas": areas,
            "entities": entities,
            "entities_by_domain": entities_by_domain
        }



    #-----------------------------------------------------------#
    #       Private Methods - Registry
    #-----------------------------------------------------------#

    def _get_areas(self):
        return async_get_area_registry(self.hass).areas.values()

    def _get_entities(self):
        return async_get_entity_registry(self.hass).entities.values()

    def _get_entities_by_domain(self):
        entities = self._get_entities()
        entities_by_domain = {}

        for entity in entities:
            domain = entity.entity_id.split(".")[0]

            if not domain in entities_by_domain:
                entities_by_domain[domain] = []

            entities_by_domain[domain].append(entity)

        return entities_by_domain