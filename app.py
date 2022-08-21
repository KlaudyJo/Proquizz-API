from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import os
from flask_cors import CORS
from resources.questions import QuestionsAll, Question
from resources.metadata import MetaData, UniqueData
from resources.user import UserRegister
from security import authenticate, identity
app = Flask(__name__)
uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resorces={r'/questions/*': {"origins": '*'}})


app.secret_key = os.environ.get('HESLO_FLASK')
api = Api(app)

jwt = JWT(app, authenticate, identity)



api.add_resource(QuestionsAll, '/questions/all')
api.add_resource(Question, '/questions')
api.add_resource(MetaData, '/questions/metadata')
api.add_resource(UniqueData, '/questions/uniques')
api.add_resource(UserRegister, '/questions/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)