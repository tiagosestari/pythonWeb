from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, InfoModel
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://tiagosestari@localhost:5432/flaskone"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/form')
def form():
    return render_template('form.html')
 
 
@app.route('/login', methods = ['POST'])
def login():
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        print(name, age)
        new_user = InfoModel(name=name, age=age)
        db.session.add(new_user)
        db.session.commit()
        return f"Done!!"
 
 
if __name__ == '__main__':
    app.run(debug=True)