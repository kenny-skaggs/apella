from dataclasses import dataclass
from typing import List


@dataclass
class Course:
    id: int
    name: str
    units: List['Unit'] = None

    def to_dict(self):
        result = self.__dict__
        if self.units:
            result['units'] = [unit.to_dict() for unit in self.units]
        return result


@dataclass
class Unit:
    id: int
    name: str
    course_id: int = None
    lessons: List['Lesson'] = None

    def to_dict(self):
        result = self.__dict__
        if self.lessons:
            result['lessons'] = [lesson.to_dict() for lesson in self.lessons]
        return result


@dataclass
class Lesson:
    id: int
    name: str
    unit_id: int = None

    def to_dict(self):
        result = self.__dict__
        return result
