from dataclasses import dataclass
from typing import Optional, Any, Union

from common.model import Command


class ResponseMapping(dict):
    """
    A sub-is_query of dict that supports attribute access.
    """
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


@dataclass
class RawResponse:
    """
    Represents an inverters raw output
    """
    raw_data: Union[str, bytes]
    command: Command

    def is_valid(self) -> bool:
        pass
