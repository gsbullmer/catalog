from datetime import datetime, timedelta
import random

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
abstract_strategy = Category(name = "Abstract Strategy Games", slug = "abstract_strategy", description = "like Chess or Go")
s.add(abstract_strategy)

customizable = Category(name = "Customizable Games", slug = "customizable", description = "CCGs, CMGs, LCGs, etc")
s.add(customizable)

thematic = Category(name = "Thematic Games", slug = "thematic", description = "emphasis on narrative")
s.add(thematic)

family = Category(name = "Family Games", slug = "family", description = "fun for kids and adults")
s.add(family)

childrens = Category(name = "Children's Games", slug = "childrens", description = "best for younger kids")
s.add(childrens)

party = Category(name = "Party Games", slug = "party", description = "few rules, lots of laughs")
s.add(party)

strategy = Category(name = "Strategy Games", slug = "strategy", description = "more complex games")
s.add(strategy)

wargames = Category(name = "Wargames", slug = "wargames", description = "conflict simulation, etc.")
s.add(wargames)

s.commit()


# Add Games
game1 = Game(name = "Duel of Ages II", picture = "http://cf.geekdo-images.com/images/pic1399113_t.jpg", description = "Duel of Ages II is a time-scramble board game played between two opposing sides each having 1 to 4 players, with uneven size allowable. Each side controls a selected team of 8-12 characters from different ages of time: Ancient, Colonial, Modern and Future. The goal is to win greater glory in overcoming adventures and in tactical combat than the opposing team.", min_players = 2, max_players = 8, date_modified = datetime.now() - timedelta(days = random.randint(0, 50), seconds = random.randint(0, 3600 * 24)), categories = [thematic, strategy], user = user1)
s.add(game1)

game2 = Game(name = "Firefly: The Game", picture = "http://cf.geekdo-images.com/images/pic1727008_t.png", description = "Players begin with a ship, and travel from planet to planet, hiring crew, purchasing ship upgrades, and picking up cargo to deliver (jobs) all in the form of cards. Some crew and cargo are illegal, and can be confiscated if your ship is boarded by an alliance vessel. Travelling from planet to planet requires turning over \"full burn\" cards, one for each space moved. Most do nothing, but you can also encounter an Alliance ship, have a breakdown, or even run into Reavers. Completing jobs gets you cash. First player to complete the story goals wins.", min_players = 1, max_players = 4, date_modified = datetime.now() - timedelta(days = random.randint(0, 50), seconds = random.randint(0, 3600 * 24)), categories = [thematic], user = user2)
s.add(game2)

game3 = Game(name = "Catan", picture = "http://cf.geekdo-images.com/images/pic2419375_t.jpg", description = "In Catan (formerly The Settlers of Catan), players try to be the dominant force on the island of Catan by building settlements, cities, and roads. On each turn dice are rolled to determine what resources the island produces. Players collect these resources (cards)-wood, grain, brick, sheep, or stone-to build up their civilizations to get to 10 victory points and win the game.", min_players = 3, max_players = 4, date_modified = datetime.now() - timedelta(days = random.randint(0, 50), seconds = random.randint(0, 3600 * 24)), categories = [family, strategy], user = user3)
s.add(game3)

game4 = Game(name = "Monopoly", picture = "http://cf.geekdo-images.com/images/pic265476_t.jpg", description = "Players take the part of land owners, attempting to buy and then develop their land. Income is gained by other players visiting their properties and money is spent when they visit properties belonging to other players. When times get tough, players may have to mortgage their properties to raise cash for fines, taxes and other misfortunes.", min_players = 2, max_players = 8, date_modified = datetime.now() - timedelta(days = random.randint(0, 50), seconds = random.randint(0, 3600 * 24)), categories = [family], user = user4)
s.add(game4)

game5 = Game(name = "7 Wonders", picture = "http://cf.geekdo-images.com/images/pic860217_t.jpg", description = "You are the leader of one of the 7 great cities of the Ancient World. Gather resources, develop commercial routes, and affirm your military supremacy. Build your city and erect an architectural wonder which will transcend future times.", min_players = 2, max_players = 7, date_modified = datetime.now() - timedelta(days = random.randint(0, 50), seconds = random.randint(0, 3600 * 24)), categories = [family, strategy], user = user5)
s.add(game5)

game6 = Game(name = "Killer Bunnies and the Quest for the Magic Carrot", picture = "http://cf.geekdo-images.com/images/pic207282_t.jpg", description = "Killer Bunnies is a funny and satirical non-collectible, expandable card game. The new Epsilon Edition Starter Deck comes with a bonus Yellow Booster Deck. This game is played with only 1 copy of the game, so players do NOT need to bring their own decks to the table.", min_players = 2, max_players = 8, date_modified = datetime.now() - timedelta(days = random.randint(0, 50), seconds = random.randint(0, 3600 * 24)), categories = [family], user = user1)
s.add(game6)

game7 = Game(name = "Arkham Horror", picture = "http://cf.geekdo-images.com/images/pic175966_t.jpg", description = "Arkham Horror is a cooperative adventure game themed around H.P Lovecraft's Cthulhu Mythos. Players choose from 16 Investigators and take to the streets of Arkham. Before the game, one of the eight Ancient Ones is chosen and it's up to the Investigators to prevent it from breaking into our world. During the course of the game, players will upgrade their characters by acquiring skills, allies, items, weapons, and spells. It's up to the players to clean out the streets of Arkham by fighting many different types of monsters, but their main goal is to close portals to other dimensions that are opening up around town. With too many portals open the Ancient One awakens and the players only have one last chance to save the world. Defeat the Ancient One in combat!", min_players = 1, max_players = 8, date_modified = datetime.now() - timedelta(days = random.randint(0, 50), seconds = random.randint(0, 3600 * 24)), categories = [thematic], user = user2)
s.add(game7)

game8 = Game(name = "Android: Netrunner", picture = "http://cf.geekdo-images.com/images/pic1324609_t.jpg", description = "Android: Netrunner is an asymmetrical Living Card Game for two players. Set in the cyberpunk future of Android and Infiltration, the game pits a megacorporation and its massive resources against the subversive talents of lone runners.", min_players = 2, max_players = 2, date_modified = datetime.now() - timedelta(days = random.randint(0, 50), seconds = random.randint(0, 3600 * 24)), categories = [customizable], user = user3)
s.add(game8)

game9 = Game(name = "Go", picture = "http://cf.geekdo-images.com/images/pic1728832_t.jpg", description = "By all appearances, it's just two players taking turns laying stones on a 19x19 (or smaller) grid of intersections. But once its basic rules are understood, Go shows its staggering depth. One can see why many people say it's one of the most elegant brain-burning abstract games in history, with players trying to claim territory by walling off sections of the board and surrounding each other's stones. The game doesn't end until the board fills up, or, more often, when both players agree to end it, at which time whoever controls the most territory wins.", min_players = 2, max_players = 2, date_modified = datetime.now() - timedelta(days = random.randint(0, 50), seconds = random.randint(0, 3600 * 24)), categories = [abstract_strategy], user = user4)
s.add(game9)

game10 = Game(name = "Bang!", picture = "http://cf.geekdo-images.com/images/pic1170986_t.jpg", description = "The card game BANG! recreates an old-fashioned spaghetti western shoot-out, with each player randomly receiving a Character card to determine special abilities, and a secret Role card to determine their goal.", min_players = 4, max_players = 7, date_modified = datetime.now() - timedelta(days = random.randint(0, 50), seconds = random.randint(0, 3600 * 24)), categories = [party], user = user5)
s.add(game10)

s.commit()


print "added games!"
s.close()
