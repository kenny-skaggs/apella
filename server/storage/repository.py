from typing import List

from curriculum import models, view_models
from tool_kit.external import DatabaseConnection

_db = DatabaseConnection()


def _needs_session(func):
    def wrapper(*args, **kwargs):
        if 'session' not in kwargs:
            with _db.get_new_session() as session:
                kwargs['session'] = session
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


class CourseRepository:
    @classmethod
    @_needs_session
    def get_all(cls, session) -> List[view_models.Course]:
        db_courses = session.query(models.Course).all()
        return [
            view_models.Course(
                id=course.id,
                name=course.name
            )
            for course in db_courses]

    @classmethod
    @_needs_session
    def get_by_id(cls, _id, session) -> view_models.Course:
        course = session.query(models.Course).get(_id)
        return view_models.Course(
            id=course.id,
            name=course.name,
            units=[
                view_models.Unit(id=unit.id, name=unit.name)
                for unit in course.units
            ]
        )

    @classmethod
    @_needs_session
    def upsert(cls, course: view_models.Course, session) -> int:
        db_course = session.query(models.Course).get(course.id)
        if db_course:
            db_course.name = course.name
        else:
            db_course = models.Course(
                name=course.name
            )
            session.add(db_course)

        session.flush()
        return db_course.id


class UnitRepository:
    @classmethod
    @_needs_session
    def get_for_course(cls, course_id, session):
        db_units = session.query(models.Unit).filter(
            models.Unit.course_id == course_id
        ).all()
        return [
            view_models.Unit(id=unit.id, name=unit.name)
            for unit in db_units
        ]

    @classmethod
    @_needs_session
    def get_by_id(cls, _id, session):
        unit = session.query(models.Unit).get(_id)
        return view_models.Unit(
            id=unit.id,
            name=unit.name,
            lessons=[
                view_models.Lesson(id=lesson.id, name=lesson.name)
                for lesson in unit.lessons
            ]
        )

    @classmethod
    @_needs_session
    def upsert(cls, unit: view_models.Unit, session):
        db_unit = session.query(models.Unit).get(unit.id)
        if db_unit:
            db_unit.name = unit.name
        else:
            db_unit = models.Unit(
                name=unit.name,
                course_id=unit.course_id
            )
            session.add(db_unit)

        session.flush()
        return db_unit.id


class LessonRepository:
    @classmethod
    @_needs_session
    def get_for_unit(cls, unit_id, session):
        db_lessons = session.query(models.Lesson).filter(
            models.Lesson.unit_id == unit_id
        ).all()
        return [
            view_models.Lesson(id=lesson.id, name=lesson.name)
            for lesson in db_lessons
        ]

    @classmethod
    @_needs_session
    def upsert(cls, lesson: view_models.Lesson, session):
        db_lesson = session.query(models.Lesson).get(lesson.id)
        if db_lesson:
            db_lesson.name = lesson.name
        else:
            db_lesson = models.Lesson(
                name=lesson.name,
                unit_id=lesson.unit_id
            )
            session.add(db_lesson)

        session.flush()
        return db_lesson.id
