from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class urlModel(db.Model):
    __tablename__ = 'url_to_redirect'
 
    id = db.Column(db.Integer, primary_key = True)
    shortner = db.Column(db.String())
    destination = db.Column(db.String())
    
 
    def __init__(self, shortner, destination):
        self.shortner = shortner
        self.destination = destination
        
 
    def json(self):
        return {'id': self.id, 'shortner': 'http://127.0.0.1:5000/' + self.shortner, 'destination': self.destination}