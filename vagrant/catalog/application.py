from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy.sql import func

app = Flask(__name__)

# imports for CRUD Operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Game, User
from datetime import datetime

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

    if 'user_id' not in login_session:
        current_user = None
    else:
        current_user = getUserInfo(login_session['user_id'])

    return render_template("categories.html", categories = categories, recent_games = recent_games, current_user = current_user, countGames = countGames)

@app.route('/category/<slug>/')
def showGames(slug):
    categories = session.query(Category).order_by('name').all()
    category = session.query(Category).filter_by(slug = slug).one()

    if 'user_id' not in login_session:
        current_user = None
    else:
        current_user = getUserInfo(login_session['user_id'])

    return render_template("games.html", categories = categories, category = category, current_user = current_user, countGames = countGames)

@app.route('/game/<int:game_id>/')
def showGameDetails(game_id):
    categories = session.query(Category).order_by('name').all()
    game = session.query(Game).filter_by(id = game_id).one()

    if 'user_id' not in login_session:
        current_user = None
    else:
        current_user = getUserInfo(login_session['user_id'])

    return render_template('gameDetails.html', categories = categories, game = game, current_user = current_user, countGames = countGames)

@app.route('/game/new/', methods = ['GET', 'POST'])
def newGame():
    categories = session.query(Category).order_by('name').all()
    if request.method == 'POST':
        newGame = Game(
            name = request.form['name'],
            description = request.form['description'],
            picture = request.form['picture'],
            min_players = request.form['min_players'],
            max_players = request.form['max_players'],
            date_modified = datetime.today()
            # user = getUser(login_session['user_id'])
        )
        for c in request.form.getlist('category'):
            print c
            newGame.categories.append(getCategory(c))

        session.add(newGame)
        session.commit()
        flash("%s Created" % newGame.name)
        game = session.query(Game).order_by('id DESC').first()
        return redirect(url_for('showGameDetails', game_id = game.id))
    else:
        return render_template("newGame.html", categories = categories)

@app.route('/game/<int:game_id>/edit/', methods = ['GET', 'POST'])
def editGame(game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    categories = session.query(Category).order_by('name').all()
    if request.method == 'POST':
        for c in categories:
            if c in game.categories:
                game.categories.remove()

        game.name = request.form['name'],
        game.description = request.form['description'],
        game.picture = request.form['picture'],
        game.min_players = request.form['min_players'],
        game.max_players = request.form['max_players'],
        game.date_modified = datetime.today(),
        game.user = getUser(login_session['user_id'])

        for c in request.form.getlist('category'):
            print c
            game.categories.append(getCategory(c))

        session.add(game)
        session.commit()
        flash("%s Created" % request.form['name'])
        return redirect(url_for('showGameDetails', game_id = game.id))
    else:
        return render_template("editGame.html", categories = categories)

@app.route('/game/<int:game_id>/delete/', methods = ['GET', 'POST'])
def deleteGame(game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    if login_session['user_id'] != game.user_id:
        flash("You don't have permission to modify this game.")
        return redirect(url_for('showGameDetails', game_id = game_id))
    if request.method == 'POST':
        session.delete(game)
        session.commit()
        flash("%s deleted" % game.name)
        return redirect(url_for('showCategories'))
    else:
        return render_template("deleteGame.html", game = game)

@app.route('/login/')
def showLogin():
    state = "".join(random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html", STATE = state)

# Helper functions
def countGames(gamesList):
    return len(gamesList)

def getCategory(slug):
    category = session.query(Category).filter_by(slug = slug).one()
    return category

def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUser(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return Null

def createUser(login_session):
    newUser = User(
        name = login_session['username'],
        email = login_session['email'],
        picture = login_session['picture']
    )
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
