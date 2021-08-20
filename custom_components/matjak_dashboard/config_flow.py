#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

from __future__ import annotations
from . import DOMAIN
from .const import (
    CONF_CONFIG_PATH,
    CONF_SIDEPANEL_ICON,
    CONF_SIDEPANEL_TITLE,
    DEFAULT_CONFIG_PATH,
    DEFAULT_SIDEPANEL_ICON,
    DEFAULT_SIDEPANEL_TITLE
)
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import area_registry, config_validation as cv, entity_registry
from typing import Any, Dict, Union
import voluptuous as vol


#-----------------------------------------------------------#
#       Constants
#-----------------------------------------------------------#

# ------ Abort Reasons ---------------
ABORT_REASON_ALREADY_CONFIGURED = "already_configured"

# ------ Steps ---------------
STEP_INIT = "init"
STEP_USER = "user"


#-----------------------------------------------------------#
#       Steps
#-----------------------------------------------------------#

class MD_Steps:
    @staticmethod
    def init(hass: HomeAssistant, data: Dict[str, Any] = {}) -> vol.Schema:
        return vol.Schema({
            vol.Required(CONF_SIDEPANEL_TITLE, default=data.get(CONF_SIDEPANEL_TITLE, DEFAULT_SIDEPANEL_TITLE)): str,
            vol.Required(CONF_SIDEPANEL_ICON, default=data.get(CONF_SIDEPANEL_ICON, DEFAULT_SIDEPANEL_ICON)): str,
            vol.Required(CONF_CONFIG_PATH, default=data.get(CONF_CONFIG_PATH, DEFAULT_CONFIG_PATH)): str
        })


#-----------------------------------------------------------#
#       Config Flow
#-----------------------------------------------------------#

class MD_ConfigFlow(ConfigFlow, domain=DOMAIN):
    #--------------------------------------------#
    #       Static Properties
    #--------------------------------------------#

    VERSION = 1


    #--------------------------------------------#
    #       Static Methods
    #--------------------------------------------#

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> MD_OptionsFlow:
        return MD_OptionsFlow(config_entry)


    #--------------------------------------------#
    #       Methods
    #--------------------------------------------#

    async def async_step_user(self, user_input: Dict[str, Any] = None) -> Dict[str, Any]:
        if self._async_current_entries():
            self.async_abort(reason=ABORT_REASON_ALREADY_CONFIGURED)

        if user_input is not None:
            return self.async_create_entry(title=DOMAIN, data=user_input)

        schema = MD_Steps.init(self.hass)
        return self.async_show_form(step_id=STEP_USER, data_schema=schema)


#-----------------------------------------------------------#
#       Options Flow
#-----------------------------------------------------------#

class MD_OptionsFlow(OptionsFlow):
    #--------------------------------------------#
    #       Constructor
    #--------------------------------------------#

    def __init__(self, config_entry: ConfigEntry):
        self._config_entry = config_entry
        self._data = { **config_entry.data, **config_entry.options }


    #--------------------------------------------#
    #       Steps - Init
    #--------------------------------------------#

    async def async_step_init(self, user_input: Union[Dict[str, Any], None] = None) -> Dict[str, Any]:
        if user_input is not None:
            return self.async_create_entry(title=DOMAIN, data=user_input)

        schema = MD_Steps.init(self.hass, self._data)
        return self.async_show_form(step_id=STEP_INIT, data_schema=schema)