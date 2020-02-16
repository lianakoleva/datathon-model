# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 16:31:14 2020

@author: lianakoleva
"""
import pandas as pd

rev = [pd.read_csv('total_revenue_part1.csv'), 
                   pd.read_csv('total_revenue_part2.csv')]

master = pd.concat(rev)

csv_names = ['CensusData/aggregate_income.csv']
dataframes = [master]

for f in csv_names:
    dataframes.append(pd.read_csv(f))

index = 0
for df in dataframes:
    if index > 0:
        dataframes[0] = pd.merge(left=dataframes[0], right=df, 
                          how='left', on='GEO.id', left_index=True, right_index=True)
    index+=1

print('master dataframe: \n'+str(dataframes[0].head()))
dataframes[0].to_csv('master.csv', encoding='utf-8', index=False)