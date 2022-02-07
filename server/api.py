
from flask import Flask
from flask_cors import CORS

import auth
from curriculum import api as curriculum_api


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'top secret'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

auth.guard.init_app(app, auth.User)
auth.init_users()


app.register_blueprint(auth.blueprint)
app.register_blueprint(curriculum_api.blueprint, url_prefix='/curriculum')
