
from flask import Blueprint, request
from flask_restful import Api, Resource

import auth
from core import Role
from organization import service, repository, model


class Classes(Resource):
    @classmethod
    @auth.requires_roles(Role.TEACHER)
    def get(cls, class_id=None):
        if class_id is None:
            return [
                apella_class.to_dict()
                for apella_class in repository.ClassRepository.get_classes_taught_by_user(
                    user_id=auth.get_current_user().identity
                )
            ]
        else:
            apella_class = repository.ClassRepository.get_class(class_id)
            return apella_class.to_dict()

    @classmethod
    @auth.requires_roles(Role.TEACHER)
    def post(cls, class_id=None):
        json = request.json
        apella_class = model.Class(
            id=class_id,
            name=json['name']
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


blueprint = Blueprint('organization', __name__)

api = Api(blueprint)
api.add_resource(Classes, '/classes', '/class/<int:class_id>')
api.add_resource(StudentClass, '/class/<int:class_id>/student/<int:student_id>')
