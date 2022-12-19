ALTER TABLE people ADD COLUMN people_search_col tsvector;
UPDATE people SET people_search_col =
    to_tsvector('english', coalesce(primaryName,''));

CREATE INDEX people_text_search_idx ON people USING GIN (people_search_col);

CREATE TRIGGER ts_vector_people_update BEFORE INSERT OR UPDATE
    ON people FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(people_search_col, 'pg_catalog.english', primaryName);
