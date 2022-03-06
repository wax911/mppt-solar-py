from dataclasses import dataclass
from typing import Optional


@dataclass
class Payload:
    name: str
    state_topic: Optional[str]


@dataclass
class SensorPayload(Payload):
    device_class: str
    value_template: str
    unit_of_measurement: str


@dataclass
class SwitchPayload(Payload):
    command_topic: Optional[str]
    value_template: str
