# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from poke_app.models import Pokemon, User, PokeTeam

class PokeTeamForm(FlaskForm):
    """Form to create a Pokemon Team."""
    team_name = StringField('Team Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    pokemon_team = QuerySelectMultipleField('Pokemon',
        query_factory=lambda: Pokemon.query)
    submit = SubmitField('Submit')


class TrainerForm(FlaskForm):
    """Form to create a trainer."""
    username = StringField('Trainer Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    badges = TextAreaField('What or how many badges do you have?')
    submit = SubmitField('Submit')


class PokemonForm(FlaskForm):
    """Form to create a Pokemon!"""
    index_number = StringField('Pokemon Index Number',
        validators=[DataRequired(), Length(min=1, max=4)])
    name = StringField('Pokemon Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    stats = StringField('Stats',
        validators=[DataRequired(), Length(min=3, max=80)])
    type_1 = StringField('Type',
        validators=[DataRequired(), Length(min=3, max=80)])
    type_2 = StringField('Type',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')