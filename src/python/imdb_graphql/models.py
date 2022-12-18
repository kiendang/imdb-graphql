from sqlalchemy import case, Column, Integer, Float, ForeignKey, String, ARRAY
from sqlalchemy.orm import column_property, relationship
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
    rating = relationship('Rating', uselist=False)
    averageRating = association_proxy('rating', 'averageRating')
    numVotes = association_proxy('rating', 'numVotes')
    title_search_col = Column('title_search_col')

    __mapper_args__ = {'polymorphic_on': _type}


class Movie(Title):
    __mapper_args__ = {'polymorphic_identity': 'movie'}


class Series(Title):
    __mapper_args__ = {'polymorphic_identity': 'series'}

    episodes = relationship('EpisodeInfo')


class Episode(Title):
    __mapper_args__ = {'polymorphic_identity': 'episode'}

    info = relationship('EpisodeInfo', uselist=False)

    seasonNumber = association_proxy('info', 'seasonNumber')
    episodeNumber = association_proxy('info', 'episodeNumber')
    series = association_proxy('info', 'series')


class EpisodeInfo(Base):
    __tablename__ = 'episodes'

    imdbID = Column('tconst', String, ForeignKey(Episode.imdbID), primary_key=True)
    seriesID = Column('parenttconst', String)
    seasonNumber = Column('seasonnumber', Integer)
    episodeNumber = Column('episodenumber', Integer)
    series = relationship(
        'Series',
        foreign_keys=seriesID,
        primaryjoin='Series.imdbID == EpisodeInfo.seriesID'
    )


class Rating(Base):
    __tablename__ = 'ratings'

    imdbID = Column('tconst', String, ForeignKey(Title.imdbID), primary_key=True)
    averageRating = Column('averagerating', Float)
    numVotes = Column('numvotes', Integer)
