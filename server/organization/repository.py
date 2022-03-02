from typing import Sequence

from sqlalchemy.orm import Session

from core import needs_session
from general import model as general_view_models
from organization import schema, model


class ClassRepository:
    @classmethod
    @needs_session
    def get_classes_taught_by_user(cls, user_id, session: Session):
        db_classes: Sequence[schema.Class] = session.query(schema.Class).join(schema.TeacherClass).filter(
            schema.TeacherClass.user_id == user_id
        ).all()
        return [
            db_class.to_model(with_students=True)
            for db_class in db_classes
        ]

    @classmethod
    @needs_session
    def upsert(cls, apella_class: model.Class, teacher_id: int, session: Session):
        db_class = session.query(schema.Class).get(apella_class.id)
        if not db_class:
            db_class = schema.Class()
            session.add(db_class)

            TeacherClassRepository.assign_teacher_to_class(
                teacher_id=teacher_id,
                apella_class=db_class,
                session=session
            )

        db_class.name = apella_class.name

        session.flush()
        return db_class.to_model()


class TeacherClassRepository:
    @classmethod
    @needs_session
    def assign_teacher_to_class(cls, teacher_id, apella_class, session: Session):
        db_teacher_class = schema.TeacherClass(user_id=teacher_id)
        if isinstance(apella_class, schema.Class):
            db_teacher_class.cls = apella_class
        else:
            db_teacher_class.class_id = apella_class

        session.add(db_teacher_class)
        # todo: there should be a way to make sure there aren't a bunch of duplicates


class StudentClassRepository:
    @classmethod
    @needs_session
    def assign_student_to_class(cls, student_id, apella_class, session: Session):
        student_class = schema.StudentClass(user_id=student_id)
        if isinstance(apella_class, schema.Class):
            student_class.cls = apella_class
        else:
            student_class.class_id = apella_class

        session.add(student_class)
        # todo: there should be a way to make sure there aren't a bunch of duplicates
