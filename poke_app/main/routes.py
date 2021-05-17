"""Import packages and modules."""
from os import stat
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from poke_app.models import User, Pokemon, PokeTeam
# the forms we made
from poke_app.main.forms import PokeTeamForm, TrainerForm, PokemonForm
from poke_app import bcrypt
# Import app and db
from poke_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_pokemon = Pokemon.query.all()
    all_trainers = User.query.all()
    return render_template('home.html',
        all_pokemon=all_pokemon, all_trainers=all_trainers)


@main.route('/create_team', methods=['GET', 'POST'])
@login_required
def create_team():
    form = PokeTeamForm()
    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_team = PokeTeam(
            team_name=form.team_name.data,
            trainer=form.trainer.data,
            pokemon=form.pokemon.data
        )
        db.session.add(new_team)
        db.session.commit()

        flash('Team has been created successfully.')
        return redirect(url_for('main.book_detail', book_id=new_team.id))
    return render_template('create_team.html', form=form)


@main.route('/create_trainer', methods=['GET', 'POST'])
@login_required
def create_trainer():
    form = TrainerForm()
    if form.validate_on_submit():
        new_trainer = User(
            username=form.username.data,
            badges=form.badges.data
        )
        db.session.add(new_trainer)
        db.session.commit()

        flash('New trainer created successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_trainer.html', form=form)

# Trainer display page
@main.route('/profile_traienr/<username>')
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile_trainer.html', user=user)

@main.route('/create_pokemon', methods=['GET', 'POST'])
@login_required
def create_pokemon():
    form = PokemonForm()
    if form.validate_on_submit():
        new_pokemon = Pokemon(
            index_number=form.index_number.data,
            name=form.name.data,
            stats=form.name.data,
            type_1=form.type_1.data,
            type_2=form.type_2.data,
        )
        db.session.add(new_pokemon)
        db.session.commit()

        flash('New pokemon added successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_pokemon.html', form=form)
