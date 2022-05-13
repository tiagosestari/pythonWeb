from flask import Flask, redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, MovieModel
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://tiagosestari@localhost:5432/flaskcrud"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def root():
    return redirect('/movies')

#READ Routes
@app.route('/movies', methods = ['GET'])
def movies():
    movies = MovieModel.query.all()
    return render_template('movies.html', movies = movies)

@app.route('/movies/<int:id>')
def returnSingleMoive(id):
    movie = MovieModel.query.filter_by(id = id).first()
    if movie:
        return render_template('movie.html', movie = movie)
    return f"No movie with ID {id}"

#CREATE ROUTES
@app.route('/movies/addmovie', methods = ['GET','POST'])
def addmovie():

    if request.method == 'GET':
        return render_template('form.html')
    
    if request.method == 'POST':
        
        name = request.form['name']
        
        if (request.form['like'] == 'like'):
            like = True
        else:
            like = False
        
        if ('watched' in request.form):
            watched = True
        else:
            watched = False
        
        new_movie = MovieModel(name=name, like=like, watched=watched)
        db.session.add(new_movie)
        db.session.commit()
        return redirect("/movies")

#DELETE ROUTES
@app.route('/movies/<int:id>/delete', methods = ['GET', 'POST'])
def delete(id):
    movie = MovieModel.query.filter_by(id = id).first()
    if (request.method == 'GET'):
        if movie:
            return render_template('delete.html', movie = movie)
        else:
            return f"No movie with ID {id}"
    
    if(request.method == 'POST'):
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return redirect("/movies")
        
#UPDATE ROUTES 

if __name__ == '__main__':
    app.run(debug=True)


