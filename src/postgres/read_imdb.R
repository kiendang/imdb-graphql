read_imdb_tsv <- function(file) {
    data.table::fread(file, quote="", na="\\N", data.table=FALSE)
}

types <- c("titles", "akas", "episodes", "ratings", "people", "principals", "crew")

read_imdb <- function(file, type) {
    if (! type %in% types) {
        stop("type must be one of %s", paste(types, collapse=","))
    }

    df <- file %>% read_imdb_tsv

    if (type == "titles") {
        df %>% mutate_at(vars(genres), strsplit, ",")
    } else if (type == "akas") {
        df %>%
            mutate_at(vars(types), strsplit, ",") %>%
            mutate_at(vars(attributes), strsplit, "\002")
    } else if (type == "people") {
        df %>% mutate_at(vars(primaryProfession, knownForTitles), strsplit, split=",")
    } else if (type == "principals") {
        df %>% mutate_at(vars(characters), ~ gsub("\\\"|\\]|\\[", "", .x))
    } else {
        df
    }
}
