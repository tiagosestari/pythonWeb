from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class MovieModel(db.Model):
    __tablename__ = 'moviesrest'
 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    watched = db.Column(db.Boolean())
    like = db.Column(db.Boolean())
 
    def __init__(self, name, watched, like):
        self.name = name
        self.watched = watched
        self.like = like
        
 
    def json(self):
        return {'id': self.id, 'name': self.name, 'watched': self.watched, 'liked': self.like}