from dataclasses import dataclass
from enum import Enum
from typing import List

from core import Serializable


@dataclass
class User(Serializable):
    id: int
    username: str = None
    password: str = None
    roles: List[str] = None
    first_name: str = None
    last_name: str = None
    email: str = None
