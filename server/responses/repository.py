from typing import Sequence

from sqlalchemy.orm import Session

from core import needs_session
from curriculum import models as curriculum_models
from responses import models, view_models


class AnswerRepository:
    @classmethod
    @needs_session
    def user_answer_map_for_lesson(cls, user_id, lesson_id, session: Session):
        answers: Sequence[models.Answer] = (
            session.query(models.Answer)
            .join(curriculum_models.Question)
            .join(curriculum_models.Page)
            .join(curriculum_models.Lesson)
            .filter(
                curriculum_models.Lesson.id == lesson_id,
                models.Answer.user_id == user_id
            )
        ).all()

        return {
            answer.question_id: view_models.Answer(
                id=answer.id,
                user_id=answer.user_id,
                question_id=answer.question_id,
                text=answer.text,
                selected_option_ids=[option_ref.option_id for option_ref in answer.option_refs]
            )
            for answer in answers
        }

    @classmethod
    @needs_session
    def upsert(cls, answer: view_models.Answer, session: Session):
        db_answer = session.query(models.Answer).filter(
            models.Answer.user_id == answer.user_id,
            models.Answer.question_id == answer.question_id
            # TODO: this lookup will need an index
        ).one_or_none()
        if not db_answer:
            db_answer = models.Answer(
                user_id=answer.user_id,
                question_id=answer.question_id
            )
            session.add(db_answer)

        db_answer.text = answer.text
        db_answer.option_refs = [
            models.AnswerOption(option_id=option_id)
            for option_id in answer.selected_option_ids or []
        ]

        session.flush()
        return view_models.Answer(
            id=db_answer.id,
            user_id=answer.user_id,
            question_id=answer.question_id,
            text=answer.text,
            selected_option_ids=answer.selected_option_ids
        )
