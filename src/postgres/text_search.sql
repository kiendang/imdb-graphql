ALTER TABLE titles DROP COLUMN IF EXISTS title_search_col;
ALTER TABLE titles ADD COLUMN title_search_col tsvector;

DROP INDEX IF EXISTS titles_text_search_idx;
CREATE INDEX titles_text_search_idx ON titles USING GIN (title_search_col);
UPDATE titles SET title_search_col =
    setweight(to_tsvector(coalesce(primaryTitle,'')), 'A') ||
    setweight(to_tsvector(coalesce(originalTitle,'')), 'C');

DROP FUNCTION IF EXISTS titles_trigger;
CREATE FUNCTION titles_trigger() RETURNS trigger AS $$
begin
    new.title_search_col :=
        setweight(to_tsvector('pg_catalog.english', coalesce(new.primaryTitle,'')), 'A') ||
        setweight(to_tsvector('pg_catalog.english', coalesce(new.originalTitle,'')), 'C');
    return new;
end
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS ts_vector_titles_trigger ON titles;
CREATE TRIGGER ts_vector_titles_trigger BEFORE INSERT OR UPDATE
    ON titles FOR EACH ROW EXECUTE PROCEDURE titles_trigger();
