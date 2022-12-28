import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import desc, func

from .models import (
    Episode as EpisodeModel,
    EpisodeInfo as EpisodeInfoModel,
    Movie as MovieModel,
    Rating as RatingModel,
    Series as SeriesModel,
    Title as TitleModel,
    TitleType as TitleTypeEnum,
)

TitleType = graphene.Enum.from_enum(TitleTypeEnum)


class Title(graphene.Interface):
    imdb_id = graphene.String(name="imdbID")
    title_type = graphene.String()
    primary_title = graphene.String()
    original_title = graphene.String()
    is_adult = graphene.Boolean()
    start_year = graphene.Int()
    end_year = graphene.Int()
    runtime = graphene.Int()
    genres = graphene.List(graphene.String)
    average_rating = graphene.Float()
    num_votes = graphene.Int()


exclude_fields = (
    'title_search_col',
    '_type',
)


class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel
        interfaces = (Title,)
        exclude_fields = exclude_fields


class Episode(SQLAlchemyObjectType):
    class Meta:
        model = EpisodeModel
        interfaces = (Title,)
        exclude_fields = exclude_fields

    season_number = graphene.Int()
    episode_number = graphene.Int()
    series = graphene.Field(lambda: Series)


class Series(SQLAlchemyObjectType):
    class Meta:
        model = SeriesModel
        interfaces = (Title,)
        exclude_fields = exclude_fields

    total_seasons = graphene.Int()
    episodes = graphene.Field(
        graphene.List(Episode), season=graphene.List(graphene.Int)
    )

    def resolve_episodes(self, info, season=None):
        imdbid_filter = EpisodeInfoModel.series_id == self.imdb_id
        season_filter = (
            (EpisodeInfoModel.season_number.in_(season),)
            if season is not None
            else tuple()
        )

        return (
            Episode.get_query(info)
            .join(EpisodeModel.info)
            .filter(imdbid_filter, *season_filter)
            .order_by(EpisodeInfoModel.season_number, EpisodeInfoModel.episode_number)
        )

    def resolve_totalSeasons(self, info):
        return (
            EpisodeInfoModel.query.with_entities(EpisodeInfoModel.season_number)
            .filter_by(series_id=self.imdb_id)
            .group_by(EpisodeInfoModel.season_number)
            .count()
        )


class Query(graphene.ObjectType):
    title = graphene.Field(Title, imdb_id=graphene.String(name='imdbID', required=True))
    movie = graphene.Field(Movie, imdb_id=graphene.String(name='imdbID', required=True))
    series = graphene.Field(
        Series, imdb_id=graphene.String(name='imdbID', required=True)
    )
    episode = graphene.Field(
        Episode, imdb_id=graphene.String(name='imdbID', required=True)
    )
    search = graphene.Field(
        graphene.List(Title),
        title=graphene.String(required=True),
        types=graphene.List(TitleType),
        result=graphene.Int(default_value=5),
    )

    def resolve_title(self, info, imdb_id):
        return TitleModel.query.filter_by(imdb_id=imdb_id).first()

    def resolve_movie(self, info, imdb_id):
        return Movie.get_query(info).filter_by(imdb_id=imdb_id).first()

    def resolve_series(self, info, imdb_id):
        return Series.get_query(info).filter_by(imdb_id=imdb_id).first()

    def resolve_episode(self, info, imdb_id):
        return Episode.get_query(info).filter_by(imdb_id=imdb_id).first()

    def resolve_search(self, info, title, types=None, result=None):
        tsquery = func.to_tsquery(f'\'{title}\'')
        title_search_filter = TitleModel.title_search_col.op('@@')(tsquery)
        type_filter = (TitleModel._type.in_(types),) if types is not None else tuple()

        return (
            TitleModel.query.filter(title_search_filter, *type_filter)
            .join(TitleModel.rating)
            .order_by(
                desc(RatingModel.num_votes >= 1000),
                desc(TitleModel.primary_title.ilike(f'%{title}%')),
                desc(RatingModel.num_votes),
                desc(func.ts_rank_cd(TitleModel.title_search_col, tsquery, 1)),
            )
            .limit(result)
        )


schema = graphene.Schema(query=Query, types=[Movie, Series, Episode])
