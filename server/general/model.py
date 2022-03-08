from dataclasses import dataclass
from enum import Enum
from typing import List

from core import Serializable


class Role(Enum):
    AUTHOR = 1
    TEACHER = 2
    STUDENT = 3


@dataclass
class User(Serializable):
    id: int
    username: str
    password: str = None
    roles: List[str] = None
