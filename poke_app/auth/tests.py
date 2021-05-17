# Create your tests here.
import os
import unittest
from unittest import TestCase
from poke_app import app, db, bcrypt
from poke_app.models import User, Pokemon, PokeTeam

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


class AuthTests(TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_login_incorrect_password(self):
        """test to see if the user can log in with an incorrect password"""
        create_user()
        sample_data = {
            "username": "user",
            "password": "nopass",
        }
        response = self.app.post("/login", data=sample_data)
        response_msg = response.get_data(as_text=True)
        self.assertIn("Log In", response_msg)
        self.assertIn(
            "Password doesnt match. Please try again.", response_msg
        )
        self.assertNotIn("Log Out", response_msg)

    def test_logout(self):
        """test logout"""
        create_user()
        sample_data = {
            "username":"user",
            "password":"passWord"
        }
        
        self.app.post("/login", data=sample_data)

        response = self.app.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_msg = response.get_data(as_text=True)
        
        self.assertIn("Log In", response_msg)
        self.assertNotIn("Log Out", response_msg)

    def test_signup_existing_user(self):
        create_user()
        sample_data = {
            "username": "user1",
            "password": "password",
        }
        response = self.app.post("/signup", data=sample_data)
        # - Check that the form is displayed again with an error message
        response_msg = response.get_data(as_text=True)
        self.assertIn("Sign Up", response_msg)
        self.assertIn(
            "That username is taken. Please choose a different one.",
            response_msg,
        )


    def test_login_nonexistent_user(self):
        """test a nonexistent user, make sure it fails"""
        sample_data = {
            "username": "nonexistent_user",
            "password": "oppsie",
        }
        response = self.app.post("/login", data=sample_data)

        response_msg = response.get_data(as_text=True)
        self.assertIn("Log In", response_msg)
        self.assertIn(
            "No user with that username. Please try again or sign up!", response_msg
        )
        self.assertNotIn("Log Out", response_msg)
