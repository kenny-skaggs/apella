import os

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_praetorian.constants import DEFAULT_JWT_PLACES

import auth
from curriculum import api as curriculum_api
from responses import api as responses_api, socket_server
from general import api as general_api
from organization import api as organization_api


app = Flask(__name__)
CORS(app)
socket_io = socket_server.initialize_server(app)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
app.config['JWT_PLACES'] = [*DEFAULT_JWT_PLACES, 'self']

auth.guard.init_app(app, auth.User)

app.jinja_env.globals.update(
    chr=chr
)


app.register_blueprint(auth.blueprint)
app.register_blueprint(curriculum_api.blueprint, url_prefix='/curriculum')
app.register_blueprint(general_api.blueprint)
app.register_blueprint(organization_api.blueprint, url_prefix='/organization')
app.register_blueprint(responses_api.blueprint, url_prefix='/responses')


if __name__ == '__main__':
    socket_io.run(app, debug=True)
