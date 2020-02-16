#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 01:13:10 2020

@author: lputnam, lkoleva
"""
import pandas as pd
from collections import Counter
from operator import itemgetter

givenDataAggregatedLocation = 'GivenData/AggregatedParts.csv'
givenDataAggregatedAndRevenueTotal = 'GivenData/Aggregated_parts_with_total_revenue.csv'
givenDataMasterMerged = 'GivenData/Master.csv'

########################################

########################################

def processData1():
    #turn each given file into a dataframe, stored in list 'dataframes'
    filenames = ['part1.csv', 'part2.csv', 'part3.csv', 'part4a.csv',
                 'part4b.csv', 'part5.csv']
    dataframes = [pd.read_csv('GivenData/%s'% (f)) for f in filenames] 
    
    #consolidate all dataframes into dataframes[0]
    for dfs in dataframes[1:]:
        dataframes[0] = pd.concat([dataframes[0], dfs]) 
        
    #output aggregated data to csv
    dataframes[0].to_csv(givenDataAggregatedLocation); 
    return 0

########################################
    
def processData2():
    #load in the aggregated given data
    RawAggregated = pd.read_csv(givenDataAggregatedLocation)
    
    #create a new frame that includes total revenue
    total_revenue = pd.DataFrame(columns=['GEO.id', 'GEO.display-label', 
                                          'NAICS.id', 'NAICS.display-label',
                                          'REVENUE (k)', 'YEAR.id', 'ESTAB']);
    
    # Cycle through the data rows and sum up the revenue 
    # start summation: RCPSZFE.id = 1
    # 100k to 250k: RCPSZFE.id = 123 (average = 125k)
    # 250k to 500k: RCPSZFE.id = 125 (average = 375k)
    # 500k to 1M: RCPSZFE.id = 131 (average = 750k)
    # 1M and over: RCPSZFE.id = 132 (1M)
    
#    flist = ['part1.csv', 'part2.csv', 'part3.csv', 'part4a.csv',
#                 'part4b.csv', 'part5.csv']
#    optlist = [114, 123, 125, 131, 132]
#
#    for file in flist:
#        with open(flist[file], newline='') as f:
#            reader = csv.reader(f)
#            rev_id = Counter(map(itemgetter(5), reader))
#            print(rev_id)

    
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
    return 0

########################################
# process aggregated given data
# append columns for spending power, market saturation
def processData3():
    master = pd.read_csv(givenDataAggregatedAndRevenueTotal)
    csv_names = ['CensusData/aggregate_income.csv'] #B19025 from AFF
    
    for csvName in csv_names:
        subjectToMerge = pd.read_csv(csvName)
        master = pd.merge(left=master, right=subjectToMerge, how='outer', on='GEO.id', left_index=True, right_index=True)
    
    master['MS.dollars'] = master['INCOME.aggregate'] - (master['REVENUE (k)'] * 1000)
    master['MS.percent'] = (master['REVENUE (k)'] * 1000) / master['INCOME.aggregate']
    
    #drop the column of 2012s
    master = master.drop('YEAR.id', axis=1);    
    master = master.dropna()
    master.to_csv(givenDataMasterMerged, encoding='utf-8', index=False)
    
    return 0

# call function(s) as needed
processData1()
processData2()
processData3()