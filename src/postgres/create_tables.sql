DROP TABLE IF EXISTS titles CASCADE;
CREATE TABLE titles (
    tconst char(9) primary key,
    titleType varchar(20),
    primaryTitle text,
    originalTitle text,
    isAdult smallint,
    startYear smallint,
    endYear smallint,
    runtimeMinutes integer,
    genres varchar(20)[]
);


DROP TABLE IF EXISTS akas CASCADE;
CREATE TABLE akas (
    titleId char(9),
    ordering smallint,
    title text,
    region varchar(10),
    language varchar(10),
    types varchar(20)[],
    attributes text[],
    isOriginalTitle smallint
);


DROP TABLE IF EXISTS episodes CASCADE;
CREATE TABLE episodes (
    tconst char(9) unique,
    parentTconst char(9),
    seasonNumber integer,
    episodeNumber integer
);


DROP TABLE IF EXISTS ratings CASCADE;
CREATE TABLE ratings (
    tconst char(9) unique,
    averageRating double precision,
    numVotes integer
);


DROP TABLE IF EXISTS people CASCADE;
CREATE TABLE people (
    nconst varchar(10) primary key,
    primaryName text,
    birthYear smallint,
    deathYear smallint,
    primaryProfession varchar(50)[],
    knownForTitles char(9)[]
);


DROP TABLE IF EXISTS principals CASCADE;
CREATE TABLE principals (
    tconst char(9),
    ordering integer,
    nconst varchar(10),
    category varchar(20),
    job text,
    character text
);


DROP TABLE IF EXISTS crew CASCADE;
CREATE TABLE crew (
    tconst char(9) unique,
    directors varchar(10)[],
    writers varchar(10)[]
);
