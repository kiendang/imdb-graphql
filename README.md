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
  search(title: String!, result: Int = 5): [Title]
}

interface Title {
  imdbID: String
  titleType: String
  primaryTitle: String
  originalTitle: String
  isAdult: Int
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
  isAdult: Int
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
  isAdult: Int
  startYear: Int
  endYear: Int
  runtime: Int
  genres: [String]
  averageRating: Float
  numVotes: Int
  episodes(season: [Int]): [Episode]
  totalSeasons: Int
}

type Episode implements Title {
  imdbID: String
  titleType: String
  primaryTitle: String
  originalTitle: String
  isAdult: Int
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
```
