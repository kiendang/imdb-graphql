ALTER TABLE akas
    ALTER COLUMN types TYPE varchar(20)[]
    USING
        string_to_array(types, ',')::varchar(20)[],
    ALTER COLUMN attributes TYPE text[]
    USING
        string_to_array(attributes, ',');


ALTER TABLE people
    ALTER COLUMN primaryProfession TYPE varchar(50)[]
    USING
        string_to_array(primaryProfession, ',')::varchar(50)[],
    ALTER COLUMN knownForTitles TYPE char(10)[]
    USING
        string_to_array(knownForTitles, ',')::char(10)[];


ALTER TABLE crew
    ALTER COLUMN directors TYPE char(10)[]
    USING
        string_to_array(directors, ',')::char(10)[],
    ALTER COLUMN writers TYPE char(10)[]
    USING
        string_to_array(writers, ',')::char(10)[];
