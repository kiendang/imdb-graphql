from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://imdb:@/imdb')

session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

Base = declarative_base()
Base.query = session.query_property()


def init_db():
    from models import Title, Movie, Series, Episode, EpisodeInfo, Rating
    Base.metadata.reflect(engine)
