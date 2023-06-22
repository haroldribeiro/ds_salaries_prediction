# ----------------- #
# 1.  LIBRARIES     #
# ----------------- #
library('fastDummies') # generate dummies
library('MASS') # step-wise
library('caret') # k-fold 
library('e1071') #skewed 
library('Metrics') # evaluate model
library('HH') #checking multicollinearity

# ------------------------------------------- #
# 2.  PRE-PROCESSING                          #
# ------------------------------------------- #

# Set my work directory
setwd("/Users/haroldribeiro/OneDrive/Documents/Studies/Data Science/DS Portfolio/Web Scraping Glassdoor/0_data/3_abt_data")


# Remove scientific notation
options(scipen=999)

# Import the dataset
df <- as.data.frame(read.csv("abt_train.csv", sep = ","))

df_oot <- as.data.frame(read.csv("abt_ott.csv", sep = ","))

# removing unnecessary columns 
df <- df[ , !(names(df) %in% c("nome_empresa","cidade", "industria"))]

df_oot <- df_oot[ , !(names(df_oot) %in% c("nome_empresa","cidade", "industria"))]

# generating dummies variables
df <- dummy_cols(df, select_columns = c('vaga_simplificada', 'senioridade',
                                       'tamanho', 'tipo_propriedade', 'setor',
                                       'receita', 'estado'), remove_selected_columns = TRUE)


df_oot <- dummy_cols(df_oot, select_columns = c('vaga_simplificada', 'senioridade',
                                        'tamanho', 'tipo_propriedade', 'setor',
                                        'receita', 'estado'), remove_selected_columns = TRUE)


sort(table(df$setor))

# adding column
df_oot$`setor_Agriculture & Forestry` <- 0


# setting a seed
set.seed(345)

# splitting dataset between train and test 80/20
amostra <- sort(sample(nrow(df), nrow(df)*0.8))

df_treino <- df[amostra,]

df_teste <- df[-amostra,]

sort(table(df_teste$`setor_Agriculture & Forestry`),decreasing = T)
sort(table(df_treino$`setor_Agriculture & Forestry`),decreasing = T)



# ------------------------------------------- #
# 3.  LINEAR REGRESSION                       #
# ------------------------------------------- #

# generating multiple linear model
# assuming 10% of significance and 90% of confidence 
base_lr <- lm(data=df_treino, 
        salario_medio ~ .
         )
summary(base_lr)
AIC(base_lr)
#20817.49

# using step-wise feature selection with both direction (forward ans backward)
lr_2 <- lm(salario_medio ~., data = df_treino)
step <- stepAIC(lr_2, direction = "both", trace = FALSE)
step$coefficients
summary(step)


# backward selection (after feature selection)
# assuming 10% of significance and 90% of confidence 
lr_best <- lm(data = df_treino,
                salario_medio ~
                fg_glassdor_est
                +fg_por_hora
                +vaga_simplificada_Manager
                +`tipo_propriedade_Nonprofit Organization`
                +`tipo_propriedade_Private Practice / Firm`
                +`setor_Agriculture & Forestry`
                +`setor_Biotech & Pharmaceuticals` 
                +setor_Government
                +`setor_Health Care`                                     
                #+`setor_Restaurants, Bars & Food Services` # 3
                #+setor_Retail  # 1                                           
                +`receita_$1 to $5 million (USD)`                       
                #+`receita_$10+ billion (USD)` # 5                        
                +`receita_$25 to $50 million (USD)`                    
                #+`receita_$500 million to $1 billion (USD)` #6
                +estado_AL                                              
                +estado_CA                                              
                #+estado_DC #9
                #+estado_IN #7
                +estado_MD                                               
                +estado_OH                                        
                #+estado_WI #8                                               
                +`tamanho_201 to 500 Employees`                        
                +`receita_$50 to $100 million (USD)`                   
                #+`tipo_propriedade_Company - Public` # 4
                #+idade_empresa # 2
                )

summary(lr_best)


# checking if there is multicollinearity between independent variables
# assuming VIF > 5 there aren't multicollinearity in the model
vif(lr_best, y.name = 'salario_medio')


# predict value
df_treino$salario_medio_pred <- fitted.values(lr_best)

# residual value
df_treino$residuo <- residuals(lr_best)


# -----------------------------------------------------------------------------------------

# ------------------------------------------- #
# 4.  RESIDUAL ANALYSIS                       #
# ------------------------------------------- #


par(mfrow=c(1,3))

plot(df_treino$salario_medio_pred, df_treino$residuo, main = 'Resíduos X Predito', ylab ='Resíduos', xlab = 'Predito', col = 'darkturquoise')

hist(df_treino$residuo, xlab = 'Resíduo', col = 'darkturquoise', main = 'Hist dos resíduos (Assimetria=0.34)')
skewness(df_treino$residuo)

qqnorm(df_treino$residuo, col="darkturquoise", frame = FALSE)
qqline(df_treino$residuo, col='red', lwd =2)

mape(actual = df_treino$salario_medio, predicted = df_treino$salario_medio_pred) # mean absolute percentage error
sse(actual = df_treino$salario_medio, predicted = df_treino$salario_medio_pred) # sum square error

# h0 is rejected based on p-value of < 0.10 thus the residuals ARE NOT normally distributed
shapiro.test(df_treino$residuo)

# confident intervals for the model
confint(lr_best, level = 0.90)

mean(df_treino$residuo)

# ------------------------------------------- #
#     5.  MODEL EVALUATION                    #
# ------------------------------------------- #

# train 
print('train')

mse(df_treino$salario_medio, df_treino$salario_medio_pred) # mean squared error
rmse(df_treino$salario_medio, df_treino$salario_medio_pred) # root mean squared error

mae(df_treino$salario_medio, df_treino$salario_medio_pred) # mean absolute error
mape(df_treino$salario_medio, df_treino$salario_medio_pred) # mean absolute percentage error
mpe()

# test
print('test')

df_teste$salario_medio_pred <- predict(lr_best, df_teste)

mse(df_teste$salario_medio, df_teste$salario_medio_pred) # mean squared error
rmse(df_teste$salario_medio, df_teste$salario_medio_pred) # root mean squared error

mae(df_teste$salario_medio, df_teste$salario_medio_pred) # mean absolute error
mape(df_teste$salario_medio, df_teste$salario_medio_pred) # mean absolute percentage error


# oot
print('oot')

df_oot$salario_medio_pred <- predict(lr_best, df_oot)

mse(df_oot$salario_medio, df_oot$salario_medio_pred) # mean squared error
rmse(df_oot$salario_medio, df_oot$salario_medio_pred) # root mean squared error

mae(df_oot$salario_medio, df_oot$salario_medio_pred) # mean absolute error
mape(df_oot$salario_medio, df_oot$salario_medio_pred) # mean absolute percentage error


