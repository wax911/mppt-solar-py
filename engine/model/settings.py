from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PluginRunTimeConfig(object):
    main: str
    tests: Optional[List[str]]


@dataclass
class DependencyModule:
    name: str
    version: str

    def __str__(self) -> str:
        return f'{self.name}>={self.version}'


@dataclass
class PluginConfig:
    name: str
    alias: str
    creator: str
    runtime: PluginRunTimeConfig
    repository: str
    description: str
    version: str
    requirements: Optional[List[DependencyModule]]
