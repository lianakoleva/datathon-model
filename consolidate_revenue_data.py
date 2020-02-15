#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 20:13:07 2020

@author: suchetkumar
"""

# Load the Pandas libraries with alias 'pd' 
import pandas as pd 

# Read data from file 'filename.csv' 
metadata = pd.read_csv("Metadata.csv")
part1 = pd.read_csv("Part 1.csv")
part2 = pd.read_csv("Part 2.csv")
part3 = pd.read_csv("Part 3.csv")
part4a = pd.read_csv("Part 4a.csv")
part4b = pd.read_csv("Part 4b.csv")
part5 = pd.read_csv("Part 5.csv")

# consolidate all the data into part1
part1.append(part2)
part1.append(part3)
part1.append(part4a)
part1.append(part4b)
part1.append(part5)

# Create a new dataset with total revenue
total_revenue = pd.DataFrame(columns=['GEO.id', 'GEO.display-label', 'NAICS.id', 'NAICS.display-label', 'REVENUE', 'YEAR.id', 'ESTAB']);

# Cycle through the data rows
# start summation: RCPSZFE.id = 1
# 100k to 250k: RCPSZFE.id = 123 (average = 125k)
# 250k to 500k: RCPSZFE.id = 125 (average = 375k)
# 500k to 1M: RCPSZFE.id = 131 (average = 750k)
# 1M and over: RCPSZFE.id = 132 (1M)
sum = 0
for row in part1.iterrows():
    if (row.RCPSZFE.id == 1):
        # create new row
        #current_row = 
    elif (row.RCPSZFE.id == 123):
        sum += 125
    elif (row.RCPSZFE.id == 125):
        sum += 375
    elif (row.RCPSZFE.id == 131):
        sum += 750
    elif (row.RCPSZFE.id == 132):
        sum += 1000
    
        


































