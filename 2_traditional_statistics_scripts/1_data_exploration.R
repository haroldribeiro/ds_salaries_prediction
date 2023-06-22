# -------------------------------------------#
#         1. LIBRARIES                       #
# -------------------------------------------#

library(descr) #pivot table
library(e1071) #skewd
library(dplyr) 
library(GGally) #ggpairs
library(ggplot2)
#-------------------------------------------------------------------------------


# ------------------------------------------- #
# 2.  DATASET AND FIRST DATA STRUCTURE CHECK  #
# ------------------------------------------- #

# Set my work directory
setwd("/Users/haroldribeiro/OneDrive/Documents/Studies/Data Science/DS Portfolio/Web Scraping Glassdoor/0_data/3_abt_data")


# Remove scientific notation
options(scipen=999)

# Import the dataset
df_ds_salarios <- as.data.frame(read.csv("abt_train.csv", sep = ","))

str(df_ds_salarios)

# Missing value check
sum(is.null(df_ds_salarios))

sum(is.na(df_ds_salarios))

# ------------------------------------------------------------------------------ 

# ------------------------------------------- #
# 3.  EXPLORATORY DATA ANALYSIS (EDA)         #
# ------------------------------------------- #


par(mfrow=c(1,1))
## 3.1 UNIVARITE ANALISYS

### 3.2 Vacancies variables

# job title (vaga_simplificada)
#  ~70% of vacancies with skills related for DS are really a Data Scientist Job
#  ~30% of vacancies are requering DS skills but the job is not to work as one

freq(df_ds_salarios$vaga_simplificada)

analise_uni <- df_ds_salarios %>% group_by(vaga_simplificada) %>%
               summarise(qtd_vagas = n()
                         ) %>%
               arrange(-qtd_vagas)

barplot(analise_uni$qtd_vagas, names.arg  = analise_uni$vaga_simplificada)

# ---

# seniority (senioridade)
# Most of vacancies are Senior level(23,61%) or Unkonwn 67,57%)
freq(df_ds_salarios$senioridade)

# grouping vacancies by seniority
analise_uni <- df_ds_salarios %>% group_by(senioridade) %>%
  summarise(qtd_vagas = n()
            ) %>%
  arrange(-qtd_vagas)

# adding relative accumulative frequence column
analise_uni <- transform(analise_uni, relative = prop.table(qtd_vagas))

View(analise_uni)
# ---

# Qty of words in the description of each vacancy (descricao_qtd_palavras)
# Amplitude higher between min and max qty of words of 1317 words
# Median is 148 words whereas mean is 198 words
summary(df_ds_salarios$descricao_qtd_palavras)
# Strong right skewed distribution of 2.657 asymmetric value
hist(df_ds_salarios$descricao_qtd_palavras,
     col="darkturquoise", xlab = NULL, ylab = NULL, main = NULL)
skewness(df_ds_salarios$descricao_qtd_palavras)
# There are a lot of outliers above upper limit 
boxplot(df_ds_salarios$descricao_qtd_palavras)

# ---

# Flag Glassdoor estimation (fg_glassdoor_est)
# 97% salaries were estimated by Glassdoor  
summary(df_ds_salarios$fg_glassdor_est)
freq(df_ds_salarios$fg_glassdor_est)


# Flag per hour (fg_per_hora)
# Just 1% of the vacancies are payed per hour
summary(df_ds_salarios$fg_por_hora)
freq(df_ds_salarios$fg_por_hora)

# ---

# ----------------------------------------------------------------------------#
# statistic (estastica) = ~0.29 vacancies there are statistic as skill        #
# programming (programacao) = ~0.14 vacancies there are programming as skill  #
# etl = ~0.12 vacancies there are etl as skill                                #
# saas = ~0.07 vacancies there are saas as skill                              #
# bi tools (ferramentas_bi) = ~0.14 vacancies there are bi tools as skill     #
# ml_ai = ~0.29 vacancies there are ML and AI as skill                        #
summary(df_ds_salarios[,c("estatistica","programacao","etl","saas","ferramentas_bi","ml_ai")])

cor(x = df_ds_salarios[,c("estatistica","programacao","etl","saas","ferramentas_bi","ml_ai")])

freq(df_ds_salarios$estatistica)
freq(df_ds_salarios$ml_ai)
freq(df_ds_salarios$programacao)
freq(df_ds_salarios$etl)
freq(df_ds_salarios$saas)
freq(df_ds_salarios$ferramentas_bi)


# ------------------------------------------------------------------------    #

### 3.3 Companies variables

# Company note (nota)

# Most of companies there is a note of 3.9
par(mfrow=c(1,2))
summary(df_ds_salarios$nota)
# Normal distribution because the skewness value is low -0.010 
hist(df_ds_salarios$nota,
     col="darkturquoise", xlab = NULL, ylab = NULL, main = NULL)
skewness(df_ds_salarios$nota) 
# There are fewer outliers lower (~3.3) and upper (~4.7)  limit 
boxplot(df_ds_salarios$nota,
        col="darkturquoise", xlab = NULL, ylab = NULL, main = NULL)
freq(df_ds_salarios$nota)
sd(df_ds_salarios$nota)

shapiro.test(df_ds_salarios$nota)

plot(density(df_ds_salarios$nota))

4.1-3.7 #IQQ
3.7-(0.4*1.5) # lower limit
4.1+(0.4*1.5) # lower limit


# ---

# Company Age (idade_empresa)

# 75% of the companies are under than 44 years (new companies)
summary(df_ds_salarios$idade_empresa)
# Right skewed distribution (positive) 
hist(df_ds_salarios$idade_empresa,
     col="darkturquoise", xlab = NULL, ylab = NULL, main = NULL)
skewness(df_ds_salarios$idade_empresa) 
# There are some companies as outliers with more than 77 (upper limit) 
boxplot(df_ds_salarios$idade_empresa,
        col="darkturquoise", xlab = NULL, ylab = NULL, main = NULL)
sd(df_ds_salarios$idade_empresa) #standard deviation = desvio padrão

shapiro.test(df_ds_salarios$idade_empresa)


IQQ <- 44-22 # IQQ
22 - (IQQ * 1.5) # Lower limit
44 + (IQQ * 1.5) # Upper limit

# ---

# company name (nome_empresa)
# No insight - So many categories and less representation between them
empresa <- freq(df_ds_salarios$nome_empresa, ) 

# ---

# size company (tamanho)
# Big companies with 10k+ (28%) employees are looking for Data Scientists 
freq(df_ds_salarios$tamanho)

# grouping vacancies by seniority
analise_uni <- df_ds_salarios %>% group_by(tamanho) %>%
  summarise(qtd_vagas = n()
  ) %>%
  arrange(-qtd_vagas)

# adding relative accumulative frequency column
analise_uni <- transform(analise_uni, relative = prop.table(qtd_vagas))

View(analise_uni)


# ---

#  property type (tipo_propriedade)
#  39% of companies are private, followed by 30% as public properties
freq(df_ds_salarios$tipo_propriedade)

# grouping vacancies by seniority
analise_uni <- df_ds_salarios %>% group_by(tipo_propriedade) %>%
  summarise(qtd_vagas = n()
  ) %>%
  arrange(-qtd_vagas)

# adding relative accumulative frequency column
analise_uni <- transform(analise_uni, relative = prop.table(qtd_vagas))

View(analise_uni)

# ---

# industry (industria)
# 22% are unknown, followed by 8.9% health and 8.16% biotech & pharm industries
freq(df_ds_salarios$industria)
industria <- freq(df_ds_salarios$industria)
View(industria)

# ---

# Sector (setor)
# 22% unknown
# 16% companies are related to Information Technology
freq(df_ds_salarios$setor)

# grouping vacancies by seniority
analise_uni <- df_ds_salarios %>% group_by(setor) %>%
  summarise(qtd_vagas = n()
  ) %>%
  arrange(-qtd_vagas)

# adding relative accumulative frequency column
analise_uni <- transform(analise_uni, relative = prop.table(qtd_vagas))

View(analise_uni)

# --- 

# Company revenue (receita)
# 40% Unknown 
# 19% are big companies which have more than 10 billion of revenue 
freq(df_ds_salarios$receita)

# grouping vacancies by seniority
analise_uni <- df_ds_salarios %>% group_by(receita) %>%
  summarise(qtd_vagas = n()
  ) %>%
  arrange(-qtd_vagas)

# adding relative accumulative frequency column
analise_uni <- transform(analise_uni, relative = prop.table(qtd_vagas))

View(analise_uni)

# ------------------------------------------------------------------------    #

### 3.4 Geospatial variables


# City (cidade)
# the variable alone doesn't have representation enough 
freq(df_ds_salarios$cidade)

sort(table(df_ds_salarios$cidade), decreasing = TRUE)

# State (estado)
# ~19% of vacancies is to work in CA, followed by NY with 8%

freq(df_ds_salarios$estado)

# grouping qty of vancies by state
estado_freq <-  df_ds_salarios %>% 
                group_by(estado) %>% 
                summarise(qtd_vagas=n()) %>%
                arrange(desc(qtd_vagas))

estado_freq <- estado_freq[order(estado_freq$qtd_vagas, decreasing = TRUE), ]

# Vacancies by state
ggplot(data = estado_freq, aes(x = reorder(estado,-qtd_vagas) , y=qtd_vagas)) + 
geom_bar(stat = "identity", fill = "darkturquoise", color = "black" ) + 
geom_text(aes(label=qtd_vagas), vjust=-0.3) +  
labs(x = NULL, y = NULL, title = NULL, caption = "Na = Not Applicable") +
theme(
  panel.grid.major = element_blank(), 
  panel.grid.minor = element_blank(),
  panel.background = element_blank(),
  plot.title = element_text(hjust = 0.5)
  
) 

# ------------------------------------------------------------------------    #


# average salary (salario_medio) - target variable

# Descriptive analysis
# Mean salary of a DS is 105k USD yearly
# there is 127k of difference (amplitude) between who earn less and more
# 75% of vacancies are offering a salary fees less than 115k yearly
summary(df_ds_salarios$salario_medio)

par(mfrow=c(1,1))

# Average salary there is a slight skewed left distribution (mean < median)
# Asymmetric value of -0.0577
hist(df_ds_salarios$salario_medio, col="darkturquoise", xlab = NULL, main = "Salário Médio (assimetria de -0.05)")
# skewness value
skewness(df_ds_salarios$salario_medio)
# test of skewness
shapiro.test(df_ds_salarios$salario_medio)


# there more outliers earning less than 57.5K than 149.5K yearly based on limits
boxplot(df_ds_salarios$salario_medio, col = "darkturquoise", main = "Salário Médio")
# 115-92 #IQQ 23k
# 92-(23*1.5) #lower limit 57.5
# 115+(23*1.5) #upper limit 149.5

# Amplitude
156500-29200 # 127300

# Checking outliers
df_limit_superior <- subset(df_ds_salarios, salario_medio > 149500)
df_limit_inferior <- subset(df_ds_salarios, salario_medio < 57500)

# Standard deviation
sd(df_ds_salarios$salario_medio)

# coefficient of variation
(sd(df_ds_salarios$salario_medio) / mean(df_ds_salarios$salario_medio)) * 100


sort(table(df_ds_salarios$salario_medio), decreasing = TRUE)

mode(df_ds_salarios$salario_medio)


View(df_limit_superior)
# ------------------------------------------------------------------------------

## BIVARIATE ANALYSIS

### Quantitative x Dependent Variable
par(mfrow=c(1,1))

ggpairs(df_ds_salarios[,c("salario_medio","idade_empresa","nota","descricao_qtd_palavras")])


# Company Age (idade_empresa)
# There is weak negative linear correlation of (-0.053)  between [company age] vs [avg salary]
plot(df_ds_salarios$salario_medio~df_ds_salarios$idade_empresa)
cor(df_ds_salarios$salario_medio,df_ds_salarios$idade_empresa, method = "pearson")

# Company note (nota)
# There is almost no linear correlation of (0.017) between [company note] vs [avg salary]
plot(df_ds_salarios$salario_medio~df_ds_salarios$nota)
cor(df_ds_salarios$nota,df_ds_salarios$salario_medio, method = "pearson")

# Qty of words in description (descricao_qtd_palavras)
# There is weak negative linear correlation of (-0.033)  between [qty of words] vs [avg salary]
plot(df_ds_salarios$salario_medio~df_ds_salarios$descricao_qtd_palavras)
cor(df_ds_salarios$salario_medio,df_ds_salarios$descricao_qtd_palavras, method ="pearson")

#---------------------------------
### Dummies x Dependent Variable

# fg_glassdor_est
# There is a big variability between salary who is estimated by Glassdoor vs companies
# Salaries estimated by companies usually pay less
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$fg_glassdor_est, 
        col="darkturquoise", xlab = NULL, ylab = NULL)
prop.table(table(df_ds_salarios$fg_glassdor_est))
summary(df_ds_salarios$salario_medio)

# fg per hour
# there is a big variability between vacancies who paid hourly vs annual salary
# hourly wages usually pay less than annual salary
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$fg_por_hora,
        col="darkturquoise", xlab = NULL, ylab = NULL)
prop.table(table(df_ds_salarios$fg_por_hora))


# statistic 
# vacancies who requires statistic skill usually pay more if you compare the body of boxplot (IQQ)
# and because there is more outliers at upper limit
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$estatistica)
prop.table(table(df_ds_salarios$estatistica))

# ml_ai
# vacancies who requires ML / AI skill usually pay more if you compare the body of boxplot (IQQ)
# and because there is more outliers at upper limit
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$ml_ai)
prop.table(table(df_ds_salarios$ml_ai))


# programming 
# vacancies who requires programming skill usually have a range more stable if 
# you compare the body of boxplot (IQQ)
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$programacao)
prop.table(table(df_ds_salarios$programacao))

# etl
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$etl)
prop.table(table(df_ds_salarios$etl))

# saas
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$saas)
prop.table(table(df_ds_salarios$saas))


# bi_tools 
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$ferramentas_bi)

#---------------------------------
### Quali x Dependent Variable


# job x avg salary 
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$vaga_simplificada,
        col="darkturquoise", xlab = NULL, ylab = NULL)
prop.table(table(df_ds_salarios$vaga_simplificada))

salario_por_vaga <- df_ds_salarios %>% group_by(vaga_simplificada) %>%
                    summarise(salario_medio = mean(salario_medio),
                              qtd_vagas = n()) %>%
                    arrange(-salario_medio)


                    
# ggplot(salario_por_vaga)  + 
#   geom_bar(aes(x=vaga_simplificada, y=salario_medio),stat="identity", fill="darkturquoise", colour="darkturquoise") +
#   geom_line(aes(x=vaga_simplificada, y=qtd_vagas),stat="identity", group = 1) +
#   geom_text(aes(label=qtd_vagas, x=vaga_simplificada, y=0.5*qtd_vagas), colour="black")+
#   geom_text(aes(label=salario_medio, x=vaga_simplificada, y=0.9*salario_medio), colour="black") +
#   scale_y_continuous(sec.axis = sec_axis(~./max(salario_por_vaga$salario_medio)))
#   

# seniority x avg salary
# senior usually earn 106k yearly
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$senioridade)
table(df_ds_salarios$senioridade)

df_ds_salarios %>% group_by(senioridade) %>% 
  summarise(salario_mediana=median(salario_medio),
            min_salario=min(salario_medio),
            max_salario = max(salario_medio),
            qtd=n()) 
  

# company size x avg salary
# small companies usually pay slightly more than big companies
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$tamanho,
        col="darkturquoise", xlab = NULL, ylab = NULL)

# property type x avg salary
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$tipo_propriedade)
freq(df_ds_salarios$tipo_propriedade)


grafico_tipo_propriedade <- df_ds_salarios %>% group_by(tipo_propriedade) %>% 
  summarise(salario_med = mean(salario_medio),
            salario_min = min(salario_medio),
            salario_max = max(salario_medio),
            qtd=n()) 
View(grafico_tipo_propriedade)
# industry x avg salary
# there aren't a good representation 
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$industria)
sort(table(df_ds_salarios$industria), decreasing = TRUE)


# sector x avg salary
# top 3 sectors are Education, Aerospace & Defesense, Transporation & Logistic (by median)
# The worst sector (Retail) pays around 99k yearly
# The best  sector (Education) pays around 111k yearly
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$setor)
salario_por_setor <- df_ds_salarios %>%
  group_by(setor) %>%
  summarise(salario_medio=mean(salario_medio), qtd=n()) %>%
  arrange(-salario_medio)
  #filter(qtd > 9)

View(salario_por_setor)
head(salario_por_setor, 5)


# revenue x avg salary
# usually small companies (who don't have a big revenue) pay more 
# than companies who have more th
tmp_receita <- boxplot(df_ds_salarios$salario_medio~df_ds_salarios$receita
        , xaxt= "n", xlab=NULL, ylab = NULL, col="darkturquoise")
tick <- seq_along(tmp_receita$names)
text(tick, par("usr")[3] - 0.5,labels = tmp_receita$names, srt = 45, adj = -0,1, xpd = TRUE)
table(df_ds_salarios$receita)



?boxplot
# state x avg salary 
# There is a good variability when we compare salary range across the states 
# states with more then 10 vacancies there is a salary range of 107k-112k annualy
boxplot(df_ds_salarios$salario_medio~df_ds_salarios$estado)

salarios_por_estado <- df_ds_salarios %>%
  group_by(estado) %>%
  summarise(salario_med=mean(salario_medio),
            salario_min = min(salario_medio),
            salario_max = max(salario_medio)
            ) %>%
  arrange(-salario_med)




