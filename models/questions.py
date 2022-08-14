
from db import db
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from sqlalchemy import func


class QuestionModel(db.Model):
    __tablename__ = 'questions'
    __table_args__ = {'sqlite_autoincrement': True} 


    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(50),  nullable=False)
    subcategory = db.Column(db.String(50),  nullable=True)
    question = db.Column(db.String(2000), nullable=False)
    block_code = db.Column(db.String(5000), nullable=True)
    difficulty = db.Column(db.String(50),  nullable=False)
    correct_answer =  db.Column(db.String(2000),  nullable=False)
    wrong_answers = db.Column(MutableList.as_mutable(PickleType), default=[], nullable=False)



    def __init__(self, subcategory, category, question, 
    block_code, difficulty, 
    correct_answer, wrong_answers):
        self.category = category
        self.subcategory = subcategory
        self.question =question
        self.block_code = block_code
        self.difficulty = difficulty
        self.correct_answer  = correct_answer
        self.wrong_answers =   wrong_answers

    def return_json(self):
        return {
            'id': self.get_id(),
            'category': self.category,
            'subcategory': self.subcategory,
            'question': self.question,
            'block_code': self.block_code,
            'difficulty': self.difficulty,
            'correct_answer': self.correct_answer,
            'wrong_asnwers': self.wrong_answers
        }
    @classmethod
    def get_filtered(cls, category, limit, subcategory=None, difficulty=None):
        if difficulty and subcategory:
                return cls.query.filter_by(category=category, 
                subcategory=subcategory, 
                difficulty=difficulty).order_by(func.random()).limit(int(limit))
        elif difficulty:
            return cls.query.filter_by(
            category=category,
            difficulty=difficulty).order_by(func.random()).limit(int(limit))
        elif subcategory:
            return cls.query.filter_by(
                category=category, 
                subcategory=subcategory).order_by(func.random()).limit(int(limit))
        return cls.query.filter_by(
            category=category).order_by(func.random()).limit(int(limit))


    @classmethod
    def get_all(cls, limit):
        return cls.query.order_by(func.random()).limit(limit)


    def get_id(self):
        data =  db.session.query(QuestionModel).filter(
            QuestionModel.question == self.question,
            QuestionModel.correct_answer == self.correct_answer,
            QuestionModel.category == self.category,
            QuestionModel.difficulty == self.difficulty).first()
        return data.id

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
           
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_counts(cls):
        #Table.query.with_entities(Table.column, func.count(Table.column)).group_by(Table.column).all()
        return cls.query.with_entities(cls.category, cls.subcategory, func.count(cls.subcategory)).group_by(cls.category, cls.subcategory).all()


    @classmethod
    def get_category_unique(cls):
        return cls.query.with_entities(cls.category, cls.subcategory).group_by(cls.subcategory, cls.category).all()