from ctypes import c_uint8
from typing import List

from common.model.commands import Command, Crc
from common.helper import LoggerFactory


class CyclicRedundancyCodeHelper:
    """
    Credits: https://forums.aeva.asn.au/viewtopic.php?title=pip4048ms-inverter&p=53760&t=4332#p53760
    """

    __crc_lookup: List[int] = [
        0x0000, 0x1021, 0x2042, 0x3063,
        0x4084, 0x50a5, 0x60c6, 0x70e7,
        0x8108, 0x9129, 0xa14a, 0xb16b,
        0xc18c, 0xd1ad, 0xe1ce, 0xf1ef
    ]

    def __init__(self, logger_factory: LoggerFactory) -> None:
        self._logger = logger_factory.create_logger(__name__)

    @staticmethod
    def __create_crc(checksum: int) -> Crc:
        checksum_low = c_uint8(checksum).value
        checksum_high = c_uint8(checksum >> 8).value

        if checksum_low == 0x28 or checksum_low == 0x0d or checksum_low == 0x0a:
            checksum_low += 1
        if checksum_high == 0x28 or checksum_high == 0x0d or checksum_high == 0x0a:
            checksum_high += 1

        return Crc(checksum_high, checksum_low)

    def calculate_crc(self, command: str) -> Crc:
        """
        Calculates a crc for the supplied command, also see c-code variant
        https://forums.aeva.asn.au/viewtopic.php?title=pip4048ms-inverter&p=53760&t=4332#p53760
        :param command: The command that requires a crc to be calculated
        :return: CRC for the given command
        """
        checksum: int = 0x0
        for character in command:
            t_da = c_uint8(checksum >> 8)
            da = t_da.value >> 4
            checksum <<= 4
            index = da ^ (ord(character) >> 4)
            checksum ^= self.__crc_lookup[index]
            t_da = c_uint8(checksum >> 8)
            da = t_da.value >> 4
            checksum <<= 4
            index = da ^ (ord(character) & 0x0f)
            checksum ^= self.__crc_lookup[index]

        crc = self.__create_crc(checksum)

        self._logger.debug(
            f'COMMAND: {command} -> CRC_HIGH: {crc.crc_high} CRC_LOW: {crc.crc_low} | FULL_CRC: {crc.crc_full}'
        )
        return crc

    def command_with_crc(self, command: str) -> Command:
        """
        Command with CRC wrapped in a command object
        :param command: The command that requires a crc to be calculated
        :return: Command
        """
        crc = self.calculate_crc(command)
        return Command(command=command, crc=crc)
