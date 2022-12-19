DROP TABLE IF EXISTS akas CASCADE;
CREATE TABLE akas (
    titleId char(10),
    ordering smallint,
    title text,
    region varchar(10),
    language varchar(10),
    types text,
    attributes text,
    isOriginalTitle smallint,
    constraint akas_pk primary key (titleId, ordering)
);


DROP TABLE IF EXISTS people CASCADE;
CREATE TABLE people (
    nconst char(10) primary key,
    primaryName text,
    birthYear smallint,
    deathYear smallint,
    primaryProfession text,
    knownForTitles text
);


DROP TABLE IF EXISTS principals CASCADE;
CREATE TABLE principals (
    tconst char(10),
    ordering integer,
    nconst varchar(10),
    category varchar(20),
    job text,
    character text,
    constraint principals_pk primary key (tconst, ordering)
);


DROP TABLE IF EXISTS crew CASCADE;
CREATE TABLE crew (
    tconst char(10) primary key,
    directors text,
    writers text
);
