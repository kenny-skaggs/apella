
from flask import Flask
from flask_socketio import SocketIO, emit, join_room

import auth
from organization import repository as organization_repository
from responses import service as responses_service


def initialize_server(app: Flask) -> SocketIO:
    server = SocketIO(app, cors_allowed_origins='*')

    # @server.on('connect')
    # @auth.load_token_from_data
    # @auth.requires_login
    # def on_connect(data):
    #     return 'bobaoeu'
    #     # todo: get authed user, if they're a teacher then get all class ids and join
    #     #  their socket to the rooms with the ids as names
    #     bob = 7 / 0
    #     user = auth.get_current_user()
    #     print(user.roles)

    @server.on('identify')
    @auth.load_token_from_data
    @auth.requires_login
    def on_identify(_):
        user = auth.get_current_user()
        if 'teacher' in user.rolenames:
            class_list = organization_repository.ClassRepository.get_classes_taught_by_user(
                user_id=user.identity
            )
            for cls in class_list:
                join_room(cls.id)

    @server.on('response_provided')
    @auth.load_token_from_data
    @auth.requires_login
    def on_response(response_data):
        user = auth.get_current_user()
        answer = responses_service.answer_provided(
            user_id=user.identity,
            question_id=response_data['questionId'],
            submitted=response_data['submitted'],
            answer=response_data['answer']
        )
        if answer.submitted:
            # TODO: have responses only go to subscribed teacher connections
            #  find all the classes that the user is in (for the given question?) and emit the response to all the
            #  rooms named after the class ids

            class_list = organization_repository.ClassRepository.get_classes_attended_by_user(
                user_id=user.identity
            )
            for cls in class_list:
                emit('newResponse', answer.to_dict(), to=cls.id)

    return server
