from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Game, User

engine = create_engine('postgresql:///catalog')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

Session = sessionmaker(bind = engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
s = Session()

# Clear the Database
s.query(Game).delete()
s.query(Category).delete()
s.query(User).delete()
s.commit()


# Add Users
user1 = User(name = "Lucille Ballard", email = "lballard@email.com")
s.add(user1)

user2 = User(name = "Simon Poole", email = "spoole@email.com")
s.add(user2)

user3 = User(name = "Ivan Walters", email = "iwalters@email.com")
s.add(user3)

user4 = User(name = "Tamara Becker", email = "tbecker@email.com")
s.add(user4)

user5 = User(name = "Henry Palmer", email = "hpalmer@email.com")
s.add(user5)
s.commit()


# Add Catagories
adventure = Category(name = "Adventure", slug = "adventure", user = user1)
s.add(adventure)

fantasy = Category(name = "Fantasy", slug = "fantasy", user = user2)
s.add(fantasy)

fighting = Category(name = "Fighting", slug = "fighting", user = user3)
s.add(fighting)

scifi = Category(name = "Science Fiction", slug = "science-fiction", user = user4)
s.add(scifi)

wargame = Category(name = "Wargame", slug = "wargame", user = user5)
s.add(wargame)

travel = Category(name = "Travel", slug = "travel", user = user1)
s.add(travel)

space_exploration = Category(name = "Space Exploration", slug = "space-exploration", user = user2)
s.add(space_exploration)

civilization = Category(name = "Civilization", slug = "civilization", user = user3)
s.add(civilization)

negotiation = Category(name = "Negotiation", slug = "negotiation", user = user4)
s.add(negotiation)

economic = Category(name = "Economic", slug = "economic", user = user5)
s.add(economic)

s.commit()


# Add Games
game1 = Game(name = "Duel of Ages II", description = "Duel of Ages II is a time-scramble board game played between two opposing sides each having 1 to 4 players, with uneven size allowable. Each side controls a selected team of 8-12 characters from different ages of time: Ancient, Colonial, Modern and Future. The goal is to win greater glory in overcoming adventures and in tactical combat than the opposing team.", min_players = 2, max_players = 8, date_added = datetime.today(), categories = [adventure, fantasy, fighting, scifi, wargame], user = user2)
s.add(game1)

game2 = Game(name = "Firefly: The Game", description = "Players begin with a ship, and travel from planet to planet, hiring crew, purchasing ship upgrades, and picking up cargo to deliver (jobs) all in the form of cards. Some crew and cargo are illegal, and can be confiscated if your ship is boarded by an alliance vessel. Travelling from planet to planet requires turning over \"full burn\" cards, one for each space moved. Most do nothing, but you can also encounter an Alliance ship, have a breakdown, or even run into Reavers. Completing jobs gets you cash. First player to complete the story goals wins.", min_players = 1, max_players = 4, date_added = datetime.today(), categories = [scifi, travel, space_exploration], user = user4)
s.add(game2)

game3 = Game(name = "Catan", description = "In Catan (formerly The Settlers of Catan), players try to be the dominant force on the island of Catan by building settlements, cities, and roads. On each turn dice are rolled to determine what resources the island produces. Players collect these resources (cards)-wood, grain, brick, sheep, or stone-to build up their civilizations to get to 10 victory points and win the game.", min_players = 3, max_players = 4, date_added = datetime.today(), categories = [civilization, negotiation], user = user1)
s.add(game3)

game4 = Game(name = "Monopoly", description = "Players take the part of land owners, attempting to buy and then develop their land. Income is gained by other players visiting their properties and money is spent when they visit properties belonging to other players. When times get tough, players may have to mortgage their properties to raise cash for fines, taxes and other misfortunes.", min_players = 2, max_players = 8, date_added = datetime.today(), categories = [economic, negotiation], user = user3)
s.add(game4)

s.commit()


print "added games!"
s.close()
