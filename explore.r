library(tidyverse)
library(RColorBrewer)
library(ggsci)
df <- read.csv("./UPs.csv",
    colClasses = c(
        "uid" = "character",
        "time" = "Date",
        "special" = "factor",
        "first" = "Date",
        "newest" = "Date",
        "update" = "factor",
        "watch" = "factor"
    ),
    encoding = "UTF-8"
)
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

library(hrbrthemes)

pie(c(num_one, num_two),
    labels = c("", "在两个分区发布视频"),
    border = "white",
    col = pal_npg("nrc", alpha = 0.7)(2)
)

ggplot(data = two_fields, aes(x = fans_level, fill = fans_level)) +
    geom_bar() +
    scale_fill_npg()

library(treemap)
treemap(
    table(df$single_field) %>%
        as.data.frame(),
    index = "Var1", vSize = "Freq"
)

two_fields_56 <- two_fields %>% filter(fans_level == 5 | fans_level == 6)
two_fields_56
main_fields <- two_fields_56$single_field %>%
    as.character() %>%
    as.factor()
second_fields <- str_split(two_fields_56$field,
    ",",
    simplify = T
)[, 2] %>%
    as.factor()

data_56 <- expand.grid(x = levels(main_fields), y = levels(second_fields))
data_56$z <- table(two_fields_56$field) %>%
    .[paste(data_56$x, data_56$y, sep = ",")] %>%
    as.numeric()
data_56$z[is.na(data_56$z)] <- 0
data_56 <- as_tibble(data_56)
data_56
ggplot(data_56, aes(x = x, y = y, fill = z)) +
    geom_tile() +
    scale_fill_material("blue")

ggplot(table(two_fields_56$field) %>%
    as.data.frame(), aes(x = reorder(Var1, Freq), y = Freq)) +
    geom_segment(
        aes(
            x = reorder(Var1, Freq),
            xend = reorder(Var1, Freq),
            y = 0,
            yend = Freq
        ),
        col = "grey"
    ) +
    geom_point(color = "orange", size = 4) +
    theme_ipsum()

library(ggradar)

table_to_radar <- function(table) {
    table %>%
        as.data.frame.array() %>%
        t() %>%
        apply(2, function(x) x / sum(.)) %>%
        as.data.frame() %>%
        t() %>%
        as_tibble() %>%
        add_column(group = "Radar", .before = colnames(.)[1])
}

table(df$single_field) %>%
    table_to_radar() %>%
    ggradar() +
    scale_color_npg()

field_video <- c("电影", "纪录片", "影视", "动画", "国创")
field_entertainment <- c("音乐", "舞蹈", "游戏", "鬼畜", "娱乐")
field_knowledge <- c("知识", "科技", "资讯")
field_life <- c("生活", "美食", "动物圈", "汽车", "时尚", "运动")

df$big_field <- df %>%
    select(single_field) %>%
    apply(1, function(x) {
        if (x %in% field_video) {
            res <- "video"
        } else if (x %in% field_entertainment) {
            res <- "entertainment"
        } else if (x %in% field_knowledge) {
            res <- "knowledge"
        } else if (x %in% field_life) {
            res <- "life"
        } else {
            res <- "none"
        }
        return(res)
    })

df$big_field %>%
    table() %>%
    table_to_radar() %>%
    select(!none) %>%
    rename(泛影视 = video, 泛娱乐 = entertainment, 泛知识 = knowledge, 泛生活 = life) %>%
    ggradar() +
    scale_color_npg()

df %>%
    select(fans, big_field) %>%
    filter(big_field != "none") %>%
    ggplot(aes(x = big_field, y = log10(fans), fill = big_field)) +
    geom_boxplot() +
    theme_ipsum() +
    scale_fill_npg()

df$view_mean <- df$view / df$total
df$likes_mean <- df$likes / df$total
df$view_mean[is.infinite(df$view_mean)] <- 0
df$view_mean[is.nan(df$view_mean)] <- 0
df$likes_mean[is.infinite(df$likes_mean)] <- 0
df %>% ggplot(aes(x = log(view), y = log(likes))) +
    geom_point()
df %>% ggplot(aes(x = log(view), y = log(likes), col = big_field)) +
    geom_point() +
    theme_ipsum() +
    scale_color_npg()

df %>% ggplot(aes(x = log(fans), y = log(view))) +
    geom_point()

df %>% ggplot(aes(x = log10(total), y = log10(view_mean), col = big_field)) +
    geom_point() +
    theme_ipsum() +
    scale_color_npg()

df %>% ggplot(aes(x = log10(fans), y = log10(view_mean))) +
    geom_point()

ggplot(df, aes(x = fans_level, y = view_mean, fill = fans_level)) +
    geom_boxplot() +
    theme_ipsum() +
    scale_fill_npg()
library(gt)
library(gtExtras)
library(formattable)
df[order(df$view_mean, decreasing = T), ] %>%
    select(name, view_mean, likes_mean, fans, total) %>%
    .[1:10, ] %>%
    add_column(排名=1:10,.before = "name") %>% 
    gt() %>%
    cols_label(
        name = md("UP主"),
        view_mean = md("平均播放量"),
        likes_mean = md("平均点赞数"),
        fans = md("粉丝数"),
        total = md("视频总数")
    ) %>%
    fmt_integer(columns = c(view_mean, likes_mean, fans)) %>%
    tab_header(md("关注的UP主平均播放量前十")) %>%
    gt_highlight_rows(rows = 1, font_weight = "normal") %>%
    gt_theme_espn()
df[order(df$likes_mean, decreasing = T), ] %>%
    select(name, view_mean, view, likes, likes_mean, fans, total) %>%
    .[1:10, ] %>%
    gt() %>%
    gt_theme_espn()


field.update <- expand.grid(x = levels(as.factor(df$big_field)), y = levels(df$update))
field.update
field.update$z <- table(df$big_field, df$update) %>% as.vector()


field.update$z <- scale(field.update["z"])
ggplot(field.update, aes(x = x, y = y, fill = z)) +
    geom_tile() +
    scale_fill_material("blue")

table(df$big_field, df$update) %>%
    as.data.frame() %>%
    ggplot(aes(x = Var2, y = Freq, fill = Var1)) +
    geom_bar(position = "stack", stat = "identity") +
    theme_ipsum() +
    scale_fill_npg()
table(df$big_field, df$update) %>%
    as.data.frame() %>%
    ggplot(aes(x = Var2, y = Freq, fill = Var1)) +
    geom_bar(position = "fill", stat = "identity") +
    theme_ipsum() +
    scale_fill_npg()
table(df$big_field, df$update) %>%
    as.data.frame() %>%
    ggplot(aes(x = Var1, y = Freq, fill = Var2)) +
    geom_bar(position = "stack", stat = "identity") +
    theme_ipsum() +
    scale_fill_npg()
table(df$big_field, df$update) %>%
    as.data.frame() %>%
    ggplot(aes(x = Var1, y = Freq, fill = Var2)) +
    geom_bar(position = "fill", stat = "identity") +
    theme_ipsum() +
    scale_fill_npg()

df %>% filter(big_field == "none")

library(lubridate)

table <- df["time"] %>%
    apply(1, year) %>%
    table(df$big_field)
colnames(table) <- c("Entertainment", "Knowledge", "Life", "None", "Videos")
table %>%
    as.data.frame() %>%
    rename_with(function(x) {
        return(c("Year", "Fields", "Freq"))
    }) %>%
    ggplot(aes(x = Year, y = Freq, fill = Fields)) +
    geom_bar(position = "dodge", stat = "identity") +
    xlab("Year") +
    ylab("Count") +
    theme_ipsum() +
    scale_fill_npg()
df["time"] %>%
    apply(1, year) %>%
    table(df$big_field) %>%
    as.data.frame() %>%
    rename_with(function(x) {
        return(c("Year", "Field", "Freq"))
    }) %>%
    ggplot(aes(x = Year, y = Freq, fill = Field)) +
    geom_bar(position = "stack", stat = "identity") +
    theme_ipsum() +
    scale_fill_npg()

df["time"] %>%
    apply(1, year) %>%
    table(df$update) %>%
    as.data.frame() %>%
    rename_with(function(x) {
        return(c("Year", "Update", "Freq"))
    }) %>%
    ggplot(aes(x = Year, y = Freq, fill = Update)) +
    geom_bar(position = "fill", stat = "identity") +
    theme_ipsum() +
    scale_fill_npg()

year_color <- colorRampPalette(pal_npg("nrc")(10))(15)

df["first"] %>%
    apply(1, year) %>%
    table() %>%
    as.data.frame() %>%
    rename_with(function(x) {
        return(c("Year", "Freq"))
    }) %>%
    filter(Year != 1970) %>%
    ggplot(aes(x = Year, y = Freq)) +
    geom_bar(stat = "identity", fill = "orange") +
    theme_ipsum()
# scale_fill_manual(values=year_color)

df %>% filter(year(first) == 2010)
