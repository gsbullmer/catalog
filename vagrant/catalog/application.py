from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy.sql import func

app = Flask(__name__)

# imports for CRUD Operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Game, User

# imports for OAuth
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2, json, requests
from flask import make_response

# Create session and connect to DB
engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).order_by('name').all()
    recent_games = session.query(Game).order_by("date_modified DESC").limit(10)

    return render_template("categories.html", categories = categories, recent_games = recent_games, countGames = countGames)

@app.route('/category/<slug>/')
def showGames(slug):
    categories = session.query(Category).order_by('name').all()
    category = session.query(Category).filter_by(slug = slug).one()

    return render_template("games.html", categories = categories, category = category, countGames = countGames)

@app.route('/game/<int:game_id>/')
def showGameDetails(game_id):
    categories = session.query(Category).order_by('name').all()
    game = session.query(Game).filter_by(id = game_id).one()

    return render_template('gameDetails.html', categories = categories, game = game, countGames = countGames)

# Helper functions
def countGames(gamesList):
    return len(gamesList)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
