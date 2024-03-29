from typing import List

from sqlalchemy.orm import joinedload

from core import needs_session
from curriculum import schema, model
import organization


class CourseRepository:
    @classmethod
    @needs_session
    def get_all(cls, session) -> List[model.Course]:
        db_courses = session.query(schema.Course).all()
        return [course.to_model() for course in db_courses]

    @classmethod
    @needs_session
    def get_by_id(cls, _id, session) -> model.Course:
        course = (
            session.query(schema.Course)
            .options(
                joinedload(schema.Course.unit_refs).joinedload(schema.CourseUnit.unit)
            )
        ).get(_id)
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

    @classmethod
    @needs_session
    def courses_taught_by_user(cls, user_id, session):
        db_course_list = session.query(
            schema.Course
        ).join(
            organization.schema.SchoolCourse
        ).join(
            organization.schema.School
        ).join(
            organization.schema.SchoolUser
        ).filter(
            organization.schema.SchoolUser.user_id == user_id
        ).all()

        return [course.to_model() for course in db_course_list]

    @classmethod
    @needs_session
    def courses_enrolled_for_user(cls, user_id, session):
        db_course_list = session.query(
            schema.Course
        ).join(
            organization.schema.ClassCourse
        ).join(
            organization.schema.Class
        ).join(
            organization.schema.StudentClass
        ).filter(
            organization.schema.StudentClass.user_id == user_id
        )

        return [course.to_model() for course in db_course_list]


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
            db_unit = schema.Unit()
            db_unit.course_refs.append(
                schema.CourseUnit(course_id=unit.course_id)
            )
            session.add(db_unit)

        db_unit.name = unit.name

        db_resources = [
            schema.Resource(
                name=resource.name,
                link=resource.link
            )
            for resource in unit.resources
        ]
        db_unit.resource_refs = [
            schema.UnitResource(resource=resource)
            for resource in db_resources
        ]

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

        db_resources = [
            schema.Resource(
                name=resource.name,
                link=resource.link
            )
            for resource in lesson.resources
        ]
        db_lesson.resource_refs = [
            schema.LessonResource(resource=resource)
            for resource in db_resources
        ]

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

    @classmethod
    @needs_session
    def delete(cls, page_id, session):
        session.query(schema.Page).filter(
            schema.Page.id == page_id
        ).update({
            schema.Page.active: False
        })


class QuestionRepository:
    @classmethod
    @needs_session
    def get(cls, question_id: int, session):
        db_question = session.query(schema.Question).get(question_id)
        return db_question.to_model()

    @classmethod
    @needs_session
    def upsert(cls, question: model.Question, session):
        # todo: check if id is null before trying to load
        db_question = session.query(schema.Question).get(question.id)
        if not db_question:
            db_question = schema.Question(page_id=question.page_id, type=question.type)
            session.add(db_question)

        db_question.options = []
        for option_data in (question.options or []):
            db_question.options.append(schema.Option(text=option_data.text))

        if question.rubric_items is not None:
            uploaded_rubric_ids = [item.id for item in question.rubric_items if item.id is not None]

            to_remove = []
            for index, db_item in enumerate(db_question.rubric_items):
                if db_item.id not in uploaded_rubric_ids:
                    to_remove.append(index)
            for index_to_delete in sorted(to_remove, reverse=True):
                del db_question.rubric_items[index_to_delete]
            for item_data in question.rubric_items:
                cls._add_or_update_rubric_item(item_data, db_question)

        session.flush()
        return db_question.to_model()

    @classmethod
    def _add_or_update_rubric_item(cls, item: model.RubricItem, db_question: schema.Question):
        if item.id is None:
            db_question.rubric_items.append(
                schema.RubricItem(text=item.text, points=item.points)
            )
        else:
            for db_item in db_question.rubric_items:
                if db_item.id == item.id:
                    db_item.text = item.text
                    db_item.points = item.points
                    return

            raise Exception(f'unable to find item id {item.id} in question {db_question.id}')
