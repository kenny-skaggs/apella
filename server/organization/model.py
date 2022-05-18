from dataclasses import dataclass, field
from typing import List

from core import Serializable
from curriculum import model as curriculum_model
from general import model as general_view_models


@dataclass
class Class(Serializable):
    id: int
    name: str
    students: List[general_view_models.User] = field(default_factory=list)


@dataclass
class School(Serializable):
    id: int
    name: str
    courses: List[curriculum_model.Course] = None
    teachers: List[general_view_models.User] = None
