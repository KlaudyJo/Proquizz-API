
from .marsh import QuestionSchema
from flask_restful import Resource
from models.questions import QuestionModel
from flask import request
from flask_jwt import jwt_required

message = {'message': 'Wrong params'}
## get all questions(Resource)
class QuestionsAll(Resource):
    
    
    def get(self):
        limit =  request.args.get('limit') or 25 
        if limit:
            return {'questions': list(map(lambda x: x.return_json(), QuestionModel.get_all(limit)))}
        return message

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        question_schema = QuestionSchema()
        data = question_schema.load(json_data)
        item = QuestionModel(**data)
        print(item)
        try:
            item.save_to_db()
        except:
            return message
        return item.return_json(), 201
        
    @jwt_required()
    def put(self):
        json_data = request.get_json()
        question_schema =   QuestionSchema()
        data = question_schema.load(json_data)
        id = request.args.get('id')
        try:
            question = QuestionModel.find_by_id(id)
            if question:
                question.category = data['category']
                question.subcategory = data['subcategory']
                question.difficulty = data['difficulty']
                question.correct_answer = data['correct_answer']
                question.wrong_answers = data['wrong_answers']
                question.block_code = data['block_code']
            else: 
                question = QuestionModel(**data)
            question.save_to_db()
            return question.return_json()
        except TypeError:    
            return message, 404

    @jwt_required()
    def delete(self):
        _id = request.args.get('id')
        removed_id = QuestionModel.find_by_id(_id)
        if removed_id:
            removed_id.delete_from_db()
            return {'message': 'delete from Questions Database'}, 201
        return message, 404


class Question(Resource):
    def get(self):
        category = None or request.args.get('category') 
        limit = 25 and request.args.get('limit')
        subcategory = None or request.args.get('subcategory')
        difficulty = None or request.args.get('difficulty')

        try:
            if int(limit) <=25:
                question = QuestionModel.get_filtered(category, limit, subcategory=subcategory, difficulty=difficulty)
                return list(map(lambda x: x.return_json(), question))
        except TypeError:
            return message

