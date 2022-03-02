
from typing import List

from core import needs_session
from curriculum import schema, model


class CourseRepository:
    @classmethod
    @needs_session
    def get_all(cls, session) -> List[model.Course]:
        db_courses = session.query(schema.Course).all()
        return [course.to_model() for course in db_courses]

    @classmethod
    @needs_session
    def get_by_id(cls, _id, session) -> model.Course:
        course = session.query(schema.Course).get(_id)
        return course.to_model(with_units=True)

    @classmethod
    @needs_session
    def upsert(cls, course: model.Course, session) -> int:
        db_course = session.query(schema.Course).get(course.id)
        if not db_course:
            db_course = schema.Course(name=course.name)
            session.add(db_course)

        db_course.name = course.name

        session.flush()
        return db_course.id


class UnitRepository:
    @classmethod
    @needs_session
    def get_by_id(cls, _id, session):
        unit = session.query(schema.Unit).get(_id)
        return unit.to_model(with_lessons=True)

    @classmethod
    @needs_session
    def upsert(cls, unit: model.Unit, session):
        db_unit = session.query(schema.Unit).get(unit.id)
        if not db_unit:
            db_unit = schema.Unit(course_id=unit.course_id)
            session.add(db_unit)

        db_unit.name = unit.name

        session.flush()
        return db_unit.id

    @classmethod
    @needs_session
    def set_lesson_order(cls, unit_id, ordered_lesson_ids, session):
        unit = session.query(schema.Unit).get(unit_id)

        pages = session.query(schema.Lesson).filter(schema.Lesson.id.in_(ordered_lesson_ids))
        page_id_map = {page.id: page for page in pages}

        unit.lessons = [page_id_map[id_] for id_ in ordered_lesson_ids]
        unit.lessons.reorder()


class LessonRepository:
    @classmethod
    @needs_session
    def get_by_id(cls, _id, session):
        lesson = session.query(schema.Lesson).get(_id)
        return lesson.to_model(with_pages=True)

    @classmethod
    @needs_session
    def upsert(cls, lesson: model.Lesson, session):
        db_lesson = session.query(schema.Lesson).get(lesson.id)
        if not db_lesson:
            db_lesson = schema.Lesson(unit_id=lesson.unit_id)
            session.add(db_lesson)

        db_lesson.name = lesson.name

        session.flush()
        return db_lesson.id

    @classmethod
    @needs_session
    def set_page_order(cls, lesson_id, ordered_page_ids, session):
        lesson = session.query(schema.Lesson).get(lesson_id)

        pages = session.query(schema.Page).filter(schema.Page.id.in_(ordered_page_ids))
        page_id_map = {page.id: page for page in pages}

        lesson.pages = [page_id_map[id_] for id_ in ordered_page_ids]
        lesson.pages.reorder()


class PageRepository:
    @classmethod
    @needs_session
    def upsert(cls, page: model.Page, session):
        db_page = session.query(schema.Page).get(page.id)
        if not db_page:
            db_page = schema.Page(lesson_id=page.lesson_id)
            session.add(db_page)

        db_page.name = page.name
        db_page.html = page.html

        session.flush()
        return db_page.to_model()


class QuestionRepository:
    @classmethod
    @needs_session
    def get(cls, question_id: int, session):
        db_question = session.query(schema.Question).get(question_id)
        return db_question.to_model()

    @classmethod
    @needs_session
    def upsert(cls, question: model.Question, session):
        db_question = session.query(schema.Question).get(question.id)
        if not db_question:
            db_question = schema.Question(page_id=question.page_id, type=question.type)
            session.add(db_question)

        db_question.options = []
        for option_data in (question.options or []):
            db_question.options.append(schema.Option(text=option_data.text))

        session.flush()
        return db_question.to_model()
