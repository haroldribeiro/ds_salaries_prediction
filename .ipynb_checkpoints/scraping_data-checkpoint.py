#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 15:07:47 2021

@author: haroldribeiro
"""

import scraping_glassdor as gs


df = gs.get_jobs("data scientist","3",400,False,20)

df.to_csv(r'/Users/haroldribeiro/OneDrive/Documents/Studies/Data Science/DS Portfolio/Web Scraping Glassdor/ds_data.csv',index = False, header = True)