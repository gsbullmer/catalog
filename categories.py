from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base

engine = create_engine('postgresql+psycopg2://ibgdb@/ibgdb')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a 'staging zone' for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
s = Session()


def addCategories():
    """Add Categories to database"""

    abstract_strategy = Category(
        name='Abstract Strategy Games', slug='abstract_strategy',
        description='like Chess or Go')
    s.add(abstract_strategy)

    customizable = Category(
        name='Customizable Games', slug='customizable',
        description='CCGs, CMGs, LCGs, etc')
    s.add(customizable)

    thematic = Category(
        name='Thematic Games', slug='thematic',
        description='emphasis on narrative')
    s.add(thematic)

    family = Category(
        name='Family Games', slug='family',
        description='fun for kids and adults')
    s.add(family)

    childrens = Category(
        name="Children's Games", slug='childrens',
        description='best for younger kids')
    s.add(childrens)

    party = Category(
        name='Party Games', slug='party',
        description='few rules, lots of laughs')
    s.add(party)

    strategy = Category(
        name='Strategy Games', slug='strategy',
        description='more complex games')
    s.add(strategy)

    wargames = Category(
        name='Wargames', slug='wargames',
        description='conflict simulation, etc.')
    s.add(wargames)

    s.commit()


addCategories()

print('Categories Initialized!')

s.close()
