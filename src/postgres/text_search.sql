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

ALTER TABLE people ADD COLUMN people_search_col tsvector;
UPDATE people SET people_search_col =
    to_tsvector('english', coalesce(primaryName,''));

CREATE INDEX people_idx ON people USING GIN (people_search_col);

CREATE TRIGGER ts_vector_people_update BEFORE INSERT OR UPDATE
    ON people FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(people_search_col, 'pg_catalog.english', primaryName);
