from typing import List, Optional

from flask import Blueprint, jsonify, request
import flask_praetorian
from flask_restful import Api, Resource

guard = flask_praetorian.Praetorian()


requires_login = flask_praetorian.auth_required
requires_roles = flask_praetorian.roles_required

get_current_user = flask_praetorian.current_user


users = []


class User:
    # flask-praetorian wants to be able to create user instances without needing to pass in values
    def __init__(self, identity: int = None, username: str = None, hashed_password: str = None, roles: List[str] = None):
        if roles is None:
            roles = []

        self.identity = identity
        self.username = username
        self.password = hashed_password
        self.rolenames = roles

    @classmethod
    def lookup(cls, username) -> Optional['User']:
        """One or none that looks up a user based on a 'username'"""
        for user in users:
            if user.username == username:
                return user

        return None

    @classmethod
    def identify(cls, id_) -> Optional['User']:
        """One or none that looks up a user based on their id number"""
        for user in users:
            if user.identity == id_:
                return user

        return None


def init_users():
    global users
    users = [
        User(identity=1, username='student', hashed_password=guard.hash_password('student'), roles=['student']),
        User(identity=2, username='teacher', hashed_password=guard.hash_password('teacher'), roles=['teacher']),
        User(identity=3, username='author', hashed_password=guard.hash_password('author'), roles=['author'])
    ]


class Login(Resource):
    @classmethod
    def post(cls):
        json = request.get_json(force=True)
        username = json.get('username', None)
        password = json.get('password', None)

        user = guard.authenticate(username, password)
        return {
            'access_token': guard.encode_jwt_token(user),
            'user': {
                'roles': user.rolenames,
                'username': user.username
            }
        }


blueprint = Blueprint('login', __name__)

api = Api(blueprint)
api.add_resource(Login, '/login')
