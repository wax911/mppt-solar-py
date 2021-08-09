from dataclasses import dataclass
from typing import Optional, Dict, List, Union


@dataclass
class Crc:
    crc_high: int
    crc_low: int

    @property
    def crc_full(self) -> int:
        crc_full = self.crc_high << 8
        crc_full += self.crc_low
        return crc_full

    def __str__(self) -> str:
        return f'{chr(self.crc_high)}{chr(self.crc_low)}'


@dataclass
class Command:
    command: str
    is_query: bool = True
    crc: Optional[Crc] = None

    # noinspection PyTypeChecker
    def __str__(self) -> str:
        return f'{self.command}{self.crc}\x0d'


@dataclass
class CommandValidation:
    input_rule: Optional[str]
    output_rule: Optional[str]


@dataclass
class CommandSpecification:
    type: Optional[str]
    description: Optional[str]
    payload_definition: Union[str, List[str], Dict]


@dataclass
class CommandDefinition:
    specifications: List[CommandSpecification]
    validation: CommandValidation


@dataclass
class CommandResponse:
    raw: Optional[str]
    name: str
    description: str
    command: Command
    definition: CommandDefinition
