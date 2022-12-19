ALTER TABLE titles
    ALTER COLUMN genres TYPE varchar(20)[]
    USING
        string_to_array(genres, ',')::varchar(20)[];
