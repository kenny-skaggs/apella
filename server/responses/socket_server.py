
from flask import Flask
from flask_socketio import SocketIO, emit

import auth
from responses import service as responses_service


def initialize_server(app: Flask) -> SocketIO:
    server = SocketIO(app, cors_allowed_origins='*')

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
            emit('newResponse', answer.to_dict(), broadcast=True)
        # TODO: have responses only go to subscribed teacher connections

    return server
