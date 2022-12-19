DROP TABLE IF EXISTS titles CASCADE;
CREATE TABLE titles (
    tconst char(10) primary key,
    titleType varchar(20),
    primaryTitle text,
    originalTitle text,
    isAdult boolean,
    startYear smallint,
    endYear smallint,
    runtimeMinutes integer,
    genres text
);


DROP TABLE IF EXISTS episodes CASCADE;
CREATE TABLE episodes (
    tconst char(10) primary key,
    parentTconst char(10),
    seasonNumber integer,
    episodeNumber integer
);


DROP TABLE IF EXISTS ratings CASCADE;
CREATE TABLE ratings (
    tconst char(10) primary key,
    averageRating real,
    numVotes integer
);
