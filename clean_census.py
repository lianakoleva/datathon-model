# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 19:55:11 2020

@author: lkoleva
"""
import pandas as pd

household = pd.read_csv('CensusData/ACS_12_5YR_S1901.csv')
delete = ['GEO.id2', 'GEO.display-label']

for col in household.columns:
    if 'MOE' in col:
        delete.append(col)
        
household = household.drop(columns=delete)
household.to_csv('CensusData/household.csv', encoding='utf-8', index=False)