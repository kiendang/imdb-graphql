import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.environ['DB_CONNECTION'])

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()


def init_db():
    from .models import Episode, EpisodeInfo, Movie, Rating, Series, Title

    Base.metadata.reflect(engine)
