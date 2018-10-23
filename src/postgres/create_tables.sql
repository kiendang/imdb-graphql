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

ALTER TABLE titles ADD COLUMN title_search_col tsvector;
UPDATE titles SET title_search_col =
    to_tsvector('english', coalesce(primaryTitle,'') || ' ' || coalesce(originalTitle,''));

CREATE INDEX title_idx ON titles USING GIN (title_search_col);
UPDATE titles SET title_search_col =
    setweight(to_tsvector(coalesce(primaryTitle,'')), 'A') ||
    setweight(to_tsvector(coalesce(originalTitle,'')), 'C');

CREATE FUNCTION titles_trigger() RETURNS trigger AS $$
begin
  new.title_search_col :=
     setweight(to_tsvector('pg_catalog.english', coalesce(new.primaryTitle,'')), 'A') ||
     setweight(to_tsvector('pg_catalog.english', coalesce(new.originalTitle,'')), 'C');
  return new;
end
$$ LANGUAGE plpgsql;

CREATE TRIGGER ts_vector_titles_trigger BEFORE INSERT OR UPDATE
    ON titles FOR EACH ROW EXECUTE PROCEDURE titles_trigger();


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

ALTER TABLE people ADD COLUMN people_search_col tsvector;
UPDATE people SET people_search_col =
    to_tsvector('english', coalesce(primaryName,''));

CREATE INDEX people_idx ON people USING GIN (people_search_col);

CREATE TRIGGER ts_vector_people_update BEFORE INSERT OR UPDATE
    ON people FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(people_search_col, 'pg_catalog.english', primaryName);


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
