#-----------------------------------------------------------#
#       Imports
#-----------------------------------------------------------#

from homeassistant.core import HomeAssistant
from .const import  PARSER_KEYWORD, PARSER_KEY_CONFIG, PARSER_KEY_GLOBAL, PARSER_KEY_REGISTRY
from .data_registry import DataRegistry
from collections import OrderedDict
from homeassistant.exceptions import HomeAssistantError
from homeassistant.util.yaml import loader
from jinja2.environment import Environment
from logging import Logger
from typing import Dict
import io
import os
import time


#-----------------------------------------------------------#
#       Setup
#-----------------------------------------------------------#

def get_parser(logger: Logger, hass: HomeAssistant, jinja: Environment, config_paths: Dict[str, str], data_registry: DataRegistry):
    #-----------------------------------------------------------#
    #       YAML Parsers
    #-----------------------------------------------------------#

    def load_config():
        result = {}

        for key, value in config_paths.items():
            path = hass.config.path(value)
            result[key] = {}

            if os.path.exists(path):
                dashboard_config = {}

                for filename in loader._find_files(path, "*.yaml"):
                    config = load_yaml(filename)
                    if isinstance(config, dict):
                        dashboard_config.update(config)

                result[key].update(dashboard_config)

        return result

    def load_yaml(filename, secrets = None, args = {}):
        try:
            is_lovelace_gen = False
            with open(filename, encoding="utf-8") as file:
                if file.readline().lower().startswith(PARSER_KEYWORD):
                    is_lovelace_gen = True

            if is_lovelace_gen:
                stream = io.StringIO(jinja.get_template(filename).render({
                            **args,
                            PARSER_KEY_GLOBAL: {
                                PARSER_KEY_CONFIG: load_config(),
                                PARSER_KEY_REGISTRY: data_registry.get()
                            }
                        }))
                stream.name = filename
                return loader.yaml.load(stream, Loader=lambda _stream: loader.SafeLineLoader(_stream, secrets)) or OrderedDict()
            else:
                with open(filename, encoding="utf-8") as file:
                    return loader.yaml.load(file, Loader=lambda stream: loader.SafeLineLoader(stream, secrets)) or OrderedDict()
        except loader.yaml.YAMLError as exc:
            logger.error(str(exc))
            raise HomeAssistantError(exc)
        except UnicodeDecodeError as exc:
            logger.error("Unable to read file %s: %s", filename, exc)
            raise HomeAssistantError(exc)


    #-----------------------------------------------------------#
    #       YAML Constructors
    #-----------------------------------------------------------#

    def include_yaml(ldr, node):
        args = {}
        if isinstance(node.value, str):
            fn = node.value
        else:
            fn, args, *_ = ldr.construct_sequence(node)
        filename = os.path.abspath(os.path.join(os.path.dirname(ldr.name), fn))
        try:
            return loader._add_reference(
                load_yaml(filename, ldr.secrets, args=args), ldr, node
            )
        except FileNotFoundError as exc:
            logger.error("Unable to include file %s: %s", filename, exc)
            raise HomeAssistantError(exc)

    def uncache_file(ldr, node):
        path = node.value
        timestamp = str(time.time())
        if "?" in path:
            return f"{path}&{timestamp}"
        return f"{path}?{timestamp}"


    #-----------------------------------------------------------#
    #       Return
    #-----------------------------------------------------------#

    return load_yaml, {
        "!include": include_yaml,
        "!file": uncache_file
    }