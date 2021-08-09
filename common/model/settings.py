from dataclasses import dataclass


@dataclass
class MQTTConfig:
    topic: str
    host: str
    port: int
    username: str
    password: str


@dataclass
class DeviceConfig:
    interface: str
    baud_rate: int
    is_serial: bool


@dataclass
class Configuration:
    device: DeviceConfig
    mqtt: MQTTConfig
    verbosity: str
    plugin: str
