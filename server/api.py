
from flask import Flask
from flask_cors import CORS

from curriculum import api as curriculum_api


app = Flask(__name__)
CORS(app)


app.register_blueprint(curriculum_api.blueprint, url_prefix='/curriculum')
