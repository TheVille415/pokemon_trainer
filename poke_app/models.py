# Create your models here.
from os import name
from poke_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

# User Login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    badges = db.Column(db.String(200))

    def __repr__(self):
        return f'<User: {self.username}>'

'''
I need to work more on applying this into my models so i can seperate users from trainers
ex: making an account and adding my little sister and myself as users.
# Trainer Model
# Needs to conecc to team
class Trainer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    badges = db.Column(db.String(200))
    # pokeom_in_team = db.relationship('PokeTeam', secondary='trainer_pokemon', back_populates='party')
'''
class Pokemon(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index_number = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    stats = db.Column(db.String(200),nullable=False)
    type_1 = db.Column(db.String(200), nullable=False)
    type_2 = db.Column(db.String(200), nullable=False)

    # poketeam_id = db.Column(db.Integer, db.ForeignKey('poketeam.id'), nullable=False)
    # team = db.relationship('PokeTeam', back_populates='pokemon')


# connects from trainer to individual pokemon
class PokeTeam(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(), nullable=False)
    trainer = db.Column(db.String(), nullable=False)
    pokemon = db.Column(db.String(), nullable=False)
    total_health = db.Column(db.Integer)
    # pokemon = db.relationship('Pokemon', back_populates='team')
