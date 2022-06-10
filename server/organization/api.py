
from flask import Blueprint, request
from flask_restful import Api, Resource

import auth
from core import Role
import curriculum
from organization import service, repository, model


class Classes(Resource):
    @classmethod
    @auth.requires_roles(Role.TEACHER)
    def get(cls, class_id=None):
        if class_id is None:
            class_list = repository.ClassRepository.get_classes_taught_by_user(
                user_id=auth.get_current_user().identity
            )
            return [
                apella_class.to_dict()
                for apella_class in class_list
            ]
        else:
            apella_class = repository.ClassRepository.get_class(class_id)
            return apella_class.to_dict()

    @classmethod
    @auth.requires_roles(Role.TEACHER)
    def post(cls, class_id=None):
        json = request.json

        course_list = [
            curriculum.model.Course(id=course['id'])
            for course in json['course_list']
        ]
        apella_class = model.Class(
            id=class_id,
            name=json['name'],
            course_list=course_list
        )

        apella_class = repository.ClassRepository.upsert(
            apella_class=apella_class,
            teacher_id=auth.get_current_user().identity
        )
        return apella_class.to_dict(), 200


class StudentClass(Resource):
    @classmethod
    @auth.requires_roles(Role.TEACHER)
    def post(cls, class_id, student_id):
        repository.StudentClassRepository.assign_student_to_class(
            apella_class=class_id,
            student_id=student_id
        )
        return 200


class LessonClass(Resource):
    @classmethod
    @auth.requires_roles(Role.TEACHER)
    def post(cls):
        json = request.json
        repository.LessonClassRepository.set_lesson_visibility(
            lesson_id=json['lessonId'],
            class_id=json['classId'],
            visibility=json['visibility']
        )
        return 200


class SchoolApi(Resource):
    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def get(cls, school_id=None):
        if school_id is None:
            results = repository.SchoolRepository.list_schools()
            return [school.to_dict() for school in results]
        else:
            result = repository.SchoolRepository.load_school(school_id=school_id)
            return result.to_dict()

    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def post(cls):
        json = request.json
        school = repository.SchoolRepository.upsert(
            school_model=model.School(
                id=json.get('id'),
                name=json['name']
            )
        )
        return school.to_dict()


class SchoolCourseApi(Resource):
    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def post(cls):
        json = request.json
        repository.SchoolRepository.link_course(
            school_id=json['schoolId'],
            course_id=json['courseId']
        )

    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def delete(cls, school_id, course_id):
        repository.SchoolRepository.unlink_course(
            school_id=school_id,
            course_id=course_id
        )


class SchoolTeacherApi(Resource):
    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def post(cls):
        json = request.json
        repository.SchoolRepository.link_user(
            school_id=json['schoolId'],
            user_id=json['userId']
        )

    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def delete(cls, school_id, user_id):
        repository.SchoolRepository.unlink_user(
            school_id=school_id,
            user_id=user_id
        )


blueprint = Blueprint('organization', __name__)

api = Api(blueprint)
api.add_resource(Classes, '/classes', '/class/<int:class_id>')
api.add_resource(StudentClass, '/class/<int:class_id>/student/<int:student_id>')
api.add_resource(SchoolApi, '/schools', '/school/<int:school_id>')
api.add_resource(SchoolCourseApi, '/school-course', '/school/<int:school_id>/course/<int:course_id>')
api.add_resource(SchoolTeacherApi, '/school-teacher', '/school/<int:school_id>/teacher/<int:user_id>')
