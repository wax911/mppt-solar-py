import asyncio
from abc import ABC
from textwrap import wrap

import aiofiles
import serial
from multiprocessing import Queue

from typing import Optional

from common.helper import LoggerFactory
from common.model import DeviceConfig, RawResponse, Command
from processor.helper import CyclicRedundancyCodeHelper


class DispatcherContract(ABC):
    _message_queue: Queue = Queue(maxsize=25)

    def __init__(
            self,
            logger_factory: LoggerFactory,
            device_configuration: DeviceConfig,
            crc_calculator: CyclicRedundancyCodeHelper
    ) -> None:
        self._logger = logger_factory.create_logger(__name__)
        self._device_config = device_configuration
        self._crc_calculator = crc_calculator

    async def _execute_command(self, cmd: str) -> Optional[RawResponse]:
        pass

    async def queue_pending_command(self, command: Command) -> None:
        self._message_queue.put(obj=command)


class CommandDispatcher(DispatcherContract):

    async def __send_serial_command(self, command: Command) -> Optional[RawResponse]:
        try:
            self._logger.debug(
                f'Connecting to interface: {self._device_config.interface} and executing command: {command}'
            )
            with serial.serial_for_url(self._device_config.interface, self._device_config.baud_rate) as stream:
                message = str(command)
                stream.write_timeout = 2
                written = stream.write(message)
                stream.flushOutput()
                self._logger.debug(
                    f'Write result -> total bytes: {written} | message: {message}'
                )
                return written > 0
        except Exception as e:
            self._logger.error(f'Error occurred while executing command: {command}', exc_info=e)
        return None

    async def __send_usb_command(self, command: Command) -> Optional[RawResponse]:
        try:
            self._logger.debug(
                f'Connecting to interface: {self._device_config.interface} and executing command: {command}'
            )
            async with aiofiles.open(file=self._device_config.interface, mode='rw') as stream:
                full_text_command = str(command)
                for chunk in wrap(
                        text=str(command),
                        width=8,
                        expand_tabs=False,
                        replace_whitespace=False,
                        fix_sentence_endings=False,
                        break_long_words=False,
                        drop_whitespace=False,
                        break_on_hyphens=False
                ):
                    written = await stream.write(chunk)
                    await asyncio.sleep(0.16)
                # await response from device
                response = await stream.readline()
                self._logger.debug(
                    f'Write result -> total bytes: {written} | command: {command}'
                )
                return RawResponse(response, command)
        except Exception as e:
            self._logger.error(f'Error occurred while executing command: {command}', exc_info=e)
        return None

    async def _execute_command(self, cmd: str) -> Optional[RawResponse]:
        raw_response: Optional[RawResponse] = None
        command = self._crc_calculator.command_with_crc(cmd)
        if self._device_config.is_serial:
            raw_response = await self.__send_serial_command(command)
        else:
            raw_response = await self.__send_usb_command(command)
        return None
