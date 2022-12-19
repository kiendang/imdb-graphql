DROP INDEX IF EXISTS titles_idx01;
CREATE INDEX titles_idx01
  ON titles (tconst);


DROP INDEX IF EXISTS episodes_idx01;
CREATE INDEX episodes_idx01
  ON episodes (tconst);

DROP INDEX IF EXISTS episodes_idx02;
CREATE INDEX episodes_idx02
  ON episodes (parentTconst);


DROP INDEX IF EXISTS ratings_idx01;
CREATE INDEX ratings_idx01
  ON ratings (tconst);
