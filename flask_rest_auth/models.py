from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash

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

class User(db.Model):
    __tablename__ = '__user'
 
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String())
    password = db.Column(db.String())

 
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def json(self):
        return {'id': self.id, 'email': self.email, 'password': self.password}