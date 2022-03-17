from dataclasses import dataclass
from enum import Enum
from typing import List

from core import Serializable


@dataclass
class User(Serializable):
    id: int
    username: str
    password: str = None
    roles: List[str] = None
