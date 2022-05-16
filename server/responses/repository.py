from collections import defaultdict
from typing import Optional, Sequence

from sqlalchemy.orm import Session

from core import needs_session
from curriculum import schema as curriculum_schema
from responses import schema, model


class AnswerRepository:
    @classmethod
    @needs_session
    def user_answer_map_for_lesson(cls, user_id, lesson_id, session: Session):
        answers: Sequence[schema.Answer] = (
            session.query(schema.Answer)
            .join(curriculum_schema.Question)
            .join(curriculum_schema.Page)
            .join(curriculum_schema.Lesson)
            .filter(
                curriculum_schema.Lesson.id == lesson_id,
                schema.Answer.user_id == user_id
            )
        ).all()

        return {
            answer.question_id: answer.to_model()
            for answer in answers
        }

    @classmethod
    @needs_session
    def answers_for_page(cls, page_id, session: Session):
        answers: Sequence[schema.Answer] = (
            session.query(schema.Answer)
            .join(curriculum_schema.Question)
            .join(curriculum_schema.Page)
            .filter(
                curriculum_schema.Page.id == page_id
            )
        )

        question_answer_map = defaultdict(lambda: list())
        for answer in answers:
            question_answer_map[answer.question_id].append(answer.to_model())

        return question_answer_map

    @classmethod
    @needs_session
    def upsert(cls, answer: model.Answer, session: Session):
        db_answer = session.query(schema.Answer).filter(
            schema.Answer.user_id == answer.user_id,
            schema.Answer.question_id == answer.question_id
            # TODO: this lookup will need an index
        ).one_or_none()
        if not db_answer:
            db_answer = schema.Answer(
                user_id=answer.user_id,
                question_id=answer.question_id
            )
            session.add(db_answer)

        db_answer.text = answer.text
        db_answer.option_refs = [
            schema.AnswerOption(option_id=option_id)
            for option_id in answer.selected_option_ids or []
        ]
        db_answer.locked = answer.locked
        db_answer.submitted = answer.submitted

        session.flush()
        return db_answer.to_model()

    @classmethod
    @needs_session
    def updateResponseLock(cls, response_id, locked, session: Session):
        session.query(
            schema.Answer
        ).filter(
            schema.Answer.id == response_id
        ).update({
            schema.Answer.locked: locked
        })

    @classmethod
    @needs_session
    def find_existing(cls, answer_model: model.Answer, session: Session) -> model.Answer:
        result: schema.Answer = session.query(
            schema.Answer
        ).filter(
            schema.Answer.question_id == answer_model.question_id,
            schema.Answer.user_id == answer_model.user_id
        ).one_or_none()
        return result.to_model() if result else None


class RubricGradeRepository:
    @classmethod
    @needs_session
    def upsert(cls, rubric_grade: model.RubricGrade, answer_id: int, session: Session):
        db_answer = session.query(schema.Answer).filter(schema.Answer.id == answer_id).one()

        existing_rubric_grade: Optional[schema.RubricGrade] = None
        for grade in db_answer.grades:
            if grade.rubric_item_id == rubric_grade.rubric_item_id:
                existing_rubric_grade = grade
                break

        if not existing_rubric_grade:
            existing_rubric_grade = schema.RubricGrade(
                rubric_item_id=rubric_grade.rubric_item_id
            )
            db_answer.grades.append(existing_rubric_grade)
        existing_rubric_grade.grade = rubric_grade.grade

        return existing_rubric_grade.to_model()
