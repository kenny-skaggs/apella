
from flask import Blueprint, request
from flask_restful import Api, Resource

import auth
from core import Role
from general import repository
from general import model
from organization import repository as organization_repository


class Users(Resource):
    @classmethod
    @auth.requires_login
    def get(cls):
        return [user.to_dict() for user in repository.UserRepository.get_all_users()]

    @classmethod
    @auth.requires_login
    def post(cls, user_id=None):
        # TODO: check for teacher role if creating students, check for author role if creating teachers

        json = request.json
        user = model.User(
            id=user_id,
            username=json.get('username'),
            email=json.get('email'),
            first_name=json.get('firstName'),
            last_name=json.get('lastName')
        )
        return repository.UserRepository.upsert(user).to_dict()


class TeacherSearch(Resource):
    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def get(cls, search_text):
        import time
        time.sleep(2)

        return [user.to_dict() for user in repository.UserRepository.get_all_users(
            role_filter=Role.TEACHER,
            email_like_filter=search_text
        )]


class AddTeacherAccount(Resource):
    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def post(cls):
        json = request.json
        user = repository.UserRepository.upsert(
            model.User(
                id=None,
                username=json.get('username'),
                email=json.get('email'),
                first_name=json.get('firstName'),
                last_name=json.get('lastName'),
                roles=[str(Role.TEACHER)]
            )
        )

        organization_repository.SchoolRepository.link_user(
            user_id=user.id,
            school_id=json['schoolId']
        )

        return user.to_dict()


blueprint = Blueprint('general', __name__)

api = Api(blueprint)
api.add_resource(Users, '/users')
api.add_resource(TeacherSearch, '/teacher-search/<string:search_text>')
api.add_resource(AddTeacherAccount, '/new-teacher')
