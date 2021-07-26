#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 23:01:59 2021

@author: haroldribeiro
"""


import pandas as pd
import glob

##--------------------------------------------------------------------------------------------------------------
##  ---------------------------------- Concatenating datasets --------------------------------------------------
##--------------------------------------------------------------------------------------------------------------

path = r'/Users/haroldribeiro/OneDrive/Documents/Studies/Data Science/DS Portfolio/Web Scraping Glassdor' # use your path

#oot
#all_files = glob.glob(path +"/1_raw_data" +"/*oot*.csv")
#Train and test
all_files = glob.glob(path +"/1_raw_data" +"/ds_data*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)


df = pd.concat(li, axis=0, ignore_index=True)

##--------------------------------------------------------------------------------------------------------------
##  ---------------------------------------- Cleaning dataset --------------------------------------------------
##--------------------------------------------------------------------------------------------------------------

#Identifying shape of dataset
df.shape
#(1116, 14)


# Removing no Salary estimation observations

#Verying  qtd of records
df[['Salary Estimate']].value_counts()


df = df[df['Salary Estimate']!='-1']
#(1060,14)

#----------------------------------------

# Removing duplicate observations

df.drop_duplicates(inplace = True)
#(919,14)


#----------------------------------------

# Removing variables wihout information


df[['Headquarters']].value_counts()

df[['Competitors']].value_counts()

df.drop(labels=['Headquarters','Competitors'], inplace=True, axis=1)


##--------------------------------------------------------------------------------------------------------------
##  ---------------------------------------- Storing dataset --------------------------------------------------
##--------------------------------------------------------------------------------------------------------------

#----------------------------------------


# renaming the name of variables


fields = (
        ['vaga','salario_estimado','descricao','nota','nome_empresa','localizacao','tamanho'
         ,'ano_fundacao','tipo_propriedade','industria','setor','receita']
        )



df.columns = fields

# Storing consolidate data into a csv file

#Train and test
df.to_csv(path+'/2_clean_data/ds_data.csv',index=False, header=True)

#OOT
#df.to_csv(path+'/2_clean_data/ds_data_oot.csv',index=False, header=True)











