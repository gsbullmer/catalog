from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy.sql import func

app = Flask(__name__)

# imports for CRUD Operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Game, User
from datetime import datetime, timedelta

# imports for OAuth
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2, json, requests
from flask import make_response

CLIENT_ID = json.loads(
    open('static/secrets/client_secrets.json',
    'r').read())['web']['client_id']
APPLICATION_NAME = "iBGdb"

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

    return render_template("categories.html", categories = categories, recent_games = recent_games, current_user = current_user, countGames = countGames, fuzzyTime = fuzzyTime)

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
    if 'username' not in login_session:
        flash("You must be logged in to do that.", "alert")
        return redirect(url_for('showCategories'))
    categories = session.query(Category).order_by('name').all()
    if request.method == 'POST':
        newGame = Game(
            name = request.form['name'],
            description = request.form['description'],
            picture = request.form['picture'],
            min_players = request.form['min_players'],
            max_players = request.form['max_players'],
            date_modified = datetime.now(),
            user = getUserInfo(login_session['user_id'])
        )
        for c in request.form.getlist('category'):
            print c
            newGame.categories.append(getCategory(c))

        session.add(newGame)
        session.commit()
        flash("%s Created" % newGame.name, "success")
        game = session.query(Game).order_by('id DESC').first()
        return redirect(url_for('showGameDetails', game_id = game.id))
    else:
        return render_template("newGame.html", categories = categories)

@app.route('/game/<int:game_id>/edit/', methods = ['GET', 'POST'])
def editGame(game_id):
    if 'username' not in login_session:
        flash("You must be logged in to do that.", "alert")
        return redirect(url_for('showCategories'))
    game = session.query(Game).filter_by(id = game_id).one()
    categories = session.query(Category).order_by('name').all()
    if login_session['user_id'] != game.user_id:
        flash("You don't have permission to modify this game.", "alert")
        return redirect(url_for('showGameDetails', game_id = game_id))
    if request.method == 'POST':
        for c in categories:
            if c in game.categories:
                game.categories.remove()

        game.name = request.form['name'],
        game.description = request.form['description'],
        game.picture = request.form['picture'],
        game.min_players = request.form['min_players'],
        game.max_players = request.form['max_players'],
        game.date_modified = datetime.now()

        for c in request.form.getlist('category'):
            print c
            game.categories.append(getCategory(c))

        session.add(game)
        session.commit()
        flash("%s Created" % request.form['name'], "success")
        return redirect(url_for('showGameDetails', game_id = game.id))
    else:
        return render_template("editGame.html", categories = categories)

@app.route('/game/<int:game_id>/delete/', methods = ['GET', 'POST'])
def deleteGame(game_id):
    if 'username' not in login_session:
        flash("You must be logged in to do that.", "alert")
        return redirect(url_for('showCategories'))
    game = session.query(Game).filter_by(id = game_id).one()
    if login_session['user_id'] != game.user_id:
        flash("You don't have permission to delete this game.", "alert")
        return redirect(url_for('showGameDetails', game_id = game_id))
    if request.method == 'POST':
        session.delete(game)
        session.commit()
        flash("%s deleted" % game.name, "success")
        return redirect(url_for('showCategories'))
    else:
        return render_template("deleteGame.html", game = game)

# Making an API Endpoint (GET Request)
@app.route('/api/categories/json')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Categories = [c.serialize for c in categories])

@app.route('/api/category/<slug>/json')
def categoryJSON(slug):
    category = session.query(Category).filter_by(slug = slug).one()
    return jsonify(Category = [g.serialize for g in category.games])

@app.route('/api/game/<int:game_id>/json')
def gameJSON(game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    return jsonify(Game = game.serialize)

@app.route('/api/recent_games/rss')
def recentGamesRSS():
    recent_games = session.query(Game).order_by("date_modified DESC").limit(10)
    rss = render_template("recentGames.xml", recent_games = recent_games)
    response = make_response(rss)
    response.headers['Content-Type'] = 'application/xml'

    return response

# Login routes
@app.route('/login/')
def showLogin():
    state = "".join(random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html", STATE = state)

@app.route('/gconnect', methods = ["POST"])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state token'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('static/secrets/client_secrets.json',
            scope = '')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, "GET")[1])

    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token in used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID doesn't match app's ID."), 401)
        print "Token's client ID doesn't match app's ID."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is already connected"), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params = params)
    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    # Check to see if User is already in the database
    newUser = None
    user_id = getUserID(login_session['email'])
    if not user_id:
        newUser = True
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<div class="small-4 columns text-right">'
    output += '<img src="%s" style = "width: 150px; height: 150px;border-radius: 75px;-webkit-border-radius: 75px;-moz-border-radius: 75px;"> ' % login_session['picture']
    output += '</div>'
    output += '<div class="small-8 columns text-left">'
    if newUser:
        output += '<h4>Welcome, %s!</h4>' % login_session['username']
    else:
        output += '<h4>Welcome back, %s!</h4>' % login_session['username']
    output += '<h6>We\'re sure glad you\'re here!'
    output += '</div>'
    flash("Successfully logged in as %s." % login_session['username'],
    "success")
    print "done!"
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/fbconnect', methods=["POST"])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps("Invalid state parameter."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(open('static/secrets/fb_client_secrets.json',
        'r').read())['web']['app_id']
    app_secret = json.loads(open('static/secrets/fb_client_secrets.json',
        'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, "GET")[1]

    userinfo_url = "https://graph.facebook.com/v2.4/me"
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token

    h = httplib2.Http()
    result = h.request(url, "GET")[1]

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, "GET")[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # Check to see if User is already in the database
    newUser = None
    user_id = getUserID(login_session['email'])
    if not user_id:
        newUser = True
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<div class="small-4 columns text-right">'
    output += '<img src="%s" style = "width: 150px; height: 150px;border-radius: 75px;-webkit-border-radius: 75px;-moz-border-radius: 75px;"> ' % login_session['picture']
    output += '</div>'
    output += '<div class="small-8 columns text-left">'
    if newUser:
        output += '<h4>Welcome, %s!</h4>' % login_session['username']
    else:
        output += '<h4>Welcome back, %s!</h4>' % login_session['username']
    output += '<h6>We\'re sure glad you\'re here!'
    output += '</div>'
    flash("Successfully logged in as %s." % login_session['username'],
    "success")
    print "done!"
    return output

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[0]
    return "You have been logged out."

@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']

        flash("You have successfully been logged out.", "success")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in to begin with!", "alert")
        return redirect(url_for('showCategories'))

# Helper functions
def countGames(gamesList):
    return len(gamesList)

def fuzzyTime(date_time):
    time_diff = datetime.now() - date_time
    if time_diff >= timedelta(weeks = 52):
        unit = 'year'
        diff = time_diff.days // 365
        string = '%d %s%s' % (diff, unit, "s"[diff == 1:])
    elif time_diff >= timedelta(days = 30):
        unit = 'month'
        diff = time_diff.days // 30
        string = '%d %s%s' % (diff, unit, "s"[diff == 1:])
    elif time_diff >= timedelta(weeks = 1):
        unit = 'week'
        diff = time_diff.days // 7
        string = '%d %s%s' % (diff, unit, "s"[diff == 1:])
    elif time_diff.days:
        unit = 'day'
        diff = time_diff.days // 1
        string = '%d %s%s' % (diff, unit, "s"[diff == 1:])
    elif time_diff.seconds >= 3600:
        unit = 'hour'
        diff = time_diff.total_seconds() // 3600
        string = '%d %s%s' % (diff, unit, "s"[diff == 1:])
    elif time_diff.seconds >= 60:
        unit = 'minute'
        diff = time_diff.total_seconds() // 60
        string = '%d %s%s' % (diff, unit, "s"[diff == 1:])
    else:
        string = 'moments'

    fuzzy_time = '%s ago' % string
    return fuzzy_time

def getCategory(slug):
    category = session.query(Category).filter_by(slug = slug).one()
    return category

def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

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
