from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DeviceConfiguration:
    connections: Optional[str]
    identifiers: List[str]
    name: str
    manufacturer: str
    model: str
    sw_version: str
