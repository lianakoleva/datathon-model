# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 16:18:14 2020

@author: Arravind
"""

import pandas as pd 

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

election_data = pd.read_csv("GivenData/countypres_2000-2016.csv")
zip_codes = pd.read_csv("GivenData/zip_code_database.csv")

to_drop_election = ['year',
                    'state',
                    'FIPS',
                    'office',
                    'candidate',
                    'version']

to_drop_zip = ['type',
               'decommissioned',
               'primary_city',
               'acceptable_cities',
               'unacceptable_cities',
               'timezone',
               'area_codes', 
               'world_region',
               'latitude',
               'longitude',
               'irs_estimated_population_2015',
               'country']

election_data.drop(columns=to_drop_election, inplace=True)
zip_codes.drop(columns=to_drop_zip, inplace=True)

col_county = zip_codes['county']

index = 0
for name in col_county:
    if type(name) is str:
        if len(name.split(" ")):
            col_county[index] = name.split(' ')[0]
    index += 1
        
zip_codes = zip_codes.dropna()
election_data = election_data.dropna()

election_table = pd.pivot_table(election_data, values = 'candidatevotes', columns = 'party', index = ['state_po', 'county'])
zip_codes = zip_codes.set_index(['state','county'])

election = zip_codes.merge(election_table, left_index=True,right_index=True)


#election_data = election_data.pivot(index = ['state_po', 'county'], columns = 'party', values = 'candidatevotes')

#election = pd.merge(left=election_data, right=zip_codes, how='right', left_on=['state_po', 'county'], right_on =['state', 'county'], left_index=True, right_index=False)
#election.to_csv("election.csv", encoding='utf-8', index = False)