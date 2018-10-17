#' ---
#' jupyter:
#'   jupytext_format_version: '1.0'
#'   kernelspec:
#'     display_name: R
#'     language: R
#'     name: ir
#'   language_info:
#'     codemirror_mode: r
#'     file_extension: .r
#'     mimetype: text/x-r-source
#'     name: R
#'     pygments_lexer: r
#'     version: 3.5.1
#' ---

library(tidyverse)

source("read_imdb.R")

data_dir <- file.path("..", "..", "data")

list.files(data_dir)

pg_array <- function(x) ifelse(is.na(x) | x == "", NA, sprintf("{{%s}}", x))

pg_format_titles <- function(df) df %>% mutate_at(vars(genres), pg_array)

pg_format_akas <- function(df) {
    df %>%
        mutate_at(vars(attributes), ~ gsub("\002", ",", .x)) %>%
        mutate_at(vars(attributes, types), pg_array)
}

pg_format_people <- function(df) {
    df %>% mutate_at(vars(primaryProfession, knownForTitles), pg_array)
}

pg_format_principals <- function(df) {
    df %>% mutate_at(vars(characters), ~ gsub("\\\"|\\]|\\[", "", .x))
}

pg_format_crew <- function(df) {
    df %>% mutate_at(vars(directors, writers), pg_array)
}

pg_import_format <- function(df, type) {
    if (! type %in% types) {
        stop("type must be one of %s", paste(types, collapse=","))
    }
    
    if (type == "titles") pg_format_titles(df)
    else if (type == "akas") pg_format_akas(df)
    else if (type == "people") pg_format_people(df)
    else if (type == "principals") pg_format_principals(df)
    else if (type == "crew") pg_format_crew(df)
    else df
}

file_names <- types %>%
    setNames(., .) %>%
    imap_chr(~ case_when(
        .y %in% c("titles", "people") ~ "basics",
        .y == "episodes" ~ "episode",
        TRUE ~ .x
    )) %>%
    imap_chr(function(v, k) {
        prefix <- case_when(
            k == "people" ~ "name",
            TRUE ~ "title"
        )
        
        sprintf("%s.%s", prefix, v)
    }) %>%
    map_chr(~ sprintf("%s.tsv", .x))

file_names

data <- file_names %>% map(~ file.path(data_dir, .x) %>% read_imdb_tsv)

data_formatted <- imap(data, pg_import_format)

write_imdb <- function(x, file) {
    data.table::fwrite(x, file, sep="\t", quote=FALSE, na="NULL")
}

data_formatted %>% iwalk(~ write_imdb(.x, sprintf("%s.tsv", .y)))
