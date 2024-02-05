## Data Load
## - 결측치 없음
## - 93개 데이터; X1 ~ X9, Y1 ~ Y8
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
df <- read_xlsx("data_1.xlsx")

## 변수명 변경
colnames(df)[1:9] <- paste0("X", c(9, 1:8))
colnames(df)[10:15] <- paste0("Y", 1:6)
head(df)
# X9       X1    X2    X3    X4    X5    X6    X7 X8       Y1 Y2        Y3     Y4     Y5    Y6
# A       250   250   150     5     0     0     0 B1       89 62    186940 17936  13099   676.
# A       300   300   150     5     0     0     0 B1       63 60    208910 18671  13576  1865.

# ## Y2는 의뢰내용에서 사용하지 않아서 괜찮을듯
# ## 연속형 변수 Y2에 포함되어 있는 이상치 2개 제거(문의가 필요할듯)
# df <- df[-c(68,69), ]
# df$Y2 <- as.numeric(df$Y2)

## X9, Y2 제거 (의뢰내용에 X9, Y2 사용안함)
df <- dplyr::select(df, -c("X9","Y2"))
head(df)
# X1    X2    X3    X4    X5    X6    X7 X8       Y1     Y3     Y4     Y5    Y6
# 1   250   250   150     5     0     0     0 B1       89 186940 17936  13099   676.
# 2   300   300   150     5     0     0     0 B1       63 208910 18671  13576  1865.

## X7 범주형으로 변환
df$X7 <- as.character(df$X7)

## X7("0","2","3","4"), X8("B1","B2","B3") 더미변수로 변환 (X7은 "0"이 기준, X8은 "B1"이 기준)
df <- dummy_cols(df)
df <- dplyr::select(df, -c("X7","X8","X7_0","X8_B1"))
head(df)
# X1    X2    X3    X4    X5    X6    Y1     Y3     Y4     Y5    Y6  X7_2  X7_3  X7_4 X8_B2 X8_B3
# 1   250   250   150     5     0     0    89 186940 17936  13099   676.     0     0     0     0     0
# 2   300   300   150     5     0     0    63 208910 18671  13576  1865.     0     0     0     0     0


#######################################
#########   Visualization  #################
#######################################
## Box plot
# X variables
idx <- which(colnames(df) %in% c("X1","X2","X3","X4","X5","X6"))
par(mfrow = c(2, 3))
for (i in idx) {
  boxplot(df[, i], main = colnames(df)[i])
}

# Y variables
idx <- which(colnames(df) %in% c("Y1","Y3","Y4","Y5","Y6"))
par(mfrow = c(2, 3))
for (i in idx) {
  boxplot(df[, i], main = colnames(df)[i])
}


## Corr plots - 그릴 변수들만 data2로 만듬
df2 <- df[, c("X1","X2","X3","X4","X5","X6",
              "Y1","Y3","Y4","Y5","Y6")]
par(mfrow = c(1,1), mar = c(3,2,2,1))
corrplot.mixed(cor(df2), upper = 'color', number.cex = 0.75)


###########jitter plot ###########################
boxplot_custom <- function(data, mapping, ...){
  ggplot(data = data, mapping = mapping) +
    geom_boxplot()
}

jitter_custom <- function(data, mapping, ...){
  ggplot(data = data, mapping = mapping) +
    geom_jitter(alpha = 0.5)
}

p <- GGally::ggpairs(
  data = df2,
  # mapping = aes_string(color = "Y_S"),
  # columns = c("X4","X6","X8","X11","Y3","Y8"),
  diag = list(continuous = boxplot_custom),
  lower = list(continuous = jitter_custom)
)
ggsave("figure/jitter_plot.png", p, width = 10, height = 10)
