
from flask import Blueprint, request
from flask_restful import Api, Resource

import auth
from core import Role
from responses import repository, service


class Responses(Resource):
    @classmethod
    @auth.requires_roles(Role.TEACHER)
    def get(cls, page_id):
        responses = repository.AnswerRepository.answers_for_page(page_id)
        return {
            question_id: [answer.to_dict() for answer in answer_list]
            for question_id, answer_list in responses.items()
        }


class ResponseLockManagement(Resource):
    @classmethod
    @auth.requires_roles(Role.TEACHER)
    def post(cls):
        json = request.json
        repository.AnswerRepository.updateResponseLock(
            response_id=json['responseId'],
            locked=json['locked']
        )
        return 200


class GradeRubricItem(Resource):
    @classmethod
    @auth.requires_roles(Role.TEACHER)
    def post(cls, rubric_item_id, answer_id):
        json = request.json
        rubric_grade = service.rubric_item_graded(
            answer_id=answer_id,
            rubric_item_id=rubric_item_id,
            grade=json.get("grade")
        )
        return rubric_grade.to_dict()


blueprint = Blueprint('responses', __name__)

api = Api(blueprint)
api.add_resource(Responses, '/<int:page_id>')
api.add_resource(ResponseLockManagement, '/lock')
api.add_resource(GradeRubricItem, '/answer/<int:answer_id>/grade-rubric-item/<int:rubric_item_id>')
