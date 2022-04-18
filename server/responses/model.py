from dataclasses import dataclass
from typing import List

from core import Serializable


@dataclass
class RubricGrade(Serializable):
    rubric_item_id: int
    grade: int = None
    id: int = None


@dataclass
class Answer(Serializable):
    user_id: int
    question_id: int
    id: int = None
    selected_option_ids: List[int] = None
    text: str = None
    rubric_grades: List[RubricGrade] = None
