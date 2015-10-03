import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()

# Association table for Category/Game relationships
categories_games_table = Table('categories_games', Base.metadata,
    Column('category_id', Integer, ForeignKey('category.id')),
    Column('game_id', Integer, ForeignKey('game.id'))
)

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(80), nullable = False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
        }

class Category(Base):

    __tablename__ = 'category'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    # One to Many relationship
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref = "categories")

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }

class Game(Base):

    __tablename__ = 'game'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    min_players = Column(Integer)
    max_players = Column(Integer)
    date_added = Column(Datetime)
    picture = Column(String(250))

    # Many to Many relationship
    categories = relationship("Category",
        secondary = "categories_games",
        backref = "games")

    # One to One relationship
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref = "games")

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'min_players': self.min_players,
            'max_players': self.min_players,
            'picture': self.picture,
            'categories': self.categories,
        }


engine = create_engine('postgresql:///catalog')
Base.metadata.create_all(engine)
