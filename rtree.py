#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 16:56:56 2020

@author: lputnam
"""

import pandas as pd

pathToTrainingData = "appended.csv"#"total_revenue (first 100).csv"
training_data = pd.read_csv(pathToTrainingData);

#training_data_indexes = training_data[["GEO.id", "GEO.display-label", "NAICS.id", "REVENUE"]]
#training_data_features = training_data[["race_white", "andSoOn"]]


#one-hot encode the data - categories become indicator variables (each category gets get their own dimension instead of sharing a dimension with all the other categories)
training_data = pd.get_dummies(training_data)

training_data.to_csv("sample_output_onehot.csv");
import numpy as np

#training_data = training_data.drop(training_data.index[5000:])#use this line to drop rows 5000 -> infiiny

print("training data shape: ", training_data.shape)

labels = np.array(training_data[["REVENUE (k)"]])
features = training_data.drop("REVENUE (k)", axis = 1)
feature_list = list(features.columns)
features = np.array(features)


#print(training_data.head(20))

# Using Skicit-learn to split data into training and testing sets
from sklearn.model_selection import train_test_split# Split the data into training and testing sets
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)

#print('Training Features Shape:', train_features.shape)
#print('Training Labels Shape:', train_labels.shape)
#print('Testing Features Shape:', test_features.shape)
#print('Testing Labels Shape:', test_labels.shape)
#
#print('Training Features', train_features[:5])
#print('Training Labels', train_labels[:5])
#print('Testing Features', test_features[:5])
#print('Testing Labels', test_labels[:5])


# Import the model we are using
from sklearn.ensemble import RandomForestRegressor# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)# Train the model on training data
rf.fit(train_features, train_labels.ravel());

print("training done")
#Use the forest's predict method on the test data
predictions = rf.predict(test_features)# Calculate the absolute errors

print('predictions:', predictions[:5])
print('test_labels:', test_labels[:5])

errors = abs(predictions - test_labels)# Print out the mean absolute error (mae)
print('Mean Absolute Error:', round(np.mean(errors), 2), 'DOLLARS XD')