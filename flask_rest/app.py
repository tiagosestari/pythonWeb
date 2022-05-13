from flask import Flask, redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_migrate import Migrate
from models import db, MovieModel
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://tiagosestari@localhost:5432/flaskrest"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

class AddMovie(Resource):
    def post(self):
        data = request.get_json()
        new_movie = MovieModel(data['name'], data['watched'], data['like'])
        db.session.add(new_movie)
        db.session.commit()
        return new_movie.json(), 200

class Movie(Resource):
    def get(self, name):
        if name == "getall":
            movies = MovieModel.query.all()
            return {'Movies':list(movie.json() for movie in movies)}, 200
        else:
            movie = MovieModel.query.filter_by(name = name).first()
            if movie:
                return movie.json(), 200
            else:
                return {'message': 'Movie not found'},400
    
    def delete(self, name):
        movie = MovieModel.query.filter_by(name = name).first()
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return {'message': 'movie deleted'}, 200
        return {'message': 'Movie ' + name +  ' does not exist'},400
    
    def put(self, name):
        data = request.get_json()
        movie = MovieModel.query.filter_by(name = name).first()
    
        if movie:
            movie_as_is = movie.json()
            movie.name = data['name']
            movie.watched = data['watched']
            movie.like = data['like']
        else:
            return {'message': 'No movie to update'}
        
        db.session.add(movie)
        db.session.commit()
        return {'message': {'was': movie_as_is, 'updated': movie.json()}}, 200

api.add_resource(AddMovie, '/addmovie')
api.add_resource(Movie, '/movie/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)


