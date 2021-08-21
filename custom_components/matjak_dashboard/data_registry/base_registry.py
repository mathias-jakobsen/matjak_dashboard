# -----------------------------------------------------------#
#       Imports
# -----------------------------------------------------------#

from homeassistant.core import HomeAssistant
from logging import Logger
from typing import Dict, Generic, TypeVar, Union


# -----------------------------------------------------------#
#       Type Variables
# -----------------------------------------------------------#

T = TypeVar("T")


# -----------------------------------------------------------#
#       BaseRegistry
# -----------------------------------------------------------#

class BaseRegistry(Generic[T]):
    #--------------------------------------------#
    #       Constructor
    #--------------------------------------------#

    def __init__(self, hass: HomeAssistant, logger: Logger, registry: Dict[str, T]):
        self.hass = hass
        self.logger = logger
        self.registry = registry


    #--------------------------------------------#
    #       Iterator
    #--------------------------------------------#

    def __iter__(self):
        for item in self.registry.values():
            yield item


    #--------------------------------------------#
    #       Methods
    #--------------------------------------------#

    def get_by_id(self, id: str) -> Union[T, None]:
        return self.registry.get(id, None)
