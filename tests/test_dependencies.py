from logging import Logger
from typing import Union, Any, Optional
from unittest import TestCase

from paho.mqtt.client import Client

from common.helper import LoggerFactory
from common.model import Configuration
from di import ConfigurationProvider, LoggerProvider
from di.dependencies import ClientProvider, CrcProvider
from processor.helper import CyclicRedundancyCodeHelper


class TestConfigurationProvider(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._configuration: Union[Any, Optional, Configuration] = ConfigurationProvider.configuration_ioc()

    def test_configuration_instance(self):
        self.assertIsInstance(self._configuration, Configuration)


class TestLoggerProvider(TestCase):

    def setUp(self) -> None:
        super().setUp()
        _factory: LoggerFactory = LoggerProvider.logger_factory_ioc()
        self._logger: Union[Any, Optional, Logger] = _factory.create_logger(name=__name__)

    def test_logger_instance(self):
        self.assertIsInstance(self._logger, Logger)


class TestClientProvider(TestCase):

    def setUp(self) -> None:
        super().setUp()
        _factory: LoggerFactory = LoggerProvider.logger_factory_ioc()
        _logger: Union[Any, Optional, Logger] = _factory.create_logger(name=__name__)
        self._client: Union[Any, Optional, Client] = ClientProvider.client_ioc(logger=_logger)

    def test_client_instance(self):
        self.assertIsInstance(self._client, Client)


class TestCrcProvider(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._crc_helper: Union[Any, Optional, CyclicRedundancyCodeHelper] = CrcProvider.crc_ioc()

    def test_client_instance(self):
        self.assertIsInstance(self._crc_helper, CyclicRedundancyCodeHelper)
