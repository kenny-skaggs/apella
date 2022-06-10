from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from core import Serializable


@dataclass
class Course(Serializable):
    id: int
    name: str = None
    units: List['Unit'] = None


@dataclass
class Unit(Serializable):
    id: int
    name: str
    course_id: int = None
    lessons: List['Lesson'] = None
    resources: List['Resource'] = None


@dataclass
class Lesson(Serializable):
    id: int
    name: str
    unit_id: int = None
    pages: List['Page'] = None
    resources: List['Resource'] = None


@dataclass
class Page(Serializable):
    id: int
    name: str
    lesson_id: int = None
    html: str = ''
    position: int = None


class QuestionType(Enum):
    INLINE_TEXT = 1
    INLINE_DROPDOWN = 2
    PARAGRAPH = 3
    CHOICE = 4
    RUBRIC = 5


@dataclass
class Question(Serializable):
    id: int
    type: QuestionType
    options: List['Option'] = None
    rubric_items: List['RubricItem'] = None
    page_id: int = None


@dataclass
class Option(Serializable):
    id: Optional[int]
    text: str


@dataclass
class RubricItem(Serializable):
    id: Optional[int]
    text: str
    points: int


@dataclass
class Resource(Serializable):
    id: Optional[int]
    name: str
    link: str

    @classmethod
    def from_json(cls, json):
        return Resource(
            id=json.get('id'),
            name=json['name'],
            link=json['link']
        )

    @classmethod
    def list_from_json(cls, json_list):
        return [Resource.from_json(resource_json) for resource_json in json_list]

