from dataclasses import dataclass
from typing import List, Optional

from core import Serializable
from curriculum import schema


@dataclass
class Course(Serializable):
    id: int
    name: str
    units: List['Unit'] = None


@dataclass
class Unit(Serializable):
    id: int
    name: str
    course_id: int = None
    lessons: List['Lesson'] = None


@dataclass
class Lesson(Serializable):
    id: int
    name: str
    unit_id: int = None
    pages: List['Page'] = None


@dataclass
class Page(Serializable):
    id: int
    name: str
    lesson_id: int = None
    html: str = ''


@dataclass
class Question(Serializable):
    id: int
    type: schema.QuestionType
    options: List['Option'] = None
    page_id: int = None


@dataclass
class Option(Serializable):
    id: Optional[int]
    text: str
