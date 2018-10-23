from sqlalchemy import case, Column, Integer, Float, String, ARRAY
from sqlalchemy.orm import column_property, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from enum import Enum

from .database import Base


class TitleType(Enum):
    MOVIE = 'movie'
    SERIES = 'series'
    EPISODE = 'episode'


class Title(Base):
    __tablename__ = 'titles'

    imdbID = Column('tconst', String, primary_key=True)
    titleType = Column('titletype', String)
    _type = column_property(
        case(
            {
                'tvSeries': 'series',
                'tvMiniSeries': 'series',
                'tvEpisode': 'episode'
            },
            value=titleType,
            else_='movie'
        )
    )
    primaryTitle = Column('primarytitle', String)
    originalTitle = Column('originaltitle', String)
    isAdult = Column('isadult', Integer)
    startYear = Column('startyear', Integer)
    endYear = Column('endyear', Integer)
    runtime = Column('runtimeminutes', Integer)
    genres = Column('genres', ARRAY(String))
    rating = relationship(
        'Rating',
        foreign_keys=imdbID,
        primaryjoin='Title.imdbID == Rating.imdbID',
        backref=backref('title', uselist=False)
    )
    averageRating = association_proxy('rating', 'averageRating')
    numVotes = association_proxy('rating', 'numVotes')
    title_search_col = Column('title_search_col')

    __mapper_args__ = {'polymorphic_on': _type}


class Movie(Title):
    __mapper_args__ = {'polymorphic_identity': 'movie'}


class Series(Title):
    __mapper_args__ = {'polymorphic_identity': 'series'}

    episodes = association_proxy('_episodes', 'episode')


class Episode(Title):
    __mapper_args__ = {'polymorphic_identity': 'episode'}

    info = relationship(
        'EpisodeInfo',
        foreign_keys='Episode.imdbID',
        primaryjoin='Episode.imdbID == EpisodeInfo.imdbID',
        backref=backref('episode', uselist=False)
    )

    seasonNumber = association_proxy('info', 'seasonNumber')
    episodeNumber = association_proxy('info', 'episodeNumber')
    series = association_proxy('info', 'series')


class EpisodeInfo(Base):
    __tablename__ = 'episodes'

    imdbID = Column('tconst', String, primary_key=True)
    seriesID = Column('parenttconst', String)
    seasonNumber = Column('seasonnumber', Integer)
    episodeNumber = Column('episodenumber', Integer)
    series = relationship(
        'Series',
        foreign_keys=seriesID,
        primaryjoin='Series.imdbID == EpisodeInfo.seriesID',
        backref=backref('_episodes', uselist=True)
    )


class Rating(Base):
    __tablename__ = 'ratings'

    imdbID = Column('tconst', String, primary_key=True)
    averageRating = Column('averagerating', Float)
    numVotes = Column('numvotes', Integer)
