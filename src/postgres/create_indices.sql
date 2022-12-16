DROP INDEX IF EXISTS titles_idx01;
CREATE INDEX titles_idx01
  ON titles (tconst);


DROP INDEX IF EXISTS akas_idx01;
CREATE INDEX akas_idx01
  ON akas (titleId);

DROP INDEX IF EXISTS akas_idx02;
CREATE INDEX akas_idx02
  ON akas (titleId, ordering);


DROP INDEX IF EXISTS episodes_idx01;
CREATE INDEX episodes_idx01
  ON episodes (tconst);

DROP INDEX IF EXISTS episodes_idx02;
CREATE INDEX episodes_idx02
  ON episodes (parentTconst);


DROP INDEX IF EXISTS ratings_idx01;
CREATE INDEX ratings_idx01
  ON ratings (tconst);


DROP INDEX IF EXISTS people_idx01;
CREATE INDEX people_idx01
  ON people (nconst);


DROP INDEX IF EXISTS principals_idx01;
CREATE INDEX principals_idx01
  ON principals (tconst);

DROP INDEX IF EXISTS principals_idx02;
CREATE INDEX principals_idx02
  ON principals (tconst, ordering);


DROP INDEX IF EXISTS crew_idx01;
CREATE INDEX crew_idx01
  ON crew (tconst);
