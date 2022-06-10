import json
import os
from typing import List, Optional

from flask import Blueprint, redirect, request
import flask_praetorian
from flask_restful import Api, Resource
from oauthlib.oauth2 import WebApplicationClient
import requests

from general import repository, model


class TokenGuard(flask_praetorian.Praetorian):
    def __init__(self, *args, **kwargs):
        super(TokenGuard, self).__init__(*args, **kwargs)
        self._token = None

    def set_token(self, token):
        self._token = token

    def read_token_from_self(self):
        flask_praetorian.exceptions.MissingToken.require_condition(
            self._token is not None,
            "JWT token not set on the guard",
        )
        return self._token


guard = TokenGuard()


def load_token_from_data(func):
    def wrapper(data):
        guard.set_token(data.get('auth'))
        print(f'found "{data.get("auth")}" as token')
        func(data)

    return wrapper


requires_login = flask_praetorian.auth_required
requires_roles = flask_praetorian.roles_required


get_current_user = flask_praetorian.current_user


GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', None)
GOOGLE_DISCOVER_URL = (
    'https://accounts.google.com/.well-known/openid-configuration'
)


google_client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVER_URL).json()


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
        return cls.from_model(user)

    @classmethod
    def identify(cls, id_) -> Optional['User']:
        """One or none that looks up a user based on their id number"""
        user: model.User = repository.UserRepository.get_with_id(id_, populate_roles=True)
        return cls.from_model(user)

    @classmethod
    def from_model(cls, user: model.User):
        return User(
            identity=user.id,
            username=user.username,
            hashed_password=user.password,
            roles=user.roles
        )


def get_auth_success_response(user):
    return {
        'access_token': guard.encode_jwt_token(user),
        'user': {
            'roles': user.rolenames,
            'username': user.username
        }
    }


class Login(Resource):
    @classmethod
    def post(cls):
        json = request.get_json(force=True)
        username = json.get('username', None)
        password = json.get('password', None)

        user = guard.authenticate(username, password)
        return get_auth_success_response(user)


blueprint = Blueprint('login', __name__)

api = Api(blueprint)
api.add_resource(Login, '/login')
