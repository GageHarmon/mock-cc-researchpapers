from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


    
class ResearchAuthor(db.Model, SerializerMixin):
    __tablename__ = 'research_authors'
    
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    research_id = db.Column(db.Integer, db.ForeignKey('research.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    research = db.Relationship('Research', backref='research_authors')
    authors = db.Relationship('Author', backref='research_authors')
    
    serialize_rules = ('-research.research_authors', '-authors.research_authors')
    
class Research(db.Model, SerializerMixin):
    __tablename__ = 'research'
    
    # serialize_rules = ('-research_authors.research')
    
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    @validates('year')
    def validate_year(self, key, year):
        if year > 999 and year < 10000:
            return year
        
    
class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'
    
    # serialize_rules = ('-research_authors.research')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    @validates
    def validate_field_of_study(self, key, field_of_study):
        if field_of_study == 'AI' or field_of_study == 'Robotics' or field_of_study == 'Cybersecurity' or field_of_study == 'Machine Learning' or field_of_study == 'Vision':
            return field_of_study