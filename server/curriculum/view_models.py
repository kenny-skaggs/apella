from dataclasses import dataclass
from typing import List, Optional

from curriculum import models


class _Serializable:
    def to_dict(self):
        result = self.__dict__
        for field_name, value in result.items():
            if isinstance(value, list):
                result[field_name] = [item.to_dict() for item in value]
        return result


@dataclass
class Course(_Serializable):
    id: int
    name: str
    units: List['Unit'] = None


@dataclass
class Unit(_Serializable):
    id: int
    name: str
    course_id: int = None
    lessons: List['Lesson'] = None


@dataclass
class Lesson(_Serializable):
    id: int
    name: str
    unit_id: int = None
    pages: List['Page'] = None


@dataclass
class Page(_Serializable):
    id: int
    name: str
    lesson_id: int = None
    html: str = ''


@dataclass
class Question(_Serializable):
    id: int
    type: models.QuestionType
    options: List['Option'] = None
    page_id: int = None


@dataclass
class Option(_Serializable):
    id: Optional[int]
    text: str
