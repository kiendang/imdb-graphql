\cd :data_dir

\copy titles(tconst, titletype, primarytitle, originaltitle, isadult, startyear, endyear, runtimeminutes, genres) from program 'gzip -dc titles.basics.tsv.gz' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy akas from program 'gzip -dc title.akas.tsv.gz' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy episodes from program 'gzip -dc title.episode.tsv.gz' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy ratings from program 'gzip -dc title.ratings.tsv.gz' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy people(nconst, primaryname, birthyear, deathyear, primaryprofession, knownfortitles) from program 'gzip -dc name.basics.tsv.gz' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy principals from program 'gzip -dc title.principals.tsv.gz' delimiter E'\t' null as 'NULL' csv header quote E'\b';
\copy crew from program 'gzip -dc title.crew.tsv.gz' delimiter E'\t' null as 'NULL' csv header quote E'\b';
