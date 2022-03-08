
from flask import Blueprint, request
from flask_restful import Api, Resource

import auth
from curriculum import service, model, repository
from curriculum.html_processing import LessonRenderer, RenderTarget


class OrderUpdateApi(Resource):
    def __init__(self, repository_method):
        self.updated_method = repository_method

    def post(self, container_id):
        json = request.json
        self.updated_method(container_id, json['orderedIds'])
        return 'done', 200


class Courses(Resource):
    @classmethod
    @auth.requires_login
    def get(cls, course_id=None):
        if course_id is None:
            return [course.to_dict() for course in repository.CourseRepository.get_all()]
        else:
            return repository.CourseRepository.get_by_id(course_id).to_dict()

    @classmethod
    @auth.requires_roles('author')
    def post(cls):
        json = request.json
        course_data = model.Course(
            id=json.get('id'),
            name=json['name']
        )
        course_id = repository.CourseRepository.upsert(course_data)
        return course_id, 200


class Units(Resource):
    @auth.requires_login
    def get(self, unit_id):
        return repository.UnitRepository.get_by_id(unit_id).to_dict()

    @classmethod
    @auth.requires_login
    def post(cls):
        json = request.json
        unit_data = model.Unit(
            id=json.get('id'),
            name=json['name'],
            course_id=json['course_id']
        )
        unit_id = repository.UnitRepository.upsert(unit_data)
        return unit_id, 200


class LessonOrder(Resource):
    @classmethod
    def post(cls, unit_id):
        json = request.json
        repository.UnitRepository.set_lesson_order(unit_id, json['lessonIds'])
        return 'done', 200


class Lessons(Resource):
    @classmethod
    @auth.requires_login
    def get(cls, lesson_id):
        lesson_view_model = repository.LessonRepository.get_by_id(lesson_id)

        user = auth.get_current_user()
        if 'author' in user.rolenames:
            render_target = RenderTarget.AUTHORING
        elif 'teacher' in user.rolenames:
            render_target = RenderTarget.TEACHING
        else:
            render_target = RenderTarget.RESPONDING
        lesson_renderer = LessonRenderer(render_target=render_target)
        for page in lesson_view_model.pages:
            page.html = lesson_renderer.process_html(page.html, user_id=user.identity, lesson_id=lesson_id)

        return lesson_view_model.to_dict()

    @classmethod
    @auth.requires_login
    def post(cls):
        json = request.json
        lesson_data = model.Lesson(
            id=json.get('id'),
            name=json['name'],
            unit_id=json['unit_id']
        )
        unit_id = repository.LessonRepository.upsert(lesson_data)
        return unit_id, 200


class PageOrder(Resource):
    @classmethod
    def post(cls, lesson_id):
        json = request.json
        repository.LessonRepository.set_page_order(lesson_id, json['pageIds'])
        return 'done', 200


class Pages(Resource):
    @classmethod
    @auth.requires_roles('author')
    def post(cls):
        json = request.json
        page_data = model.Page(
            id=json.get('id'),
            name=json['name'],
            lesson_id=json['lesson_id'],
            html=json['html']
        )
        page_id, id_resolution = service.store_page(page_data)
        return {
            'page_id': page_id,
            'id_resolution': id_resolution
        }, 200


blueprint = Blueprint('curriculum', __name__)

api = Api(blueprint)
api.add_resource(Courses, '/courses', '/course/<int:course_id>')

api.add_resource(Units, '/units', '/unit/<int:unit_id>')
api.add_resource(LessonOrder, '/unit/order/<int:unit_id>')

api.add_resource(Lessons, '/lessons', '/lesson/<int:lesson_id>')
api.add_resource(PageOrder, '/lesson/order/<int:lesson_id>')

api.add_resource(Pages, '/pages')
