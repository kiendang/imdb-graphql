from enum import Enum

from sqlalchemy import ARRAY, Column, Float, ForeignKey, Integer, String, case
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import column_property, relationship

from .database import Base


class TitleType(Enum):
    MOVIE = 'movie'
    SERIES = 'series'
    EPISODE = 'episode'


class Title(Base):
    __tablename__ = 'titles'

    imdb_id = Column('tconst', String, primary_key=True)
    title_type = Column('titletype', String)
    _type = column_property(
        case(
            {'tvSeries': 'series', 'tvMiniSeries': 'series', 'tvEpisode': 'episode'},
            value=title_type,
            else_='movie',
        )
    )
    primary_title = Column('primarytitle', String)
    original_title = Column('originaltitle', String)
    is_adult = Column('isadult', Integer)
    start_year = Column('startyear', Integer)
    end_year = Column('endyear', Integer)
    runtime = Column('runtimeminutes', Integer)
    genres = Column('genres', ARRAY(String))
    rating = relationship(lambda: Rating, uselist=False)
    average_rating = association_proxy('rating', 'average_rating')
    num_votes = association_proxy('rating', 'num_votes')
    title_search_col = Column('title_search_col')

    __mapper_args__ = {'polymorphic_on': _type}


class Movie(Title):
    __mapper_args__ = {'polymorphic_identity': 'movie'}


class Series(Title):
    __mapper_args__ = {'polymorphic_identity': 'series'}

    episodes = relationship(lambda: EpisodeInfo)


class Episode(Title):
    __mapper_args__ = {'polymorphic_identity': 'episode'}

    info = relationship(lambda: EpisodeInfo, uselist=False)

    season_number = association_proxy('info', 'season_number')
    episode_number = association_proxy('info', 'episode_number')
    series = association_proxy('info', 'series')


class EpisodeInfo(Base):
    __tablename__ = 'episodes'

    imdb_id = Column('tconst', String, ForeignKey(Episode.imdb_id), primary_key=True)
    series_id = Column('parenttconst', String)
    season_number = Column('seasonnumber', Integer)
    episode_number = Column('episodenumber', Integer)
    series = relationship(
        Series, foreign_keys=series_id, primaryjoin=Series.imdb_id == series_id
    )


class Rating(Base):
    __tablename__ = 'ratings'

    imdb_id = Column('tconst', String, ForeignKey(Title.imdb_id), primary_key=True)
    average_rating = Column('averagerating', Float)
    num_votes = Column('numvotes', Integer)
