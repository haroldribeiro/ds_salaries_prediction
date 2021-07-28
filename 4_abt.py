# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 11:48:54 2021

@author: harold ribeiro
"""


import pandas as pd
import numpy as np

#set path
#path = r'C:/Users/Semantix/OneDrive - SEMANTIX TECNOLOGIA EM SISTEMA DE INFORMACAO S.A/Documentos/Web Scraping Glassdor/2_clean_data/'

path =  r'/Users/haroldribeiro/OneDrive/Documents/Studies/Data Science/DS Portfolio/Web Scraping Glassdoor/0_data/2_clean_data/'


#importing the data
df = pd.read_csv(path+'ds_data.csv')


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
                

#--------------------------------------------------------------------------------------------------------

#---------------------------------------#
#           job_title (vaga)            #
#---------------------------------------#

#Capitalize all words
df['vaga'] = df['vaga'].str.title().str.strip()


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


#--------------------------------------------------#
#  creating features from description (Descrição)  #
#--------------------------------------------------#
    


# identyfying hardskill

df['descricao'] = df.descricao.str.title().str.strip()

#1 - Math & Statistic

df['estatistica'] = np.where(df.descricao.str.lower().str.contains('math') |
                                 df.descricao.str.lower().str.contains('statistic')
                                 ,1,0)

df.math.value_counts()


#2 - Programming 

# R 
df['r'] = [1 if 'R' in x else 0 for x in df.descricao.str.replace('[^a-zA-Z0-9 ]+','').str.strip().str.split()]

df.r.value_counts()

#Python               
df['python'] = np.where(df.descricao.str.lower().str.contains('python'),1,0)

df.python.value_counts()

#Julia
df['julia'] = np.where(df.descricao.str.lower().str.contains('julia'),1,0)

df.julia.value_counts()

#C
df['c'] = [1 if 'C' in x else 0 for x in df.descricao.str.replace('[^a-zA-Z0-9 ]+','').str.strip().str.split()]

df.c.value_counts()

#Java
df['java'] = np.where(df.descricao.str.lower().str.contains('java'),1,0)

df.java.value_counts()

#Scala
df['scala'] = np.where(df.descricao.str.lower().str.contains('scala'),1,0)

df.scala.value_counts()

#SAS
df['sas'] = np.where(df.descricao.str.lower().str.contains('sas'),1,0)

df.sas.value_counts()

#MATLAB
df['matlab'] = np.where(df.descricao.str.lower().str.contains('matlab'),1,0)

df.matlab.value_counts()

check = df[df.c == 1]

   


# Data Manipulation
#SQL(101), Spark (41) 

# cloud(73)
# Aws, Azure, Google Cloud Plataform, GCP, Data Bricks

# Data viz
# Excel , Tableau, Power BI, Qlik

#ML
# Machine Learning, ML, Artificial Intelligence, AI, 

# MLOps


# rating
# checking distributions to see if I need to input an avarage

# company name
# splitting rating and company

# location
#splitting city and state

# size
# extract max employees as a number

# founded
# extract age 

# ownership

# industry

# sector

# revenue
# extract revenue  as number