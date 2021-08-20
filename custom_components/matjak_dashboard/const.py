#-----------------------------------------------------------#
#       Custom Component
#-----------------------------------------------------------#

DOMAIN = "matjak_dashboard"


#-----------------------------------------------------------#
#       Configuration
#-----------------------------------------------------------#

CONF_AREA_ID = "area_id"
CONF_CONFIG_PATH = "config_path"
CONF_DEVICE_CLASS = "device_class"
CONF_DEVICE_ID = "device_id"
CONF_DOMAIN = "domain"
CONF_EXCLUDE_AREAS = "exclude_areas"
CONF_EXCLUDE_ENTITIES = "exclude_entities"
CONF_ICON = "icon"
CONF_ID = "id"
CONF_NAME = "name"
CONF_SIDEPANEL_ICON = "sidepanel_icon"
CONF_SIDEPANEL_TITLE = "sidepanel_title"


#-----------------------------------------------------------#
#       Parsing
#-----------------------------------------------------------#

PARSER_KEYWORD = "# matjak_dashboard"
PARSER_KEY_CONFIG = "config"
PARSER_KEY_GLOBAL = "_global"
PARSER_KEY_REGISTRY = "registry"


#-----------------------------------------------------------#
#       Defaults
#-----------------------------------------------------------#

DEFAULT_AREA_ICON = "mdi:texture-box"
DEFAULT_AREA_ICONS = {
    "Bathroom": "mdi:toilet",
    "Bedroom": "mdi:bed",
    "Bike Room": "mdi-bike",
    "Child Room": "mdi:baby",
    "Childs Room": "mdi:baby",
    "Child's Room": "mdi:baby",
    "Garage": "mdi:garage",
    "Hallway": "mdi:coat-rack",
    "Kitchen": "mdi:silverware-fork-knife",
    "Living Room": "mdi:sofa",
    "Office": "mdi:chair-rolling",
    "Utility Room": "mdi:washing-machine",
    "Wardrobe": "mdi:wardrobe",
    "Walk In": "mdi:wardrobe"
}
DEFAULT_CONFIG_PATH = "matjak_dashboard/"
DEFAULT_SIDEPANEL_ICON = "mdi:view-dashboard"
DEFAULT_SIDEPANEL_TITLE = "Matjak"


#-----------------------------------------------------------#
#       Dashboard & Themes
#-----------------------------------------------------------#

DASHBOARD_FILENAME = "custom_components/matjak_dashboard/lovelace/ui-lovelace.yaml"
DASHBOARD_URL = "matjak-dashboard"
PLUGIN_URL = "/matjak_dashboard/plugins"
THEMES_FILENAME = "custom_components/matjak_dashboard/themes/matjak_dashboard.yaml"