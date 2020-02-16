#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 00:26:44 2020

@author: lputnam
"""
import pandas as pd

outputFile = "master_processed.csv"

master= pd.read_csv('master.csv')
master['MS.dollars'] = master['INCOME.aggregate'] - (master['REVENUE (k)'] * 1000)
master['MS.percent'] = (master['REVENUE (k)'] * 1000) / master['INCOME.aggregate']

master.to_csv(outputFile)