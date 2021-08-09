from textwrap import wrap
from unittest import TestCase

from common.model import Crc, Command
from di.dependencies import CrcProvider
from processor.helper import CyclicRedundancyCodeHelper


class TestCyclicRedundancyCodeHelper(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._crc_helper: CyclicRedundancyCodeHelper = CrcProvider.crc_ioc()

    def test_calculate_crc(self):
        given = 'QPI'  # 0x51 0x50 0x49
        expect = 0xBEAC  # CRC of `given` should result in 48812 decimal value
        actual = self._crc_helper.calculate_crc(given).crc_full
        self.assertEqual(expect, actual)

    def test_command_with_crc(self):
        given_command = 'QPI'  # 0x51 0x50 0x49
        given_crc = Crc(
            crc_high=0xBE,
            crc_low=0xAC
        )  # CRC of `given_command` should result in crc_high=0xBE and crc_low=0xAC
        expected = Command(
            command=given_command,
            crc=given_crc
        )
        actual = self._crc_helper.command_with_crc('QPI')
        self.assertEqual(expected, actual)
