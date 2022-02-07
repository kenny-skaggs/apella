from collections.abc import Callable
from typing import List, Optional, TypeVar

from curriculum import models, view_models
from tool_kit.external import DatabaseConnection
from sqlalchemy.orm import Session

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
        if not db_course:
            db_course = models.Course(name=course.name)
            session.add(db_course)

        db_course.name = course.name

        session.flush()
        return db_course.id


class UnitRepository:
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
        if not db_unit:
            db_unit = models.Unit(course_id=unit.course_id)
            session.add(db_unit)

        db_unit.name = unit.name

        session.flush()
        return db_unit.id


class LessonRepository:
    @classmethod
    @_needs_session
    def get_by_id(cls, _id, session):
        lesson = session.query(models.Lesson).get(_id)
        return view_models.Lesson(
            id=lesson.id,
            name=lesson.name,
            pages=[
                view_models.Page(id=page.id, name=page.name, html=page.html)
                for page in lesson.pages
            ]
        )

    @classmethod
    @_needs_session
    def upsert(cls, lesson: view_models.Lesson, session):
        db_lesson = session.query(models.Lesson).get(lesson.id)
        if not db_lesson:
            db_lesson = models.Lesson(unit_id=lesson.unit_id)
            session.add(db_lesson)

        db_lesson.name = lesson.name

        session.flush()
        return db_lesson.id


class PageRepository:
    @classmethod
    @_needs_session
    def upsert(cls, page: view_models.Page, session):
        db_page = session.query(models.Page).get(page.id)
        if not db_page:
            db_page = models.Page(lesson_id=page.lesson_id)
            session.add(db_page)

        db_page.name = page.name
        db_page.html = page.html

        session.flush()
        return view_models.Page(id=db_page.id, name=db_page.name, html=db_page.html)


class QuestionRepository:
    @classmethod
    @_needs_session
    def upsert(cls, question: view_models.Question, session):
        db_question = session.query(models.Question).get(question.id)
        if not db_question:
            db_question = models.Question(page_id=question.page_id, type=question.type)
            session.add(db_question)

        db_question.options = []
        for option_data in (question.options or []):
            db_question.options.append(models.Option(text=option_data.text))

        session.flush()
        return view_models.Question(
            id=db_question.id,
            options=[
                view_models.Option(id=option.id, text=option.text)
                for option in (db_question.options or [])
            ],
            type=question.type
        )
