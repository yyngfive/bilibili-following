library(tidyverse)
library(RColorBrewer)
library(ggsci)
df <- read.csv("./UPs.csv", colClasses = c("uid" = "character", "time" = "Date", "special" = "factor", "first" = "Date", "newest" = "Date", "update" = "factor", "watch" = "factor"), encoding = "UTF-8")
View(df)
df <- as_tibble(df)
str(df)

fans_lavels <- c(
    "0-100",
    "100-1000",
    "1000-1万",
    "1万-10万",
    "10万-100万",
    ">100万"
)

get_fans_level <- function(number) {
    if (number > 1000000) {
        level <- 6
    } else if (number > 100000) {
        level <- 5
    } else if (number > 10000) {
        level <- 4
    } else if (number > 1000) {
        level <- 3
    } else if (number > 100) {
        level <- 2
    } else {
        level <- 1
    }
    return(level)
}

df <- df %>% mutate(single_field = str_split(df$field, ",", simplify = T)[, 1])

df$fans_level <- df %>%
    select(fans) %>%
    apply(1, get_fans_level)

df$single_field <- df$single_field %>% as.factor()
df$fans_level <- df$fans_level %>% as.factor()
str(df)
two_fields <- df %>%
    filter_at(vars(field), all_vars(str_detect(., pattern = ",")))
num_two <- two_fields %>%
    dim() %>%
    .[1]
num_one <- df %>%
    dim() %>%
    .[1] - num_two
num_two
num_one
pie(c(num_one, num_two), labels = c("", "在两个分区发布视频"), border = "white", col = pal_npg("nrc", alpha = 0.7)(2))

ggplot(data = two_fields, aes(x = fans_level, fill = fans_level)) +
    geom_bar() +
    scale_fill_npg()

library(treemap)
treemap(df, index = "single_field", vSize = "fans")

two_fields_56  <-  two_fields %>% filter(fans_level == 5 | fans_level == 6)
two_fields_56
