#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 20:13:07 2020

@author: suchetkumar
"""

# Load the Pandas libraries with alias 'pd' 
import pandas as pd 

# pandas settings for printing
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Read data from file 'filename.csv' 
metadata = pd.read_csv("Metadata.csv")
part1 = pd.read_csv("Part 1.csv")
part2 = pd.read_csv("Part 2.csv")
part3 = pd.read_csv("Part 3.csv")
part4a = pd.read_csv("Part 4a.csv")
part4b = pd.read_csv("Part 4b.csv")
part5 = pd.read_csv("Part 5.csv")



# consolidate all the data into part1
#part1.append(part2)
#part1.append(part3)
#part1.append(part4a)
#part1.append(part4b)
#part1.append(part5)

# Create a new dataset with total revenue
total_revenue = pd.DataFrame(columns=['GEO.id', 'GEO.display-label', 'NAICS.id', 'NAICS.display-label', 'REVENUE (k)', 'YEAR.id', 'ESTAB']);

# Cycle through the data rows
# start summation: RCPSZFE.id = 1
# 100k to 250k: RCPSZFE.id = 123 (average = 125k)
# 250k to 500k: RCPSZFE.id = 125 (average = 375k)
# 500k to 1M: RCPSZFE.id = 131 (average = 750k)
# 1M and over: RCPSZFE.id = 132 (1M)
current_row = {}
for index, row in part1.iterrows():
    print('Row: '+ str(index))
    if (row['RCPSZFE.id'] == '001'):
        # add the last summation to revenue data
        if (index != 1):
            print('appending row: '+str(current_row))
            total_revenue = total_revenue.append(current_row, ignore_index=True)
            
        # create new row
        print('created new row')
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
total_revenue.to_csv('total_revenue.csv', encoding='utf-8', index=False)
    
        


































