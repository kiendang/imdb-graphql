\cd :data_dir

\copy akas from program 'gzip -dc title.akas.tsv.gz' delimiter E'\t' null as '\N' csv header quote E'\b';
\copy people(nconst, primaryname, birthyear, deathyear, primaryprofession, knownfortitles) from program 'gzip -dc name.basics.tsv.gz' delimiter E'\t' null as '\N' csv header quote E'\b';
\copy principals from program 'gzip -dc title.principals.tsv.gz' delimiter E'\t' null as '\N' csv header quote E'\b';
\copy crew from program 'gzip -dc title.crew.tsv.gz' delimiter E'\t' null as '\N' csv header quote E'\b';
