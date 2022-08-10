"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, FavCharacters, FavPlanets


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    user = User.query.all()
    all_users = list(map(lambda user: user.serialize(), user))
    return jsonify(all_users), 201

@app.route('/user', methods=['POST'])
def post_user():
    body = request.get_json()
    user = User(name=body["name"], email=body["email"], password=body["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

@app.route('/user/<int:id>', methods=['GET'])
def single_user(id):
    user = User.query.get(id)

    return jsonify(user.serialize())

# CHARACTERS: 

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    all_characters = list(map(lambda characters: characters.serialize(), characters))
    return jsonify(all_characters), 201

@app.route('/characters', methods=['POST'])
def post_characters():
    body = request.get_json()
    characters = Characters(name=body["name"])
    db.session.add(characters)
    db.session.commit()
    return jsonify(characters.serialize()), 201

@app.route('/characters/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def characters_single(id):
    if request.method == 'GET':
        characters = Characters.query.get(id)
        if characters is None:
            raise APIException("there is not character", 404)

        return jsonify(characters.serialize())
    
    if request.method == 'PUT':
        characters = Characters.query.get(id)
        if characters is None:
           raise APIException("there is not character", 404)
        body = request.get_json()

        characters.name = body["name"]
        db.session.commit()

        return jsonify(characters.serialize())
    
    if request.method == 'DELETE':
        characters = Characters.query.get(id)
        if id is None:
            raise APIException("Character not found", 201)
        db.session.delete(characters)
        db.session.commit()

        return jsonify(characters.serialize())

# PLANETS: 

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda planets: planets.serialize(), planets))
    return jsonify(all_planets), 201

@app.route('/planets', methods=['POST'])
def post_planets():
    body = request.get_json()
    planets = Planets(name=body["name"])
    db.session.add(planets)
    db.session.commit()
    return jsonify(planets.serialize()), 201

@app.route('/planets/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def planets_single(id):
    if request.method == 'GET':
        planets = Planets.query.get(id)
        if planets is None:
            raise APIException("there is not character", 404)

        return jsonify(planets.serialize())
    
    if request.method == 'PUT':
        planets = Planets.query.get(id)
        if planets is None:
           raise APIException("there is not character", 404)
        body = request.get_json()

        if not ("id" in body):
            raise APIException("id ", 404)

        planets.name = body["name"]
        db.session.commit()

        return jsonify(planets.serialize())
    
    if request.method == 'DELETE':
        planets = Planets.query.get(id)
        if id is None:
            raise APIException("Planet not found", 404)
        db.session.delete(planets)
        db.session.commit()

        return jsonify(planets.serialize())

# FAVCHARACTER: 

@app.route('/user/<int:user_id>/favcharacter/', methods=['GET'])
def favcharacter_get(user_id):
        fav_character = FavCharacters.query.filter_by(user_id=user_id)
        if user_id is None:
            raise APIException("there is not character", 404)

        favcharacter = list(map(lambda fav_character: fav_character.serialize(), fav_character))
        return jsonify(favcharacter), 201

@app.route('/user/<int:user_id>/favcharacter/<int:character_id>', methods=['POST'])
def postchar_fav(user_id, character_id):
    favorites = FavCharacters(user_id=user_id, character_id=character_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify(favorites.serialize()), 201

@app.route('/user/<int:user_id>/favcharacter/<int:character_id>', methods=['DELETE'])
def delete_char_fav(user_id, character_id):
    deleteFav = FavCharacters.query.filter_by(user_id=user_id, character_id=character_id).one() #one devuelve el objeto encontrado, sin el one, devuelve el queryobject
    db.session.delete(deleteFav)
    db.session.commit()

    return jsonify(deleteFav.serialize()), 202

# FAVPLANET: 

@app.route('/user/<int:user_id>/favplanet/', methods=['GET'])
def favplanet_get(user_id):
        fav_character = Favplanets.query.filter_by(user_id=user_id)
        if user_id is None:
            raise APIException("there is not character", 404)

        favplanet = list(map(lambda fav_character: fav_character.serialize(), fav_character))
        return jsonify(favplanet), 201

@app.route('/user/<int:user_id>/favplanet/<int:planet_id>', methods=['POST'])
def postplanet_fav(user_id, planet_id):
    favorites = Favplanets(user_id=user_id, planet_id=planet_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify(favorites.serialize()), 201

@app.route('/user/<int:user_id>/favplanet/<int:planet_id>', methods=['DELETE'])
def delete_planet_fav(user_id, planet_id):
    deleteFav = Favplanets.query.filter_by(user_id=user_id, planet_id=planet_id).one() #one devuelve el objeto encontrado, sin el one, devuelve el queryobject
    db.session.delete(deleteFav)
    db.session.commit()

    return jsonify(deleteFav.serialize()), 202

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
