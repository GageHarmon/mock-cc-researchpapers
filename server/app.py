#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class All_Research(Resource):
    def get(self):
        
        #TRADITIONAL
        all_research = Research.query.all()
        research_list = []
        for research in all_research:
            new_research = {
                "id": research.id,
                "topic": research.topic,
                "year": research.year,
                "page_count": research.page_count
            }
            research_list.append(new_research)
        return make_response(research_list, 200)

api.add_resource(All_Research, '/research')

        # research_list = Research.query.all()
        # researches_dict_list = [research.to_dict() for research in research_list]
        
        # response = make_response(
        #     researches_dict_list,
        #     200
        # )
        # return response
    
        #ALEX ONE LINE
        # return make_response([research.to_dict(only = ('id', 'topic', 'year', 'page_count')) for research in Research.query.all()], 200)
class ResearchById(Resource):
    def get(self):
        research = Research.query.filter_by(id=id).first()
        if not research:
            return make_response("Research not found", 404)
        response = make_response(research.to_dict, 200)
        return response
    
    def delete(self, id):
        research = Research.query.filter_by(id=id).first()
        if not research:
            return make_response("Research not found", 404)
            
            
        db.session.delete(research)
        db.session.commit()
        return make_response(
            'Research Deleted', 200)
    
api.add_resource(ResearchById, '/research/<int:id>')
        #ALEX 1 line
        # return make_response(Research.query.filter(Research.id == id).first().to_dict(), 200) if Research.query.filter(Research.id == id).first() else make_response({"error": "Research paper not found"}, 404)

class All_Author(Resource):
    def get(self):
        all_authors = Author.query.all()
        author_list = []
        for author in all_authors:
            new_author = {
                'id': author.id,
                'name': author.name,
                'field_of_study': author.field_of_study
            }
            author_list.append(new_author)
        return make_response(author_list, 200)

api.add_resource(All_Author, '/author')  
    
class All_Research_Author(Resource):
    def post(self):
        data = request.get_json()
        research_author = ResearchAuthor(author_id = data["author_id"], research_id = data["research_id"])
        db.session.add(research_author)
        db.session.commit()
        return make_response("Research Author Added", 200)
    
api.add_resource(All_Research_Author, '/research_author')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
