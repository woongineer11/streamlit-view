import streamlit as st
import subprocess
from PIL import Image

st.title(':key: 한화솔루션 데이터분석 (2024.01.31)')

st.sidebar.markdown('''
# About
## 목표

1.     타겟 Y3~Y6 값에 대한 해당 X 변수 도출

2.     Y1 – Y3~Y6 상관 관계 도출
 

X (변수) : 8개. 물리적 의미 및 변수 범위 기재

- X1 : 온도 (℃), 200 ~ 400℃

- X2 : 온도 (℃), 200 ~ 400℃

- X3 : RPM (rpm), 100 ~ 500 rpm

- X4 : 투입량 (kg/h), 4 ~ 20 kg/h

- X5 : 투입량 (mL/min), 0 ~ 10 mL/min

- X6 : 압력 (bar)

- X7 : 종류 1(categorical data, 0,2,4)

- X8 : 종류 2(categorical data, 각각 B1,B2,B3)

#### 변수 범위에서 Max.는 추정치라 실제 실험이 불가할 수 있습니다. 타겟에 대한 변수 도출 시 변수의 Max 값 부근에서 도출되지 않는 것이 좋을 것 같습니다.

Y (결과) : 6개. 물리적 의미

- Y1 : 압력 (bar)
- Y2 : 부하 (%)

- Y3~Y6 : 물성

R packages used:
- `ggplot2`
- 
''')

#st.subheader('1. Printing text in R')
#with st.expander('See code'):
#  code1 = '''print("Hello world ...")
#  '''
#  st.code(code1, language='R')
#process1 = subprocess.Popen(["Rscript", "helloworld.R"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#result1 = process1.communicate()
#st.write(result1)


#st.subheader('2. Creating a plot using `ggplot2`')
#with st.expander('See code'):
#  code2 = '''library(ggplot2)

#  ggplot(mtcars, aes(mpg, wt)) +
#    geom_point()

#  ggsave('plot.png')
#  '''
#  st.code(code2, language='R')
#process2 = subprocess.Popen(["Rscript", "plot.R"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#result2 = process2.communicate()
#image = Image.open('plot.png')
#st.image(image)
#st.caption('**Figure 1.** A simple scatter plot of *wt* as a function of *mpg* from the mtcars dataset.')


##
st.header(':balloon: 분석목적 및 방법')
st.subheader(':small_blue_diamond: 분석목적')
st.markdown('- 반응변수와 설명변수 간의 관계 파악 (총 93개 데이터)')
st.markdown('- 데이터 기반으로 반응변수의 최적화 시킬 수 있는 설명변수의 범위 파악')
st.markdown('&ensp; - Y3~Y6: 물성')
st.markdown('- Y_1과 Y_3~Y_6 간의 상관관계 파악')

st.subheader(':small_blue_diamond: 분석과정')
st.markdown('- 데이터 전처리: 변수 변환')
st.markdown('- 예측 모델 설계: 선형모델, 랜덤포레스트, XGBoost, Neural Network 사용')
st.markdown('- 최적화: 목표 반응변수 값을 위한 설명 변수 범위 파악 (탐색범위 정해지지 않음)\n\n')

##
st.header(':balloon: 설명변수, 반응변수')
st.subheader(':small_blue_diamond: 설명변수 (총 8개)')
st.markdown('- X1: 온도1')
st.markdown('- X2: 온도2')
st.markdown('- X3: RPM (rpm)')
st.markdown('- X4: 투입량 1(kg/h)')
st.markdown('- X5: 투입량 2(mL/min)')
st.markdown('- X6: 압력(bar)')
st.markdown('- X7: 종류 1("2") (범주형)')
st.markdown('- X8: 종류 1("3") (범주형)')
st.markdown('- X9: 종류 1("4") (범주형)')
st.markdown('- X10: 종류 2("B2") (범주형)')
st.markdown('- X11: 종류 2("B3") (범주형)')
st.markdown('-> X7~X10은 엑셀 데이터의 X7, X8을 더미화하여 생성한 변수들임.\n')

st.subheader(':small_blue_diamond: 반응변수 (총 5개)')
st.markdown('- Y1: 압력(bar)')
st.markdown('- Y3: 물성 1')
st.markdown('- Y4: 물성 2')
st.markdown('- Y5: 물성 3')
st.markdown('- Y6: 물성 4')
st.markdown('-> 연속형 변수 Y2에 "63-64", "65-67"와 같은 형태로 들어간 데이터 2개 존재하나, Y2 변수는 현재 분석에서 사용되지는 않음.\n\n')

##
st.header(':balloon: 탐색적 자료 분석')
st.subheader(':small_blue_diamond: Summary of EDA')
with st.expander('See code'):
  code3 = '''## Data Load
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
  '''
  st.code(code3, language='R')
process3 = subprocess.Popen(["Rscript", "Analysis_EDA.R"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result3 = process3.communicate()
image = Image.open('/Users/woong/Dropbox/통계학과 박시온/Projects/한화솔루션/한화솔루션_2023_2024_1st/KimSihyun/figure/jitter_plot.png')
st.image(image, width = 800)
st.caption('**Figure 1.** 변수들 간의 Correlation Plot')

st.markdown('- X변수들 중에서는 X5(투입량)과 X6(압력)이 0.960으로 correlation이 상당히 높게 나옴.')
st.markdown('- X4, X5, X6은 각 투입량과 압력 관련 변수이고, 적은 sample 수로 인해 boxplot 상의 outlier들을 실질적으로 outlier로 간주할 수 없음.\n\n')

##
st.subheader(':small_blue_diamond: Y1과 Y3-Y6 상관관계')
with st.expander('See code'):
  code3 = '''## Data Load
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
'''
  st.code(code3, language='R')
process3 = subprocess.Popen(["Rscript", "Analysis_Y_corr.R"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result3 = process3.communicate()
image = Image.open('/Users/woong/Dropbox/통계학과 박시온/Projects/한화솔루션/한화솔루션_2023_2024_1st/KimSihyun/figure/cor_Y.png')
st.image(image, width = 800)
st.caption('**Figure 2.** Y1과 Y3-Y6변수들 간의 Correlation Plot')

st.markdown('- Y1(압력)은 전체적으로 Y3~Y5 물성과의 correlation이 모두 0.89로 높은 편.')
st.markdown('- 다만, Y1과 Y6의 correlation은 0.69로 상대적으로 그렇게 높지는 않음.')
st.markdown('- 압력이 물성과 어느 정도의 유의미한 양의 상관관계를 갖는다고 볼 수 있음.\n\n')

##
st.header(':balloon: Model')
st.subheader(':small_blue_diamond: 모델 설계')
st.markdown('- 모든 반응 변수 $Y_i$를 각각 예측 $(i \in \{3\sim6\})$')
st.markdown('- 연속형 반응변수')
st.latex(r'Y_{i} = \beta_0 + \underbrace{\beta_{1} X_1 + \cdots + \beta_{p} X_{p} }_{\text{Main Effects}} + \underbrace{ \gamma_{1} X_{1}^2 + \cdots + \gamma_{p} X_{p}^2 }_{\text{Quadratic Effects}} + \underbrace{ \beta_{1,2} X_{1} X_{2}+ \cdots + \beta_{p-1,p} X_{p-1}  X_{p}}_{\text{2nd Interactions} } + \underbrace{\beta_{1,2,3} X_{1} X_{2} X_{3}  + \cdots + \beta_{p-2,p-1,p} X_{p-2} X_{p-1} X_{p} }_{\text{3rd Interactions} }+ \epsilon\\')

## 분석 방법
st.subheader(':small_blue_diamond: 분석방법')
st.markdown('모든 반응 변수 $Y_i$를 각각 예측 $(i \in \{3\sim6\})$')
st.markdown('- 선형 모델')
st.markdown('1. Full Model')
st.markdown('2. Stepwise Selection + AIC 기반 변수선택')
st.markdown('3. Stepwise Selection + BIC 기반 변수선택')
st.markdown('- 랜덤포레스트')
st.markdown('1. CV를 활용한 최적 hyperparameter 결정')
st.markdown('2. Backward elimination을 활용한 설명변수의 최적 부분집합 탐색')
st.markdown('- XGBoost')
st.markdown('1. CV를 활용한 최적 hyperparameter 결정')
st.markdown('2. Backward elimination을 활용한 설명변수의 최적 부분집합 탐색')
st.markdown('- Neural Network')
st.markdown('1. CV를 활용한 최적 hyperparameter 결정')
st.markdown('2. Backward elimination을 활용한 설명변수의 최적 부분집합 탐색\n')

## 분석 결과
st.subheader(':small_blue_diamond: 분석 결과 (10-fold CV)')
st.markdown('표 넣기')
st.markdown('- ')





###########################################################################################3
