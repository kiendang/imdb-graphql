import graphene
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
    primaryTitle = graphene.String()
    originalTitle = graphene.String()
    isAdult = graphene.Int()
    startYear = graphene.Int()
    endYear = graphene.Int()
    runtime = graphene.Int()
    genres = graphene.List(graphene.String)
    averageRating = graphene.Float()
    numVotes = graphene.Int()

class Movie(graphene.ObjectType):
    class Meta:
        interfaces = (Title, )

class Episode(graphene.ObjectType):
    class Meta:
        interfaces = (Title, )

    seasonNumber = graphene.Int()
    episodeNumber = graphene.Int()

class Series(graphene.ObjectType):
    class Meta:
        interfaces = (Title, )

    episodes = graphene.List(Episode)

    def resolve_episodes(self, info):
        return(
            session
            .query(EpisodeModel)
            .join(EpisodeModel.info)
            .filter_by(seriesID=self.imdbID)
            .order_by(
                EpisodeInfoModel.seasonNumber,
                EpisodeInfoModel.episodeNumber
            )
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

        if u.type == 'series':
            res = query_to_item(Series, u, info)
        elif u.type == 'episode':
            res = query_to_item(Episode, u, info)
        else:
            res = query_to_item(Movie, u, info)

        return res

    def resolve_movie(self, info, imdbID):
        return session.query(MovieModel).filter_by(imdbID=imdbID).first()

    def resolve_series(self, info, imdbID):
        return session.query(SeriesModel).filter_by(imdbID=imdbID).first()

    def resolve_episode(self, info, imdbID):
        return session.query(EpisodeModel).filter_by(imdbID=imdbID).first()

    def resolve_search(sef, info, title, result):
        tsquery = func.to_tsquery(f'\'{title}\'')
        query = (
            session
            .query(TitleModel)
            .filter(TitleModel.title_search_col.op('@@')(tsquery))
            .join(TitleModel.rating)
            .order_by(
                desc(RatingModel.numVotes),
                desc(TitleModel.primaryTitle.ilike(f'\'{title}\'')),
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
