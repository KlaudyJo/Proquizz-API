from flask_restful import Resource
from flask import request
from models.user import UserModel
from resources.marsh import UserSchema


class UserRegister(Resource):

    def post(self):
        json_data = request.get_json()
        user_schema = UserSchema()
        data = user_schema.load(json_data)
        

        if UserModel.find_by_name(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201