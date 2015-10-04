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

    return "categories"

@app.route('/category/<slug>/')
def showGames(slug):
    category = session.query(Category).filter_by(slug = slug).first()
    games = session.query(Game).filter_by(categories = category).order_by('name').all()

    return "games"

@app.route('/game/<int:game_id>/')
def showGameDetails(game_id):
    game = session.query(Game).filter_by(id = game_id).first()

    return "game"


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
