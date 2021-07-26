#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 15:07:47 2021

@author: haroldribeiro
"""


import scraping_glassdor as gs

path = "/Users/haroldribeiro/OneDrive/Documents/Studies/Data Science/DS Portfolio/Web Scraping Glassdor"


df = gs.get_jobs(path,"data scientist","7",400,False,15)

df.to_csv(r'/Users/haroldribeiro/OneDrive/Documents/Studies/Data Science/DS Portfolio/Web Scraping Glassdor/1_raw_data/ds_oot_7.csv',index = False, header = True)