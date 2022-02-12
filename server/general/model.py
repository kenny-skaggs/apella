from dataclasses import dataclass

from core import Serializable


@dataclass
class User(Serializable):
    id: int
    username: str
    password: str = None
