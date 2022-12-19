\cd :data_dir

\copy titles(tconst, titletype, primarytitle, originaltitle, isadult, startyear, endyear, runtimeminutes, genres) from program 'gzip -dc title.basics.tsv.gz' delimiter E'\t' null as '\N' csv header quote E'\b';
\copy episodes from program 'gzip -dc title.episode.tsv.gz' delimiter E'\t' null as '\N' csv header quote E'\b';
\copy ratings from program 'gzip -dc title.ratings.tsv.gz' delimiter E'\t' null as '\N' csv header quote E'\b';
