"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person
from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/hello', methods=['POST', 'GET'])
# def handle_hello():

#     response_body = {
#         "hello": "world"
#     }
@app.route('/person', methods=['POST', 'GET']) 
def handle_person():
    if request.method == 'POST': 
        return "A POST has been received!"
    else:
        people_query = Person.query.all()
        all_people = list(map(lambda x: x.serialize(), people_query))
        return jsonify(all_people), 200


@app.route("/person1", methods=['POST', 'GET']) # here we specify that this endpoints accepts POST and GET requests
def handle_hello():
    if request.method == 'DELETE': # we can understand what type of request are we handling using a conditional
        return "A POST has been received!"
    else:
        return "A GET has been received!"


@app.route('/person2', methods=['POST'])
def create_person():
    # POST request
        body = request.get_json() # get the request body content

        if 'username' not in body:
            return 'You need to specify the first_name',400
        if 'email' not in body:
            return 'You need to specify the last_name', 400

        return "ok", 200
      "hello"  




      

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
