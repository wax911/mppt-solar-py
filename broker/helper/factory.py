from logging import Logger

from paho.mqtt.client import Client, MQTTv5

from common.model import MQTTConfig


def create_default_client(
        logger: Logger,
        config: MQTTConfig
) -> Client:
    """
    Helper factory for creating a default client_ioc
    :param logger: A custom logger to log messages to
    :param config: Client configuration_ioc
    :return: A configured client_ioc
    """
    client = Client(protocol=MQTTv5)
    client.enable_logger(logger)
    client.username_pw_set(
        config.username,
        config.password
    )
    return client
