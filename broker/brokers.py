from abc import ABC
from logging import Logger
from typing import Dict, Optional, Any

from paho.mqtt.reasoncodes import ReasonCodes
from paho.mqtt.client import Client, MQTTMessage, MQTTMessageInfo
from paho.mqtt.properties import Properties

from common.model.settings import MQTTConfig


class Core(ABC):
    _main_topic = 'homeassistant/sensor'

    def __init__(self, logger: Logger, client: Client, config: MQTTConfig) -> None:
        self._logger = logger
        self._client = client
        self._config = config

    def _on_connect(
            self,
            client: Client,
            user_data: Optional[Any],
            flags: Dict,
            reason_code: ReasonCodes,
            properties: Properties
    ) -> None:
        """
        Callback that is called when a connection is made
        :param client: The client_ioc instance for this callback
        :param user_data: The private user data as set upon client_ioc creation
        :param flags: ResponseMapping flags sent by the broker
        :param reason_code: The MQTT v5.0 reason code: an instance of the ReasonCode class.
        :param properties: The MQTT v5.0 properties returned from the broker. An instance of the Properties class.
        """
        pass

    def _on_message(
            self,
            client: Client,
            user_data: Optional[Any],
            message: MQTTMessage
    ) -> None:
        """
        Callback for when a message is received
        :param client: The client_ioc instance for this callback
        :param user_data: The private user data as set upon client_ioc creation
        :param message: An instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
        """
        pass

    async def _connect_to_client(self) -> None:
        """
        Connects to client_ioc and sets up everything
        """
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect_async(self._config.host, self._config.port)
        self._client.loop_forever(timeout=15.0, retry_first_connection=True)

    async def start(self) -> None:
        """
        Broker starting point
        """
        try:
            await self._connect_to_client()
        except KeyboardInterrupt as e:
            self._logger.error('Publisher interrupted by user cancellation', exc_info=e)
        except Exception as e:
            self._logger.error('Publisher unable to connect to host', exc_info=e)
        finally:
            if self._client.is_connected():
                self._logger.info('Attempting to disconnect publisher...')
                self._client.unsubscribe(f'{self._main_topic}/{self._config.topic}')
                self._client.disconnect()


class Publisher(Core):

    def _on_connect(self, client: Client, user_data: Optional[Any], flags: Dict, reason_code: ReasonCodes,
                    properties: Properties) -> None:
        super()._on_connect(client, user_data, flags, reason_code, properties)

    def _on_message(self, client: Client, user_data: Optional[Any], message: MQTTMessage) -> None:
        super()._on_message(client, user_data, message)

    async def __invoke_publish(self, key: str, value: Any) -> MQTTMessageInfo:
        info = self._client.publish(
            topic=f'{self._main_topic}/{self._config.topic}/{key}',
            payload=value,
            qos=0,
            retain=True,
            properties=None
        )
        info.wait_for_publish()
        return info

    async def publish_message(self, payload: Dict) -> bool:
        """
        Publish a message on a topic.
        :param payload: Message to send
        """
        if not self._client.is_connected():
            self._logger.warning('Publisher cannot send message as client has been disconnected')
            return False

        for _key, _value in payload:
            info = await self.__invoke_publish(_key, _value)
            self._logger.debug(f'Publish end with info: {info}')


class Subscriber(Core):

    def _on_connect(
            self,
            client: Client,
            user_data: Optional[Any],
            flags: Dict,
            reason_code: ReasonCodes,
            properties: Properties
    ) -> None:
        if reason_code.value:
            self._logger.debug(f'Connected: {reason_code.getName()} -> {flags}')
            client.subscribe(f'{self._main_topic}/{self._config.topic}')
        else:
            self._logger.debug(f'Failed to connect: {reason_code.getName()} -> {flags} | {user_data}')

    def _on_message(
            self,
            client: Client,
            user_data: Optional[Any],
            message: MQTTMessage
    ) -> None:
        """TODO: Call dispatch module to handle received commands/message"""
        self._logger.info(f'New message received: {message.topic} -> {str(message.payload)}')
