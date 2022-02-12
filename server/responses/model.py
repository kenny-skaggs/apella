from dataclasses import dataclass
from typing import List

from core import Serializable


@dataclass
class Answer(Serializable):
    user_id: int
    question_id: int
    id: int = None
    selected_option_ids: List[int] = None
    text: str = None
