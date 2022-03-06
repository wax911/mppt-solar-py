import os
from importlib import import_module
from typing import Optional, Any, List

from common.helper import LoggerFactory, FileSystem
from .. import InverterCore
from ..helper import PluginUtility
from ..plugin import IPluginRegistry


class PluginUseCase:
    __loaded_module: Optional[type] = None

    def __init__(
            self,
            logger_factory: LoggerFactory,
            plugin_utility: PluginUtility,
            plugin_name: str
    ) -> None:
        super().__init__()
        self._logger = logger_factory.create_logger(__name__)
        self._plugin_name = plugin_name
        self._plugin_utility = plugin_utility
        self._logger_factory = logger_factory

    def __check_loaded_plugin_state(self, plugin_module: Any):
        if IPluginRegistry.plugin_registry is not None:
            latest_module = IPluginRegistry.plugin_registry
            latest_module_name = latest_module.__module__
            current_module_name = plugin_module.__name__
            if current_module_name == latest_module_name:
                self._logger.debug(f'Successfully imported module `{current_module_name}`')
                self.__loaded_module = latest_module
            else:
                self._logger.error(
                    f'Expected to import -> `{current_module_name}` but got -> `{latest_module_name}`'
                )
            # clear plugins from the registry when we're done with them
            IPluginRegistry.plugin_registry = None
        else:
            self._logger.error(f'No plugin found in registry for module: {plugin_module}')

    def __search_for_plugins_in(self, plugins_path: List[str], package_name: str):
        for directory in plugins_path:
            entry_point = self._plugin_utility.setup_plugin_configuration(package_name, directory)
            if entry_point is not None:
                plugin_name, plugin_ext = os.path.splitext(entry_point)
                # Importing the module will cause IPluginRegistry to invoke it's __init__ fun
                import_target_module = f'.{directory}.{plugin_name}'
                module = import_module(import_target_module, package_name)
                self.__check_loaded_plugin_state(module)
            else:
                self._logger.debug(f'No valid plugin found in {package_name}')

    def discover_plugins(self, reload: bool):
        """
        Discover the plugin classes contained in Python files, given a
        list of directory names to scan.
        """
        if reload:
            self.__loaded_module = None
            IPluginRegistry.plugin_registry = None
            _plugins_package = FileSystem.get_plugins_directory()
            self._logger.debug(f'Searching for plugins under package {_plugins_package}')
            plugins_path = PluginUtility.filter_plugins_paths(_plugins_package)
            package_name = os.path.basename(os.path.normpath(_plugins_package))
            self.__search_for_plugins_in(plugins_path, package_name)

    @staticmethod
    def register_plugin(module: type, logger_factory: LoggerFactory) -> InverterCore:
        """
        Create a plugin instance from the given module
        :param module: module to initialize
        :param logger_factory: factory for creating a logger
        :return: a high level plugin
        """
        return module(logger_factory)

    @staticmethod
    def hook_plugin(plugin: InverterCore):
        """
        Return a function accepting commands.
        """
        return plugin.invoke
