import os
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(os.environ['DB_CONNECTION'])

SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
session = async_scoped_session(
    SessionLocal,
    scopefunc=current_task,
)

Base = declarative_base()


def init_db():
    from .models import Episode, EpisodeInfo, Movie, Rating, Series, Title

    Base.metadata.reflect(engine)
