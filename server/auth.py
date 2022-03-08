from typing import List, Optional

from flask import Blueprint, request
import flask_praetorian
from flask_restful import Api, Resource

from general import repository, model

guard = flask_praetorian.Praetorian()


requires_login = flask_praetorian.auth_required
requires_roles = flask_praetorian.roles_required

get_current_user = flask_praetorian.current_user


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
        user: model.User = repository.UserRepository.get_with_username(username)
        return cls._from_model(user)

    @classmethod
    def identify(cls, id_) -> Optional['User']:
        """One or none that looks up a user based on their id number"""
        user: model.User = repository.UserRepository.get_with_id(id_, populate_roles=True)
        return cls._from_model(user)

    @classmethod
    def _from_model(cls, user: model.User):
        return User(
            identity=user.id,
            username=user.username,
            hashed_password=user.password,
            roles=user.roles
        )


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
