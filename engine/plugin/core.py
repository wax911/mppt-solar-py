from typing import Optional

from common.model import ResponseMapping, DeviceConfig
from common.helper import LoggerFactory
from ..model import DeviceInfo


class IPluginRegistry(type):
    plugin_registry: Optional[type] = None

    def __init__(cls, name, bases, attrs):
        super().__init__(cls)
        if name != 'InverterCore' or name != 'ProtocolCore':
            IPluginRegistry.plugin_registries = cls


class InverterCore(object, metaclass=IPluginRegistry):
    """
    Plugin core class for inverters
    """

    def __init__(self, device_config: DeviceConfig, logger_factory: LoggerFactory) -> None:
        """
        Entry init block for plugin
        :param device_config: Device configuration
        :param logger_factory: Logger that plugin can make use of
        """
        self.device_config = device_config
        self._logger = logger_factory.create_logger(__name__)

    async def invoke(self, command: str) -> ResponseMapping:
        """
        Starts main plugin flow
        :param command: command to execute
        :return: a device for the plugin
        """
        pass

    async def fetch_device_information(self) -> DeviceInfo:
        """
        Fetches the device information
        :return: Device information
        """
        pass

    async def fetch_settings(self) -> ResponseMapping:
        """
        Fetches the device current settings
        :return: Device information
        """
        pass

    async def fetch_status(self) -> ResponseMapping:
        """
        Fetches the device status, power, current, and other states
        :return: Device information
        """
        pass


class ProtocolCore(object, metaclass=IPluginRegistry):
    """
    Plugin core class for communication protocols
    """

    def __init__(self, logger_factory: LoggerFactory) -> None:
        """
        Entry init block for plugin
        :param logger_factory: Logger that plugin can make use of
        """
        self._logger = logger_factory.create_logger(__name__)

    async def invoke(self, command: str) -> ResponseMapping:
        """
        Starts main plugin flow
        :param command: command to execute
        :return: a device for the plugin
        """
        pass
