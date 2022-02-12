
from flask import Blueprint, request
from flask_restful import Api, Resource

import auth
from general import repository
from general import model


class Users(Resource):
    @classmethod
    @auth.requires_login
    def get(cls):
        return [user.to_dict() for user in repository.UserRepository.get_all_users()]

    @classmethod
    def post(cls, user_id=None):
        json = request.json
        user = model.User(
            id=user_id,
            username=json['username']
        )
        return repository.UserRepository.upsert(user).to_dict()


blueprint = Blueprint('general', __name__)

api = Api(blueprint)
api.add_resource(Users, '/users')
