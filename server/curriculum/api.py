
from flask import Blueprint, request
from flask_restful import Api, Resource

from curriculum import view_models
from storage import repository


class Courses(Resource):
    @classmethod
    def get(cls, course_id=None):
        if course_id is None:
            return [course.to_dict() for course in repository.CourseRepository.get_all()]
        else:
            return repository.CourseRepository.get_by_id(course_id).to_dict()

    @classmethod
    def post(cls):
        json = request.json
        course_data = view_models.Course(
            id=json.get('id'),
            name=json['name']
        )
        course_id = repository.CourseRepository.upsert(course_data)
        return course_id, 200


class Units(Resource):
    def get(self, unit_id):
        return repository.UnitRepository.get_by_id(unit_id).to_dict()

    @classmethod
    def post(cls):
        json = request.json
        unit_data = view_models.Unit(
            id=json.get('id'),
            name=json['name'],
            course_id=json['course_id']
        )
        unit_id = repository.UnitRepository.upsert(unit_data)
        return unit_id, 200


class Lessons(Resource):
    @classmethod
    def post(cls):
        json = request.json
        lesson_data = view_models.Lesson(
            id=json.get('id'),
            name=json['name'],
            unit_id=json['unit_id']
        )
        unit_id = repository.LessonRepository.upsert(lesson_data)
        return unit_id, 200


blueprint = Blueprint('curriculum', __name__)

api = Api(blueprint)
api.add_resource(Courses, '/courses', '/course/<int:course_id>')
api.add_resource(Units, '/units', '/unit/<int:unit_id>')
api.add_resource(Lessons, '/lessons')
