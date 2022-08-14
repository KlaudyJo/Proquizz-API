from flask_restful import Resource
from models.questions import QuestionModel
message = {'message': 'Wrong params'}


class MetaData(Resource):
    def get(self):
            data_cat = QuestionModel.get_counts() 
            data_dict = {}
            try:
                for cat in data_cat:
                    if cat[0] not in data_dict:
                        data_dict[cat[0]] = {'count_total': 0, 'subcategories': [{}]}
                    data_dict[cat[0]]['subcategories'][0][cat[1]] =  cat[2]
                    data_dict[cat[0]]['count_total'] += int(cat[2])
                return data_dict, 201      
            except TypeError:
                return message, 404   


class UniqueData(Resource):
    def get(self):
        data_cat = QuestionModel.get_category_unique()
        categories = {}
        try:
            for data in data_cat:
                if data.category not in categories:
                    categories[data.category] = []          
                categories[data.category].append(data.subcategory)
            return  categories, 201

        except TypeError:
            return message, 404
