import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


categories_games_table = Table(
    'categories_games',
    Base.metadata,
    Column('category_id', Integer, ForeignKey(
        'category.id', ondelete='CASCADE')),
    Column('game_id', Integer, ForeignKey('game.id', ondelete='CASCADE'))
)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(250))


class Category(Base):

    __tablename__ = 'category'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    slug = Column(String(80), unique=True)
    description = Column(String(80))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


class Game(Base):

    __tablename__ = 'game'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(5000))
    min_players = Column(Integer)
    max_players = Column(Integer)
    date_modified = Column(DateTime)
    picture = Column(String(250))

    # Many to One relationship
    categories = relationship(
        'Category',
        secondary='categories_games',
        backref=backref('games', order_by='Game.name'))

    # Many to One relationship
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('games'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'min_players': self.min_players,
            'max_players': self.min_players,
            'picture': self.picture,
            'categories': [c.serialize for c in self.categories],
            'date_modified': self.date_modified,
        }


engine = create_engine('postgresql+psycopg2://ibgdb@127.0.0.1/ibgdb')
Base.metadata.create_all(engine)
