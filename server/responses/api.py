
from flask import Blueprint, request
from flask_restful import Api, Resource

import auth
from responses import model, repository


class Responses(Resource):
    @classmethod
    @auth.requires_login
    def get(cls, page_id):
        responses = repository.AnswerRepository.answers_for_page(page_id)
        return {
            question_id: [answer.to_dict() for answer in answer_list]
            for question_id, answer_list in responses.items()
        }


blueprint = Blueprint('responses', __name__)

api = Api(blueprint)
api.add_resource(Responses, '/<int:page_id>')
