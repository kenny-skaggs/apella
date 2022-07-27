from datetime import datetime
import os

from flask import Blueprint, redirect, request, url_for
from flask_restful import Resource
from werkzeug.utils import secure_filename

import auth
from core import Role, FlaskRestfulApi
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
        print(auth.get_current_user().identity)
        if course_id is None:
            user = auth.get_current_user()
            if 'author' in user.rolenames:
                course_list = repository.CourseRepository.get_all()
            elif 'teacher' in user.rolenames:
                course_list = repository.CourseRepository.courses_taught_by_user(user_id=user.identity)
            else:
                course_list = repository.CourseRepository.courses_enrolled_for_user(user_id=user.identity)

            return [course.to_dict() for course in course_list]
        else:
            return repository.CourseRepository.get_by_id(course_id).to_dict()

    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def post(cls):
        json = request.json
        course_data = model.Course(
            id=json.get('id'),
            name=json['name']
        )
        course_id = repository.CourseRepository.upsert(course_data)
        return course_id, 200


class PdCourses(Resource):
    @classmethod
    @auth.requires_login
    @auth.allowed_roles(Role.AUTHOR, Role.TEACHER)
    def get(cls):
        user = auth.get_current_user()
        course_list = repository.CourseRepository.courses_enrolled_for_user(user_id=user.identity)

        return [course.to_dict() for course in course_list]


class Units(Resource):
    @auth.requires_login
    def get(self, unit_id):
        return repository.UnitRepository.get_by_id(unit_id).to_dict()

    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def post(cls):
        json = request.json
        unit_data = model.Unit(
            id=json.get('id'),
            name=json['name'],
            course_id=json['course_id'],
            resources=model.Resource.list_from_json(json['resources'])
        )
        unit_id = repository.UnitRepository.upsert(unit_data)
        return unit_id, 200


class LessonOrder(Resource):
    @classmethod
    @auth.requires_roles(Role.AUTHOR)
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
            if request.args.get('teacher_view'):
                render_target = RenderTarget.TEACHING
            else:
                render_target = RenderTarget.AUTHORING
        elif 'teacher' in user.rolenames:
            if request.args.get('student_view'):
                render_target = RenderTarget.RESPONDING
            else:
                render_target = RenderTarget.TEACHING
        else:
            render_target = RenderTarget.RESPONDING
        lesson_renderer = LessonRenderer(render_target=render_target)
        for page in lesson_view_model.pages:
            page.html = lesson_renderer.process_html(page.html, user_id=user.identity, lesson_id=lesson_id)

        return lesson_view_model.to_dict()

    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def post(cls):
        json = request.json
        lesson_data = model.Lesson(
            id=json.get('id'),
            name=json['name'],
            unit_id=json['unit_id'],
            resources=model.Resource.list_from_json(json['resources'])
        )
        unit_id = repository.LessonRepository.upsert(lesson_data)
        return unit_id, 200


class PageOrder(Resource):
    @classmethod
    @auth.requires_roles(Role.AUTHOR)
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

    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def delete(cls, page_id):
        repository.PageRepository.delete(page_id)
        return 200


class FileUpload(Resource):
    @classmethod
    def _is_allowed_file(cls, file_name):
        return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in [
            'png', 'jpeg', 'jpg', 'gif'
        ]

    @classmethod
    @auth.requires_roles('author')
    def post(cls):
        if 'fileToUpload' not in request.files:
            print('not found')
            return {'success': False}

        file = request.files['fileToUpload']
        if file.filename == '':
            print('no name')
            return {'success': False}

        if file and cls._is_allowed_file(file.filename):
            filename = f'{int(datetime.utcnow().timestamp())}.{secure_filename(file.filename)}'
            save_path = os.path.join('static', os.environ['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            # TODO: match the current platform image path so existing html works

            return {
                'success': True,
                'file': url_for('static', filename=os.path.join(os.environ['UPLOAD_FOLDER'], filename), _external=True)
            }

        return {
            'success': True,
            'file': 'https://images.unsplash.com/photo-1595433707802-6b2626ef1c91?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8&w=1000&q=80'
        }, 200


blueprint = Blueprint('curriculum', __name__)

api = FlaskRestfulApi(blueprint)
api.add_resource(Courses, '/courses', '/course/<int:course_id>')
api.add_resource(PdCourses, '/pd-courses')

api.add_resource(Units, '/units', '/unit/<int:unit_id>')
api.add_resource(LessonOrder, '/unit/order/<int:unit_id>')

api.add_resource(Lessons, '/lessons', '/lesson/<int:lesson_id>')
api.add_resource(PageOrder, '/lesson/order/<int:lesson_id>')

api.add_resource(Pages, '/pages', '/page/<int:page_id>')

api.add_resource(FileUpload, '/file-upload')
