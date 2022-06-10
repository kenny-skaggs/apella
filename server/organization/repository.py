from typing import Optional, Sequence

from sqlalchemy.orm import Session

from core import needs_session
from general import model as general_view_models
from organization import schema, model


class ClassRepository:
    @classmethod
    @needs_session
    def get_class(cls, class_id, session: Session):
        db_class = session.query(schema.Class).filter(schema.Class.id == class_id).one_or_none()
        return db_class.to_model(with_students=True)

    @classmethod
    @needs_session
    def get_classes_taught_by_user(cls, user_id, session: Session):
        db_classes: Sequence[schema.Class] = session.query(schema.Class).join(schema.TeacherClass).filter(
            schema.TeacherClass.user_id == user_id
        ).all()
        return [
            db_class.to_model(with_students=True, with_courses=True)
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

        db_class.course_refs = [
            schema.ClassCourse(course_id=course.id)
            for course in apella_class.course_list
        ]

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


class LessonClassRepository:
    @classmethod
    @needs_session
    def set_lesson_visibility(cls, lesson_id, class_id, visibility, session: Session):
        lesson_class_query = session.query(schema.LessonClass).filter(
            schema.LessonClass.lesson_id == lesson_id,
            schema.LessonClass.class_id == class_id
        )
        if lesson_class_query.exists():
            print('updating what was found')
            lesson_class_query.update({
                schema.LessonClass.is_visible: visibility
            })
        else:
            print('creating new')
            session.add(schema.LessonClass(
                lesson_id=lesson_id,
                class_id=class_id,
                is_visible=visibility
            ))



class SchoolRepository:
    @classmethod
    @needs_session
    def load_school(cls, school_id, session: Session) -> Optional[model.School]:
        result = session.query(
            schema.School
        ).filter(
            schema.School.id == school_id
        ).one_or_none()
        if result is None:
            return None
        else:
            return result.to_model(with_courses=True, with_teachers=True)

    @classmethod
    @needs_session
    def list_schools(cls, session: Session) -> Sequence[model.School]:
        results = session.query(schema.School).all()
        return [db_school.to_model() for db_school in results]

    @classmethod
    @needs_session
    def upsert(cls, school_model: model.School, session: Session) -> model.School:
        db_school = session.query(schema.School).get(school_model.id)
        if not db_school:
            db_school = schema.School()
            session.add(db_school)

        db_school.name = school_model.name

        session.flush()
        return db_school.to_model()

    @classmethod
    @needs_session
    def link_course(cls, school_id, course_id, session: Session):
        session.add(schema.SchoolCourse(
            school_id=school_id,
            course_id=course_id
        ))

    @classmethod
    @needs_session
    def unlink_course(cls, school_id, course_id, session: Session):
        session.query(
            schema.SchoolCourse
        ).filter(
            schema.SchoolCourse.school_id == school_id,
            schema.SchoolCourse.course_id == course_id
        ).delete()

    @classmethod
    @needs_session
    def link_user(cls, school_id, user_id, session: Session):
        session.add(schema.SchoolUser(
            school_id=school_id,
            user_id=user_id
        ))

    @classmethod
    @needs_session
    def unlink_user(cls, school_id, user_id, session: Session):
        session.query(
            schema.SchoolUser
        ).filter(
            schema.SchoolUser.school_id == school_id,
            schema.SchoolUser.user_id == user_id
        ).delete()
