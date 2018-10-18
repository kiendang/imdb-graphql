import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import func, desc

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
    series = graphene.Field(lambda: Series)

class Series(SQLAlchemyObjectType):
    class Meta:
        model = SeriesModel
        interfaces = (Title, )
        exclude_fields = exclude_fields

    episodes = graphene.Field(graphene.List(Episode), season=graphene.Int())
    totalSeasons = graphene.Int()

    def resolve_episodes(self, info, **args):
        q = (
            Episode
            .get_query(info)
            .join(EpisodeModel.info)
            .filter_by(seriesID=self.imdbID)
        )

        q = (
            q
            .filter_by(seasonNumber=args['season'])
            .order_by(EpisodeInfoModel.episodeNumber)
        ) if 'season' in args else (
            q.order_by(EpisodeInfoModel.seasonNumber,
                EpisodeInfoModel.episodeNumber)
        )
        
        return q

    def resolve_totalSeasons(self, info):
        return(
            session
            .query(EpisodeInfoModel.seasonNumber)
            .filter_by(seriesID=self.imdbID)
            .group_by(EpisodeInfoModel.seasonNumber)
            .count()
        )

class Query(graphene.ObjectType):
    title = graphene.Field(Title, imdbID=graphene.String(required=True))
    movie = graphene.Field(Movie, imdbID=graphene.String(required=True))
    series = graphene.Field(Series, imdbID=graphene.String(required=True))
    episode = graphene.Field(Episode, imdbID=graphene.String(required=True))
    search = graphene.Field(
        graphene.List(Title),
        title=graphene.String(required=True),
        result=graphene.Int(default_value=5)
    )

    def resolve_title(self, info, imdbID):
        return session.query(TitleModel).filter_by(imdbID=imdbID).first()

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
