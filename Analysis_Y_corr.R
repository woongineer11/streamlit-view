## Data Load
## - 결측치 없음
## - 93개 데이터; X1 ~ X9, Y1 ~ Y8
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
df <- read_xlsx("data_1.xlsx")

## 변수명 변경
colnames(df)[1:9] <- paste0("X", c(9, 1:8))
colnames(df)[10:15] <- paste0("Y", 1:6)

# ## Y2는 의뢰내용에서 사용하지 않아서 괜찮을듯
# ## 연속형 변수 Y2에 포함되어 있는 이상치 2개 제거(문의가 필요할듯)
# df <- df[-c(68,69), ]
# df$Y2 <- as.numeric(df$Y2)

## X9, Y2 제거 (의뢰내용에 X9, Y2 사용안함)
df <- dplyr::select(df, -c("X9","Y2"))

## X7 범주형으로 변환
df$X7 <- as.character(df$X7)

## X7("0","2","3","4"), X8("B1","B2","B3") 더미변수로 변환 (X7은 "0"이 기준, X8은 "B1"이 기준)
df <- dummy_cols(df)
df <- dplyr::select(df, -c("X7","X8","X7_0","X8_B1"))

## 2.     Y1 – Y3~Y6 상관 관계 도출
df2 <- df[, c("Y1","Y3","Y4","Y5","Y6")]
png("figure/cor_Y.png", width = 500, height = 500)
par(mfrow = c(1,1), mar = c(3,2,2,1))
corrplot.mixed(cor(df2), upper = 'color', number.cex = 0.75)
dev.off()