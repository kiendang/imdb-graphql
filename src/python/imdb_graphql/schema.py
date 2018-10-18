import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import func, desc, Integer, cast

from .models import (
    Title as TitleModel,
    Movie as MovieModel,
    Series as SeriesModel,
    Episode as EpisodeModel,
    EpisodeInfo as EpisodeInfoModel,
    Rating as RatingModel
)
from .database import session
from .get_fields import get_fields


class Title(graphene.Interface):
    imdbID = graphene.String()
    titleType = graphene.String()
    primaryTitle = graphene.String()
    originalTitle = graphene.String()
    isAdult = graphene.Int()
    startYear = graphene.Int()
    endYear = graphene.Int()
    runtime = graphene.Int()
    genres = graphene.List(graphene.String)
    averageRating = graphene.Float()
    numVotes = graphene.Int()

exclude_fields = ('title_search_col', '_type', )

class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel
        interfaces = (Title, )
        exclude_fields = exclude_fields

class Episode(SQLAlchemyObjectType):
    class Meta:
        model = EpisodeModel
        interfaces = (Title, )
        exclude_fields = exclude_fields

    seasonNumber = graphene.Int()
    episodeNumber = graphene.Int()

class Series(SQLAlchemyObjectType):
    class Meta:
        model = SeriesModel
        interfaces = (Title, )
        exclude_fields = exclude_fields

    episodes = graphene.List(Episode)

    def resolve_episodes(self, info):
        return(
            Episode
            .get_query(info)
            .join(EpisodeModel.info)
            .filter_by(seriesID=self.imdbID)
            .order_by(EpisodeInfoModel.seasonNumber,
                EpisodeInfoModel.episodeNumber)
        )

class Query(graphene.ObjectType):
    title = graphene.Field(Title, imdbID=graphene.String())
    movie = graphene.Field(Movie, imdbID=graphene.String())
    series = graphene.Field(Series, imdbID=graphene.String())
    episode = graphene.Field(Episode, imdbID=graphene.String())
    search = graphene.Field(
        graphene.List(Movie),
        title=graphene.String(),
        result=graphene.Int()
    )

    def resolve_title(self, info, imdbID):
        u = session.query(TitleModel).filter_by(imdbID=imdbID).first()

        if u._type == 'series':
            res = query_to_item(Series, u, info)
        elif u._type == 'episode':
            res = query_to_item(Episode, u, info)
        else:
            res = query_to_item(Movie, u, info)

        return res

    def resolve_movie(self, info, imdbID):
        return Movie.get_query(info).filter_by(imdbID=imdbID).first()

    def resolve_series(self, info, imdbID):
        return Series.get_query(info).filter_by(imdbID=imdbID).first()

    def resolve_episode(self, info, imdbID):
        return Episode.get_query(info).filter_by(imdbID=imdbID).first()

    def resolve_search(sef, info, title, result):
        tsquery = func.to_tsquery(f'\'{title}\'')
        query = (
            session
            .query(TitleModel)
            .filter(TitleModel.title_search_col.op('@@')(tsquery))
            .join(TitleModel.rating)
            .order_by(
                desc(RatingModel.numVotes >= 1000),
                desc(TitleModel.primaryTitle.ilike(title)),
                desc(RatingModel.numVotes),
                desc(func.ts_rank_cd(TitleModel.title_search_col, tsquery, 1))
            )
            .limit(result)
        )
        return query.all()

def query_to_item(cls, res, info):
    model_fields = dir(res) 
    schema_fields = (x[0] for x in cls._meta.fields.items())
    info_fields = get_fields(info)
    fields = set(info_fields) & set(schema_fields) & set(model_fields)
    mappings = {k: res.__getattribute__(k) for k in fields}
    return cls(**mappings)

schema = graphene.Schema(query=Query, types = [Movie, Series, Episode])
