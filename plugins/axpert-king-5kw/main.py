from common.model import ResponseMapping
from engine import InverterCore
from engine.model import DeviceInfo


class AxpertKing5kW(InverterCore):

    async def invoke(self, command: str) -> ResponseMapping:
        return await super().invoke(command)

    async def fetch_device_information(self) -> DeviceInfo:
        return await super().fetch_device_information()

    async def fetch_settings(self) -> ResponseMapping:
        return await super().fetch_settings()

    async def fetch_status(self) -> ResponseMapping:
        return await super().fetch_status()
