import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.utils import get_session
from sqlalchemy import desc, distinct, func, select

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

    async def resolve_episodes(self, info, season=None):
        session = get_session(info.context)

        imdbid_filter = EpisodeInfoModel.series_id == self.imdb_id
        season_filter = (
            (EpisodeInfoModel.season_number.in_(season),)
            if season is not None
            else tuple()
        )

        return await session.scalars(
            Episode.get_query(info)
            .join(EpisodeModel.info)
            .filter(imdbid_filter, *season_filter)
            .order_by(EpisodeInfoModel.season_number, EpisodeInfoModel.episode_number)
        )

    async def resolve_total_seasons(self, info):
        session = get_session(info.context)
        return await session.scalar(
            select(func.count(distinct(EpisodeInfoModel.season_number))).filter(
                EpisodeInfoModel.series_id == self.imdb_id
            )
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

    async def resolve_title(self, info, imdb_id):
        session = get_session(info.context)
        return await session.scalar(
            select(TitleModel).filter_by(imdb_id=imdb_id).limit(1)
        )

    async def resolve_movie(self, info, imdb_id):
        session = get_session(info.context)
        return await session.scalar(
            Movie.get_query(info).filter_by(imdb_id=imdb_id).limit(1)
        )

    async def resolve_series(self, info, imdb_id):
        session = get_session(info.context)
        result = await session.scalar(
            Series.get_query(info).filter_by(imdb_id=imdb_id).limit(1)
        )
        return result

    async def resolve_episode(self, info, imdb_id):
        session = get_session(info.context)
        return await session.scalar(
            Episode.get_query(info).filter_by(imdb_id=imdb_id).limit(1)
        )

    async def resolve_search(self, info, title, types=None, result=None):
        session = get_session(info.context)

        tsquery = func.to_tsquery(f'\'{title}\'')
        title_search_filter = TitleModel.title_search_col.op('@@')(tsquery)
        type_filter = (
            (TitleModel._type.in_(t.value for t in types),)
            if types is not None
            else tuple()
        )

        return await session.scalars(
            select(TitleModel)
            .filter(title_search_filter, *type_filter)
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
