# Create your tests here.
import os
import unittest
from unittest import TestCase
from poke_app import app, db, bcrypt
from poke_app.models import User, Pokemon, PokeTeam
# Setup
def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_pokemon():
    user1 = Pokemon(
        index_number=4,
        name= 'Charmander',
        stats='health 100',
        type_1 = 'Fire',
        type_2 = 'N/a'
    )
    db.session.add(user1)

    user2 = Pokemon(
        index_number=5,
        name= 'Charmeleon',
        stats='health 100',
        type_1 = 'Fire',
        type_2 = 'N/a'
    )
    db.session.add(user2)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='user', password=password_hash)
    db.session.add(user)
    db.session.commit()

class MainTests(unittest.TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_create_pokemon_logged_out(self):
        """see if the user is can create a pokemon if they are logged out"""
        create_pokemon()
        create_user()
        response = self.app.get('/create_pokemon')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_pokemon', response.location)

    def test_create_trainer_logged_out(self):
        """see if the user is can create a trainer if they are logged out"""
        create_pokemon()
        create_user()
        response = self.app.get('/create_trainer')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_pokemon', response.location)