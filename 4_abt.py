# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 11:48:54 2021

@author: harold ribeiro
"""


import pandas as pd
import numpy as np
from datetime import date

#set path
#path = r'C:/Users/Semantix/OneDrive - SEMANTIX TECNOLOGIA EM SISTEMA DE INFORMACAO S.A/Documentos/Web Scraping Glassdor/2_clean_data/'

path =  r'/Users/haroldribeiro/OneDrive/Documents/Studies/Data Science/DS Portfolio/Web Scraping Glassdoor/0_data/2_clean_data/'
path_store = r'/Users/haroldribeiro/OneDrive/Documents/Studies/Data Science/DS Portfolio/Web Scraping Glassdoor/0_data/3_abt_data/'

#importing the train data

df = pd.read_csv(path+'ds_data.csv') #train
#df = pd.read_csv(path+'ds_data_oot.csv') #ott

#----------------------------------------#
#           Seneriority (Senioridade)    #
#----------------------------------------#


#normalizing the job title (vaga) to create seniority feature
df['vaga'] = df['vaga'].str.lower()

#Senior label
df['senioridade']  =    np.where(                   
                        df['vaga'].str.contains('sr') | 
                        df['vaga'].str.contains('senior') |
                        df['vaga'].str.contains('associate') |
                        df['vaga'].str.contains('expert') |
                        df['vaga'].str.contains('specialist') |
                        df['vaga'].str.contains('consultant') |
                        df['vaga'].str.contains('lead') |
                        df['vaga'].str.contains('iii') |
                        df['vaga'].str.contains('experienced') |
                        df['vaga'].str.contains('principal') |
                        df['vaga'].str.endswith('3') |
                        df['vaga'].str.contains('scientist 3') |
                        df['vaga'].str.contains('scientist iii') |
                        df['vaga'].str.contains('master')
                        , 'Senior',  
                        #Manager label
                        np.where(df['vaga'].str.contains('manager') |
                                 df['vaga'].str.contains('supervisor') |
                                 df['vaga'].str.contains('director') |
                                 df['vaga'].str.contains('chief')
                        , 'Executive',
                        #Mid label (pleno)
                        np.where(df['vaga'].str.contains('mid') |
                                 df['vaga'].str.contains('level ii') |
                                 df['vaga'].str.endswith('ii') |
                                 df['vaga'].str.contains('scientist 2') |
                                 df['vaga'].str.contains('scientist ii') |
                                 df['vaga'].str.endswith('2') 
                       , 'Mid',  
                        #junior label
                        np.where(df['vaga'].str.contains('jr') |
                                 df['vaga'].str.contains('junior') |
                                 df['vaga'].str.endswith('i') |
                                 df['vaga'].str.endswith('1') |
                                 df['vaga'].str.contains('scientist 1') |
                                 df['vaga'].str.contains('scientist i') |                                 
                                 df['vaga'].str.contains('internship') |
                                 df['vaga'].str.contains('resident') |
                                 df['vaga'].str.contains('entry') 
                                 
                       , 'Junior',  
                       #Not aplicable
                       'Na'))))    
                
df.senioridade.value_counts(1)
#--------------------------------------------------------------------------------------------------------

#---------------------------------------#
#           job_title (vaga)            #
#---------------------------------------#

#Capitalize all words
df['vaga'] = df['vaga'].str.title().str.strip()


#Simplifying job tittle 

df['vaga_simplificada'] = np.where(df.vaga.str.contains('Analyst')
                                   ,'Data Analyist',
                          np.where(df.vaga.str.contains('Engineer')
                                   ,'Data Engineer',
                          np.where(df.vaga.str.contains('Learning') | 
                                   df.vaga.str.contains('Ml')
                                   ,'Machine Learning',
                          np.where(df.vaga.str.contains('Manager')
                                   ,'Manager',
                          np.where(df.vaga.str.contains('Director')                                   
                                   ,'Director',
                          np.where(df.vaga.str.contains('Scientist')
                                   ,'Data Scientist'
                                   ,'Na'))))))

                               
df.vaga_simplificada.value_counts(1)

#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------#
#  creating features from salary_estimate (Salario)#
#--------------------------------------------------#



# Creating new flags


# Flag if glassdoor estimate the salary or not
df['fg_glassdor_est'] = df['salario_estimado'].apply(lambda x: 1 if 'glassdoor' in x.lower() else 0)


# Flag if the salary is either per hour or anual rate
df['fg_por_hora'] = df['salario_estimado'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)



#------------------------------------------------------------------------------


# Creating salary variables - (salario_min, salario_max, salario_medio)

df = (
      df.assign(
                salario_min = lambda x: x.salario_estimado.str.replace('[a-zA-Z(.):$]','').str.strip().str.split('-', expand=True)[0].astype(int),
                salario_tmp = lambda x: x.salario_estimado.str.replace('[a-zA-Z(.):$]','').str.strip().str.split('-', expand=True)[1],
                salario_max = lambda x: np.where(x.salario_tmp.isnull()==True,x.salario_min,x.salario_tmp).astype(int),               
                salario_medio = lambda x: (x.salario_min + x.salario_max) / 2  
                                                 
       )
      .drop(columns='salario_tmp')
)



df.salario_medio.describe()

# Converting salary per hour for annual
df = (
      df.assign(
           salario_min = np.where(df.fg_por_hora == 1, round(((df.salario_min * 168) * 12)/1000,1), df.salario_min),
           salario_max = np.where(df.fg_por_hora == 1, round(((df.salario_max * 168) * 12)/1000,1), df.salario_max),
           salario_medio = np.where(df.fg_por_hora == 1, round(((df.salario_medio * 168) * 12)/1000,1), df.salario_medio)
          
          )
)

df.salario_medio.describe()

# x1000 scale

df = (
      df.assign(
           salario_min = round(df.salario_min * 1000),
           salario_max = round(df.salario_max * 1000),
           salario_medio = round(df.salario_medio * 1000)
      )
)


#--------------------------------------------------#
#  creating features from description (Descrição)  #
#--------------------------------------------------#
    
# normalizing description feature

df['descricao'] = df.descricao.str.title().str.strip()


#-----------------------------------------------------------------------------------------------------------------



#Counting qty of words in description field
df['descricao_qtd_palavras'] = df.descricao.apply(lambda x: len(x.split()))


df.descricao_qtd_palavras.describe()

#-----------------------------------------------------------------------------------------------------------------


# identyfying hardskill

#1 - Math & Statistic

df['estatistica'] = np.where(df.descricao.str.lower().str.contains('math') |
                                 df.descricao.str.lower().str.contains('statistic')
                                 ,1,0)

df.estatistica.value_counts()

#-----------------------------------------------------------------------------------------------------------------

#2 - Programming 

df['programacao'] = ([1 if (
                            ('R' in x) or 
                            ('python' in list(map(str.lower,x))) or
                            ('julia' in list(map(str.lower,x)))or
                            ('C' in x) or
                            ('java' in list(map(str.lower,x))) or
                            ('scala' in list(map(str.lower,x))) or
                            ('sas' in list(map(str.lower,x))) or
                            ('matlab' in list(map(str.lower,x)))
                            
                           )
                      else 0 
                      for x in df.descricao.str.replace('[^a-zA-Z0-9 ]+','').str.strip().str.split()]
                     )

df.programacao.value_counts()

#-----------------------------------------------------------------------------------------------------------------


#3 - Data Manipulation


df['etl'] = np.where(df.descricao.str.lower().str.contains('spark') |
                     df.descricao.str.lower().str.contains('sql'),1,0)

df.etl.value_counts()

#-----------------------------------------------------------------------------------------------------------------

#4 - SaaS

df['saas'] = np.where(df.descricao.str.lower().str.contains('aws') |
                      df.descricao.str.lower().str.contains('azure') |
                      df.descricao.str.lower().str.contains('google cloud platform') | 
                      df.descricao.str.lower().str.contains('gcp') |
                      df.descricao.str.lower().str.contains('databricks') 
                      ,1,0)

df.saas.value_counts()


#-----------------------------------------------------------------------------------------------------------------

#5 - Data viz


df['ferramentas_bi'] = np.where(df.descricao.str.lower().str.contains('excel') |
                                df.descricao.str.lower().str.contains('tableau') |
                                df.descricao.str.lower().str.contains('power bi') |
                                df.descricao.str.lower().str.contains('qlik')                           
                                ,1,0)

df.ferramentas_bi.value_counts()


#-----------------------------------------------------------------------------------------------------------------

#6 - ML
# Machine Learning and ML(260), Artificial Intelligence, AI, 


df['ml_ai'] = ([1 if (
                        ('ml' in list(map(str.lower,x))) or 
                        ('machine' in list(map(str.lower,x))) or
                        ('ai' in list(map(str.lower,x))) or
                        ('artificial' in list(map(str.lower,x)))                         
                     )
                else 0 for x in df.descricao.str.replace('[^a-zA-Z0-9 ]+','').str.strip().str.split()
               ]   
    )

df.ml_ai.value_counts()

#--------------------------------------------------------------------------------------------------------

#---------------------------------------#
#       company (nome_empresa)          #
#---------------------------------------#

# Keeping just company name
df['nome_empresa'] = df.apply(lambda x: x.nome_empresa.split('\n')[0] if x.nota != -1 else x.nome_empresa, axis = 1)


#--------------------------------------------------#
#  creating features from rating (nota)            #
#--------------------------------------------------#


# rating 

# checking mean and median for apply into missing values(-1)

#removing missing values to check de distribution
df.nota[df.nota != -1].describe()

#summing by rate
df[df.nota != -1].groupby('nota')['nota'].count()

#applying the median value where there are no company rating

df['nota'] = np.where(df.nota ==-1, df[df.nota !=-1].nota.median(), df.nota)
#3.8

#--------------------------------------------------------------------------------------------------------


#---------------------------------------#
#       location (localizacao)          #
#---------------------------------------#


#splitting city (cidade) and state (estado)

df.localizacao.head()

df = (
      df.assign(
          cidade = lambda x: x.localizacao.str.split(',', expand=True)[0],
          estado_tmp = lambda x: x.localizacao.str.split(',', expand=True)[1],
          estado = lambda x: np.where(x.estado_tmp.isnull()==True,'NA',x.estado_tmp.str.strip()).astype(str)            
     )
     .drop(columns='estado_tmp')
)


#Filtering records that has missing states
df_estados_na = df[df.estado == 'NA'].filter(items=['cidade','estado'])

# Normalizing as lowercase
df_estados_na['cidade'] = df_estados_na.cidade.str.lower()

# External dataset to identify states
df_estados = pd.read_csv(path+"states.csv",names=['estado','abv','codigo'],usecols=['estado','codigo'],skiprows=1)

# Normalizing as lowercase
df_estados['estado'] = df_estados.estado.str.lower()

# Merging the dataframes in order to recovery the states
df_estados_merge = df_estados_na.merge(df_estados, how='left',left_on='cidade', right_on='estado')

# Filling states with NA value
df_estados_na['codigo'] = np.where(df_estados_merge.codigo.isnull(),df_estados_merge.estado_x,df_estados_merge.codigo) 


# Checking remaning NA values

df_estados_na[df_estados_na.codigo=='NA'] 

#----------------------------------------------------
# Fixing states  manually based on city (cidade) name
#----------------------------------------------------
df_estados_na[df_estados_na.codigo=='NA'].groupby('cidade')['cidade'].count()

# New York state
df_estados_na['codigo'] = np.where((df_estados_na.cidade == 'new york state') & (df_estados_na.codigo == 'NA')
                                  ,'NY',df_estados_na.codigo)

# Puerto Rico
df_estados_na['codigo'] = np.where((df_estados_na.cidade == 'puerto rico') & (df_estados_na.codigo == 'NA')
                                  ,'PR',df_estados_na.codigo)

# Washington
df_estados_na['codigo'] = np.where((df_estados_na.cidade == 'washington state') & (df_estados_na.codigo == 'NA')
                                  ,'DC',df_estados_na.codigo)

# Merging results into main dataframe

df_codigo_estados =  df_estados_na[['cidade','codigo']].merge(df[['cidade','estado']],how = 'outer',left_index = True,right_index = True,indicator = True )


df['estado'] = np.where(df_codigo_estados._merge == 'both',df_codigo_estados.codigo,df.estado)


#Fixing state field that have counties instead of 2 letter code abbreviation
df['estado'] = np.where(df.estado.str.lower() == 'arapahoe'
                        ,'CO'
                        ,np.where(df.estado.str.lower() == 'cuyahoga','OH',df.estado))


# deleting temporary tables
del df_estados_merge, df_estados, df_estados_na, df_codigo_estados


#--------------------------------------------------------------------------------------------------------

#---------------------------------------#
#       Size (tamanho)                  #
#---------------------------------------#

# Checking size distribution

df.tamanho.value_counts()

# Adjusting companies without size information
df['tamanho'] = df.tamanho.apply(lambda x: 'Na' if (x == '-1' or x.lower() == 'unknown') else x)


# extracting size as a number


df = (
      df.assign(
                tamanho_min = lambda x: x.tamanho.str.split('to', expand = True)[0],
                tamanho_max = lambda x: x.tamanho.str.split('to', expand = True)[1],
                tamanho_tmp = lambda x: np.where(x.tamanho_max.isnull(), x.tamanho_min, x.tamanho_max),
                tamanho_num_tmp = lambda x: np.where(x.tamanho_tmp == 'Na',-1,x.tamanho_tmp.str.replace('[a-zA-Z\\+]','').str.strip()),
                tamanho_num = lambda x: x.tamanho_num_tmp.astype(int)                                                             
       )
       .drop(columns=['tamanho_min','tamanho_max','tamanho_tmp','tamanho_num_tmp'])
)


#--------------------------------------------------------------------------------------------------------

#---------------------------------------#
#       Fundation Year (Ano Fundacao)   #
#---------------------------------------#

# checking size distribution
df.ano_fundacao.value_counts()

# creating company age feature

#get current year
ano = int(date.today().strftime('%Y'))

df['idade_empresa'] = df.ano_fundacao.apply(lambda x: x if x < 0 else ano - x)

df.idade_empresa.describe()
#--------------------------------------------------------------------------------------------------------

#---------------------------------------#
#       Ownership (Tipo Propriedade)    #
#---------------------------------------#

#checking distribution
df.tipo_propriedade.value_counts(normalize=True)

#Adjusting missing value as constant
df['tipo_propriedade'] = df.tipo_propriedade.apply(lambda x: 'Na' if x == '-1' else x)

#--------------------------------------------------------------------------------------------------------

#---------------------------------------#
#       Industry (Industria)            #
#---------------------------------------#

#checking distribution
df.industria.value_counts(normalize=True)

#Adjusting missing value as constant
df['industria'] = df.industria.apply(lambda x: 'Na' if x == '-1'else x)

#--------------------------------------------------------------------------------------------------------

#---------------------------------------#
#       Sector (Setor)                  #
#---------------------------------------#

#checking distribution
df.setor.value_counts(normalize=True)

#Adjusting missing value as constant
df['setor'] = df.setor.apply(lambda x: 'Na' if x == '-1' else x)

#--------------------------------------------------------------------------------------------------------

#---------------------------------------#
#       Revenue (Receita)               #
#---------------------------------------#

#checking distribution
df.receita.value_counts()

#Adjusting missing value as constant

df['receita'] = df.receita.apply(lambda x: 'Na' if (x.strip() == '-1' or x.lower().strip() == 'unknown / non-applicable') else x) 


# extract revenue  as number
df = (
      df.assign(
             multiplicador  = np.where(df.receita == 'Na',-1,                               
                              np.where(df.receita.str.contains('billion'),1000000000,
                              np.where(df.receita.str.contains('million'),1000000,1))),
             receita_min = lambda x: x.receita.str.split('to', expand=True)[0],     
             receita_max = lambda x: x.receita.str.split('to', expand=True)[1],
             receita_tmp = lambda x: np.where(x.receita_max.isnull(),x.receita_min,x.receita_max),
             receita_re = lambda x: np.where(x.receita_tmp == 'Na','1',x.receita_tmp.str.replace('[a-zA-Z$\s()\\+]+','').str.strip()),
             receita_num = lambda x: np.where(x.receita_tmp == 'Na',-1,x.receita_re.astype(int) * x.multiplicador)
          
          )
          .drop(columns=['multiplicador','receita_min','receita_max','receita_tmp','receita_re'])
    
 )


#Ordering and fitlering variables
colunas = ['vaga_simplificada','senioridade','nome_empresa','tamanho','tipo_propriedade','industria','setor',
           'receita','cidade','estado','idade_empresa','nota','fg_glassdor_est','fg_por_hora',
           'salario_min','salario_max','salario_medio','descricao_qtd_palavras','tamanho_num','receita_num',
           'estatistica','programacao','etl','saas','ferramentas_bi','ml_ai'
           ]


#Filtering variables 
df = df[colunas]

 
#train
df.to_csv(path_store+'abt_train.csv', index=False, header=True)

#oot
#df.to_csv(path_store+'abt_ott.csv', index=False, header=True)






