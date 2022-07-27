
from flask import Blueprint, request, send_from_directory
from flask_restful import Api, Resource
from google.auth.transport import requests
from google.oauth2 import id_token
from werkzeug.exceptions import BadRequest, NotFound

import auth
from core import Role
from general import repository
from general import model
from organization import repository as organization_repository


class Index(Resource):
    @classmethod
    def get(cls):
        return send_from_directory('.', 'index.html')


class CssHandler(Resource):
    @classmethod
    def get(cls, file_name):
        return send_from_directory('static/css', file_name)


class ImgHandler(Resource):
    @classmethod
    def get(cls, file_name):
        return send_from_directory('static/img', file_name)


class LessonImgHandler(Resource):
    @classmethod
    def get(cls, file_name):
        return send_from_directory('static/lesson_images', file_name)


class FontsHandler(Resource):
    @classmethod
    def get(cls, file_name):
        return send_from_directory('static/fonts', file_name)


class JsHandler(Resource):
    @classmethod
    def get(cls, file_name):
        return send_from_directory('static/js', file_name)


class Users(Resource):
    @classmethod
    @auth.requires_login
    def get(cls):
        user = auth.get_current_user()
        if 'student' in user.rolenames:
            return 404
        elif 'author' in user.rolenames:
            return [
                user.to_dict() for user in
                repository.UserRepository.get_all_users(role_filter=Role.TEACHER)
            ]
        elif 'teacher' in user.rolenames:
            return [
                user.to_dict() for user in
                repository.UserRepository.get_students_in_school_with_teacher(teacher_user_id=user.identity)
            ]

    @classmethod
    @auth.requires_roles(Role.TEACHER)
    def post(cls, request_user_id=None):
        # creating students

        # get the teacher's school, if there are more than one then throw an error
        # todo: implement multi-school teacher functionality for adding students
        user = auth.get_current_user()
        teacher_school = organization_repository.SchoolRepository.school_for_user(
            user_id=user.identity
        )

        json = request.json
        user = model.User(
            id=request_user_id or json.get('id'),
            username=json.get('username'),
            email=json.get('email'),
            first_name=json.get('first_name'),
            last_name=json.get('last_name'),
            roles=['student']
        )
        if 'password' in json:
            user.password = auth.guard.hash_password(json.get('password'))
        upserted_user = repository.UserRepository.upsert(user).to_dict()

        if request_user_id is None:
            organization_repository.SchoolRepository.link_user(
                user_id=upserted_user['id'],
                school_id=teacher_school.id
            )

        return upserted_user


class TeacherSearch(Resource):
    @classmethod
    @auth.requires_roles(Role.AUTHOR)
    def get(cls, search_text):
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


class GoogleLoginCallback(Resource):
    @classmethod
    def post(cls):
        # csrf_token_cookie = request.cookies.get('g_csrf_token')
        # if not csrf_token_cookie:
        #     raise BadRequest('No CSRF token in Cookie.')
        # csrf_token_body = request.form['g_csrf_token']
        # if not csrf_token_body:
        #     raise BadRequest('No CSRF token in post body.')
        # if csrf_token_cookie != csrf_token_body:
        #     raise BadRequest('Failed to verify double submit cookie.')

        token = request.json['token']
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), auth.GOOGLE_CLIENT_ID)

        if idinfo.get('email_verified'):
            email = idinfo['email']
            user_model = repository.UserRepository.get_with_email(email=email)
            if user_model is None:
                raise NotFound('Account with email not found')
            else:
                return auth.get_auth_success_response(auth.User.from_model(user_model))

        else:
            # todo: record that email is not verified
            raise BadRequest('Email not verified')


blueprint = Blueprint('general', __name__)

api = Api(blueprint)
api.add_resource(Users, '/users')
api.add_resource(TeacherSearch, '/teacher-search/<string:search_text>')
api.add_resource(AddTeacherAccount, '/new-teacher')
api.add_resource(GoogleLoginCallback, '/google-login')
api.add_resource(Index, '/')
api.add_resource(CssHandler, '/css/<string:file_name>')
api.add_resource(JsHandler, '/js/<string:file_name>')
api.add_resource(FontsHandler, '/fonts/<string:file_name>')
api.add_resource(ImgHandler, '/img/<string:file_name>')
api.add_resource(LessonImgHandler, '/lesson_images/<string:file_name>')

