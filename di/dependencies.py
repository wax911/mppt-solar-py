import dependency_injector.containers as containers
import dependency_injector.providers as providers

from dependency_injector.providers import ThreadSafeSingleton, Factory

from common.model import Configuration
from common.helper import FileSystem, LoggerFactory
from broker.helper import create_default_client
from processor.helper import CyclicRedundancyCodeHelper


class ConfigurationProvider(containers.DeclarativeContainer):
    """IoC container of configuration_ioc providers."""
    configuration_ioc: ThreadSafeSingleton = providers.ThreadSafeSingleton(
        FileSystem.load_configuration,
        type_definition=Configuration
    )


class LoggerProvider(containers.DeclarativeContainer):
    """IoC container of logger providers."""
    logger_factory_ioc: ThreadSafeSingleton = providers.ThreadSafeSingleton(
        LoggerFactory,
        config=ConfigurationProvider.configuration_ioc()
    )


class ClientProvider(containers.DeclarativeContainer):
    client_ioc: Factory = providers.Factory(
        create_default_client,
        config=ConfigurationProvider.configuration_ioc().mqtt
    )


class CrcProvider(containers.DeclarativeContainer):
    crc_ioc: Factory = providers.Factory(
        CyclicRedundancyCodeHelper,
        logger_factory=LoggerProvider.logger_factory_ioc()
    )
