from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class FavCharacters(db.Model):
    __tablename__ = 'favcharacters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    userRelationship = db.relationship('User')
    characterRelationship = db.relationship('Characters')

    def __repr__(self):
        return '<FavCharacters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.userRelationship.name,
            "character": self.characterRelationship.name
        }

class FavPlanets(db.Model):
    __tablename__ = 'favplanets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    userRelationship = db.relationship('User')
    planetsRelationship = db.relationship('Planets')

    def __repr__(self):
        return '<FavPlanets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.userRelationship.name,
            "planets": self.planetsRelationship.name
        }