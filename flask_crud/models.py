from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class MovieModel(db.Model):
    __tablename__ = 'movies'
 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    watched = db.Column(db.Boolean())
    like = db.Column(db.Boolean())
 
    def __init__(self, name, watched, like):
        self.name = name
        self.watched = watched
        self.like = like
        
 
    def __repr__(self):
        return f"Id: {self.id} Name:{self.name} Watched:{self.watched} Liked:{self.like}"