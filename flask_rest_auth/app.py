from distutils.log import Log
from flask import Flask, redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from models import db, MovieModel, User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://tiagosestari@localhost:5432/flaskrestauth"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_envvar('ENV_FILE_LOCATION')

 
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class AddMovie(Resource):
    def post(self):
        data = request.get_json()
        new_movie = MovieModel(data['name'], data['watched'], data['like'])
        db.session.add(new_movie)
        db.session.commit()
        return new_movie.json(), 200

class Movie(Resource):
    @jwt_required()
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
    
    @jwt_required()
    def delete(self, name):
        movie = MovieModel.query.filter_by(name = name).first()
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return {'message': 'movie deleted'}, 200
        return {'message': 'Movie ' + name +  ' does not exist'},400
    
    @jwt_required()
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

class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(body['email'], body['password'])
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        return user.json(), 200

class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        checkUser = User.query.filter_by(email = body['email']).first()
        authorized = checkUser.check_password(body['password'])
        if not authorized:
            return {'message': 'Email or password invalid'}, 401
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(checkUser.id), expires_delta=expires)
        return {'token': access_token}, 200

api.add_resource(AddMovie, '/addmovie')
api.add_resource(Movie, '/movie/<string:name>')
api.add_resource(SignupApi, '/movie/signup')
api.add_resource(LoginApi, '/movie/login')

if __name__ == '__main__':
    app.run(debug=True)


