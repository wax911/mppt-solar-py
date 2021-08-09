from dataclasses import dataclass


@dataclass
class DeviceInfo:
    model: str
    device_name: str
    manufacturer: str
    firmware_version: str
    serial_number: str
    protocol_id: str

    def __iter__(self):
        yield 'model', self.model
        yield 'device_name', self.device_name
        yield 'manufacturer', self.manufacturer
        yield 'firmware_version', self.firmware_version
        yield 'serial_number', self.serial_number
        yield 'protocol_id', self.protocol_id

    def __str__(self) -> str:
        return f'{self.device_name} | {self.model} -> {self.firmware_version}'
