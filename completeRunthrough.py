#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 01:13:10 2020

@author: lputnam
"""
import pandas as pds

#Step1: Aggregate all the given data into one file
givenDataAggregatedLocation = "GivenData/AggregatedParts.csv" # This is where the aggregated table will go
givenDataAggregatedAndRevenueTotal = 'GivenData/Aggregated_parts_with_total_revenue.csv'

filenames = []

filenames.append('GivenData/Part 1.csv')
filenames.append('GivenData/Part 2.csv')
filenames.append('GivenData/Part 3.csv')
filenames.append('GivenData/Part 4a.csv')
filenames.append('GivenData/Part 4b.csv')
filenames.append('GivenData/Part 5.csv')

dataframes = [pd.read_csv(f) for f in filenames]

# consolidate all the data into part1
for dfs in dataframes[1:]:
    dataframes[0].append(dfs)

dataframes[0].to_csv(givenDataAggregatedLocation); #this line outputs the aggregated data to a csv
########################################
del filenames #clear up some memory
del dataframes
########################################
#load in the given data but aggregated
RawAggregated = pd.read_csv(givenDataAggregatedLocation)

#create a new frame that includes total revenue
total_revenue = pd.DataFrame(columns=['GEO.id', 'GEO.display-label', 'NAICS.id', 'NAICS.display-label', 'REVENUE (k)', 'YEAR.id', 'ESTAB']);

# Cycle through the data rows and sum up the revenue 
# start summation: RCPSZFE.id = 1
# 100k to 250k: RCPSZFE.id = 123 (average = 125k)
# 250k to 500k: RCPSZFE.id = 125 (average = 375k)
# 500k to 1M: RCPSZFE.id = 131 (average = 750k)
# 1M and over: RCPSZFE.id = 132 (1M)

current_row = {}
for index, row in RawAggregated.iterrows():
    if (row['RCPSZFE.id'] == '001'):
        # add the last summation to revenue data
        if (index != 1):
            total_revenue = total_revenue.append(current_row, ignore_index=True)
            
        # create new row
        current_row = {'GEO.id' : row['GEO.id'], 
                       'GEO.display-label' : row['GEO.display-label'], 
                       'NAICS.id' : row['NAICS.id'], 
                       'NAICS.display-label' : row['NAICS.display-label'], 
                       'REVENUE (k)' : 0, 
                       'YEAR.id' : row['YEAR.id'], 
                       'ESTAB' : row['ESTAB']}
    elif (row['RCPSZFE.id'] == '123'):
        current_row['REVENUE (k)'] += (125 * int(row['ESTAB']))
    elif (row['RCPSZFE.id'] == '125'):
        current_row['REVENUE (k)'] += (375 * int(row['ESTAB']))
    elif (row['RCPSZFE.id'] == '131'):
        current_row['REVENUE (k)'] += (750 * int(row['ESTAB']))
    elif (row['RCPSZFE.id'] == '132'):
        current_row['REVENUE (k)'] += (1000 * int(row['ESTAB']))
print('total revenue dataframe: '+str(total_revenue.head()))
total_revenue.to_csv(givenDataAggregatedAndRevenueTotal, encoding='utf-8', index=False)
########################################
del RawAggregated
del total_revenue
del current_row
########################################
#Process the given data (aggregated) and add columns for spending power and market saturations

csv_names = ['CensusData/aggregate_income.csv'] #This is the income csv from the Census dept.
dataframes = [master]

for f in csv_names:
    dataframes.append(pd.read_csv(f))

index = 0
for df in dataframes:
    if index > 0:
        dataframes[0] = pd.merge(left=dataframes[0], right=df, 
                          how='outer', on='GEO.id', left_index=True, right_index=True)
    index+=1

print('master dataframe: \n'+str(dataframes[0].head()))
dataframes[0].to_csv('master.csv', encoding='utf-8', index=False)