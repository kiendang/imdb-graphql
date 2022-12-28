# A GraphQL API for IMDB

### Schema
```graphql
schema {
  query: Query
}

type Query {
  title(imdbID: String!): Title
  movie(imdbID: String!): Movie
  series(imdbID: String!): Series
  episode(imdbID: String!): Episode
  search(title: String!, types: [TitleType], result: Int = 5): [Title]
}

interface Title {
  imdbID: String
  titleType: String
  primaryTitle: String
  originalTitle: String
  isAdult: Boolean
  startYear: Int
  endYear: Int
  runtime: Int
  genres: [String]
  averageRating: Float
  numVotes: Int
}

type Movie implements Title {
  imdbID: String
  titleType: String
  primaryTitle: String
  originalTitle: String
  isAdult: Boolean
  startYear: Int
  endYear: Int
  runtime: Int
  genres: [String]
  averageRating: Float
  numVotes: Int
}

type Series implements Title {
  imdbID: String
  titleType: String
  primaryTitle: String
  originalTitle: String
  isAdult: Boolean
  startYear: Int
  endYear: Int
  runtime: Int
  genres: [String]
  episodes(season: [Int]): [Episode]
  averageRating: Float
  numVotes: Int
  totalSeasons: Int
}

type Episode implements Title {
  imdbID: String
  titleType: String
  primaryTitle: String
  originalTitle: String
  isAdult: Boolean
  startYear: Int
  endYear: Int
  runtime: Int
  genres: [String]
  averageRating: Float
  numVotes: Int
  seasonNumber: Int
  episodeNumber: Int
  series: Series
}

enum TitleType {
  MOVIE
  SERIES
  EPISODE
}
```
