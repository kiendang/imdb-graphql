Download data from https://www.imdb.com/interfaces/, create a PostgreSQL database and run the sql files in the following order,

- `create_table.sql`
- `load_tables.sql`: `psql -f load_tables.sql -v data_dir=<path-to-directory-containing-data>`
- `format_tables.sql`: some transformations, *e.g.* converting comma separated text fields to arrays
- `create_indices.sql`
- `text_search.sql`

To set db name, user name, search path (default schema(s)),

```sh
psql 'dbname=imdb user=imdb options=--search-path=imdb' -f <sql-file>
```
