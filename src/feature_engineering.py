# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy.stats import skew

import warnings

warnings.filterwarnings("ignore")

"""Loading merged dataset from dataextraction_preprocessing.py"""

# Get the directory of the current script(for .py file)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the repository root
repo_root = os.path.dirname(script_dir)

# Construct the absolute path to the data folder
data_path = os.path.join(repo_root, 'data','raw_csvData')

# Construct the absolute path to the output folder
output_path = os.path.join(repo_root, 'outputs')

# Output folders for output files and plots
plots_outputFolder = os.path.join(output_path, 'plots')

files_outputFolder = os.path.join(output_path, 'files')

dataDf = pd.read_csv(os.path.join(files_outputFolder, 'mergedData.csv'))

# Checking the data info
print(dataDf.shape)
print(dataDf.info())

"""
1.   Creating a new variable "BPXOSY" to represent Systolic Blood Pressure value, by taking mean of the provided 3 readings taken 60 seconds apart

2.   Creating a new variable "BPXODI" to represent Diastolic Blood Pressure value, by taking mean of the provided 3 readings taken 60 seconds apart

3.   Creating a new variable "BPXOPLS" to represent Pulse measurement, by taking mean of the provided 3 readings taken 60 seconds apart
"""

dataDf['BPXOSY'] = dataDf[['BPXOSY1', 'BPXOSY2', 'BPXOSY3']].mean(axis=1, skipna=True)
dataDf['BPXODI'] = dataDf[['BPXODI1', 'BPXODI2', 'BPXODI3']].mean(axis=1, skipna=True)
dataDf['BPXOPLS'] = dataDf[['BPXOPLS1', 'BPXOPLS2', 'BPXOPLS3']].mean(axis=1, skipna=True)
dataDf = dataDf.drop(['BPXOSY1', 'BPXOSY2', 'BPXOSY3','BPXODI1', 'BPXODI2', 'BPXODI3', 'BPXOPLS1', 'BPXOPLS2', 'BPXOPLS3'],axis=1)

# Transforming categorical variables "RIDRETH3" and "RIAGENDR"

gender_map = {1: 'Male', 2: 'Female'}
dataDf['RIAGENDR'] = dataDf['RIAGENDR'].map(gender_map)

race_map = {1: 'Mexican American', 2: 'Other Hispanic', 3:	'Non-Hispanic White', 4:'Non-Hispanic Black',6:'Non-Hispanic Asian', 7:'Other Race'}
dataDf['RIDRETH3'] = dataDf['RIDRETH3'].map(race_map)

dataDf = pd.get_dummies(dataDf, columns=['RIAGENDR', 'RIDRETH3'], prefix=['Gender', 'Race'],dtype=bool)


# Removing variable/column with high % of missing values

# Columns with >=40% missing values
columnlist = [col for col in  dataDf.columns if (dataDf.isnull().sum() * 100/len(dataDf))[col] >= 40]
print(" Columns with greater than 40% missing values:\n",columnlist)

# Removing columns with high % missing values from the analysis (except for "LBDLDLM"(LDL))
newcolumnlist = columnlist.copy()
newcolumnlist.remove('LBDLDLM')
dfData_withLDL = dataDf.copy()
dfData_withLDL = dfData_withLDL.drop(newcolumnlist, axis=1)

# Removing columns with high % missing values from the analysis
dfData_withoutLDL = dataDf.copy()
dfData_withoutLDL = dfData_withoutLDL.drop(columnlist, axis=1)

# Removing rows with missing values
cleanedData = dfData_withoutLDL.copy()
cleanedData = cleanedData.dropna(how='any')
cleanedData = cleanedData.reset_index(drop=True)
print("\n Dataset without LDL variable:\n")
print(cleanedData.info())

# Removing rows with missing values(for data with LDL variable)
cleanedData_LDL = dfData_withLDL.copy()
cleanedData_LDL = cleanedData_LDL.dropna(how='any')
cleanedData_LDL = cleanedData_LDL.reset_index(drop=True)
print("\n Dataset with LDL variable:\n")
print(cleanedData_LDL.info())

# Cleaned Data (without LDL variable)
# Pre-checks Before Calculating Skewness

# Selecting only Numeric columns
numeric_cols = cleanedData.select_dtypes(include=['number'])
numeric_cols.drop(['SEQN'],axis=1,inplace=True)

# Checking for constant or near-constant values in columns
low_variance_cols = cleanedData.var()[cleanedData.var() == 0].index
print("Low variance columns: \n",low_variance_cols)

# Checking skewness for all numeric variables
""" 
Interpreting Skewness Values
|Skewness| <= 0.5 -> Symmetric
0.5 < |Skewness| <= 1 -> Moderately skewed
|Skewness| > 1 -> Highly skewed 
"""

# Compute skewness for each numeric column
skewness_values = cleanedData[numeric_cols.columns].apply(skew)

# Display skewness values
print("\nSkewness Values:\n",skewness_values)
print("\n")

# Define skewness categories
normal = []
moderate_skew = []
highly_skewed = []

for col, skew_value in skewness_values.items():
    if abs(skew_value) <= 0.5:
        normal.append(col)
    elif 0.5 < abs(skew_value) <= 1:
        moderate_skew.append(col)
    else:
        highly_skewed.append(col)

print("Normal Distribution:", normal)
print("Moderately Skewed:", moderate_skew)
print("Highly Skewed:", highly_skewed)

# Applying log transformation on highly skewed variables
for col in highly_skewed:
    cleanedData[col] = np.log1p(cleanedData[col])

print("Applying log transformation on highly skewed variables")
print("\nCleaned Data without LDL variable:\n")
print(cleanedData.info())
cleanedData.to_csv(os.path.join(files_outputFolder, 'cleanedData.csv'), index=False)

# Cleaned Data (with LDL variable)
# Pre-checks Before Calculating Skewness

# Selecting only Numeric columns
numeric_columns = cleanedData_LDL.select_dtypes(include=['number'])
numeric_columns.drop(['SEQN'],axis=1,inplace=True)


# Checking for constant or near-constant values in columns
low_variance_columns = cleanedData_LDL.var()[cleanedData_LDL.var() == 0].index
print("\nLow variance columns:\n",low_variance_columns)

# Checking skewness for all numeric variables
""" 
Interpreting Skewness Values
|Skewness| <= 0.5 -> Symmetric
0.5 < |Skewness| <= 1 -> Moderately skewed
|Skewness| > 1 -> Highly skewed 
"""

# Compute skewness for each numeric column
skewness_valuescols = cleanedData_LDL[numeric_columns.columns].apply(skew)

# Display skewness values
print("Skewness values:\n",skewness_valuescols)
print("\n")

# Define skewness categories
normalcols = []
moderate_skewcols = []
highly_skewedcols = []

for col, skew_value in skewness_valuescols.items():
    if abs(skew_value) <= 0.5:
        normalcols.append(col)
    elif 0.5 < abs(skew_value) <= 1.5:
        moderate_skewcols.append(col)
    else:
        highly_skewedcols.append(col)


print("Normal Distribution:", normalcols)
print("Moderately Skewed:", moderate_skewcols)
print("Highly Skewed:", highly_skewedcols)

# Applying log transformation on highly skewed variables
for col in highly_skewedcols:
    cleanedData_LDL[col] = np.log1p(cleanedData_LDL[col])

print("Applying log transformation on highly skewed variables")
print("\nCleaned Data with LDL variable:\n")
print(cleanedData_LDL.info())
cleanedData_LDL.to_csv(os.path.join(files_outputFolder, 'cleanedData_withLDL.csv'), index=False)
