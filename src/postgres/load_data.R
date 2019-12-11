library(DBI)
library(tidyverse)

source("utils.R")

data_dir <- file.path("..", "..", "data")
list.files(data_dir)

con <- dbConnect(RPostgreSQL::PostgreSQL(), dbname = "imdb")

dbSendQuery(con, "set search_path to imdb")

dbListTables(con)

titles <- read_data(file.path(data_dir, "title.basics.tsv")) %>%
    mutate_at(vars(genres), strsplit, ",")
head(titles)

copy_to(con, titles, "titles")

dbDisconnect(con)
