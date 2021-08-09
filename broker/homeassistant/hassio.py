from abc import ABC
import json
from typing import Any

from engine import InverterCore
from ..brokers import Publisher
from common.helper import LoggerFactory


class HassIo(ABC):
    _TELEMETRY_TOPIC: str = '/telemetry/STATE'
    _TELEMETRY_HASS_TOPIC: str = '/telemetry/HASS_STATE'
    _TELEMETRY_SENSOR_TOPIC: str = '/telemetry/SENSOR'

    def __init__(
            self,
            logger_factory: LoggerFactory,
            inverter: InverterCore,
            publisher: Publisher
    ) -> None:
        self._logger = logger_factory.create_logger(__name__)
        self._inverter = inverter
        self._publisher = publisher

    async def publish_state(self, data: Any = None, topic: str = _TELEMETRY_TOPIC):
        if data is None:
            return
        result = await self._publisher.publish_message({topic: data})
        if not result:
            self._logger.warning('Discovery failed to publish message to broker')


class Discovery(HassIo):

    async def broadcast_device_configuration(self, topic: str = HassIo._TELEMETRY_SENSOR_TOPIC):
        device_info = await self._inverter.fetch_device_information()
        device_info_state = json.dumps(device_info)
        result = await self._publisher.publish_message({topic: device_info_state})
        if not result:
            self._logger.warning('Discovery failed to publish message to broker')

    async def broadcast_device_sensor_state(self, topic: str = HassIo._TELEMETRY_SENSOR_TOPIC):
        device_info = await self._inverter.fetch_device_information()
        device_info_state = json.dumps(device_info)
        result = await self._publisher.publish_message({topic: device_info_state})
        if not result:
            self._logger.warning('Discovery failed to publish message to broker')


class Configuration(HassIo):

    async def broadcast_configuration_state(self, topic: str = HassIo._TELEMETRY_HASS_TOPIC):
        pass

    async def broadcast_energy_state(self, topic: str = HassIo._TELEMETRY_HASS_TOPIC):
        pass
