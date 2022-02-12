from dataclasses import dataclass, field
from typing import List

from core import Serializable
from general import model as general_view_models


@dataclass
class Class(Serializable):
    id: int
    name: str
    students: List[general_view_models.User] = field(default_factory=list)
