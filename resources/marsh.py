from marshmallow import Schema, fields

class QuestionSchema(Schema):
    category = fields.Str()
    subcategory = fields.Str()
    question = fields.Str()
    block_code  = fields.Str()
    difficulty =fields.Str()
    correct_answer = fields.Str()
    wrong_answers = fields.List(fields.Str())

class UserSchema(Schema):
    username = fields.Str()
    password = fields.Str()