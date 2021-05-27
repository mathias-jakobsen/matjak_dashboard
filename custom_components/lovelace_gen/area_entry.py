#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

from .const import DEFAULT_AREA_ICON
from homeassistant.helpers import area_registry
import attr


#-----------------------------------------------------------#
#       Class AreaEntry
#-----------------------------------------------------------#

@attr.s(slots=True, frozen=True)
class AreaEntry(area_registry.AreaEntry):
    icon: str = attr.ib(default=DEFAULT_AREA_ICON)