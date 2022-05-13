from flask import Flask, redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_migrate import Migrate
from models import db, urlModel
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://tiagosestari@localhost:5432/urlshortner"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

#1 send a URL
#2 chekc if URL exists
#2.yes Return it
#2.no Create new URL
#3 Return new URL
class getShortURL(Resource):
    def post(self):
        data = request.get_json()
        #expected payload {'url': url, 'shortner': shortner}
        if (not 'url' in data or not 'shortner' in data):
            return {'message': 'Please use valid payload.', 'validPayload': {'url': 'url', 'shortner': 'shortner'}},400
        
        checkShortnerExistence = urlModel.query.filter_by(shortner = data['shortner']).first()
        if checkShortnerExistence:
            return {'message': 'Shortner already in use'}, 400
       
        
        new_url = urlModel(data['shortner'], data['url'])
        db.session.add(new_url)
        db.session.commit()
        return new_url.json(), 200

class redirectURL(Resource):
    def get(self, url):
        checkUrlExistence = urlModel.query.filter_by(shortner = url).first()
        if checkUrlExistence:
            urlStr = 'https://' + checkUrlExistence.destination
            return redirect(urlStr)
        
        return {'message': 'No url for this shortner: ' + checkUrlExistence.shortner}




api.add_resource(getShortURL, '/')
api.add_resource(redirectURL, '/<string:url>')

if __name__ == '__main__':
    app.run(debug=True)


