# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor

import warnings

warnings.filterwarnings("ignore")

"""
Variables Selection

1.  Biomarkers
    * LBXTC: Total cholesterol
    * LBDLDLM: LDL cholesterol
    * LBDHDD: HDL cholesterol
    * LBXGH: HbA1c
    * LBXGLU : Fasting Glucose
    * LBXTR :The triglyceride values
    * LBXHSCRP: High-sensitivity C-reactive protein
    * LBXWBCSI: White blood cell count
    * URDACT: Urinary creatinine
    * SSAGP: Serum globulin

2.  Blood Pressure
    * BPXOSY1, BPXOSY2, BPXOSY3: Systolic blood pressure readings
    * BPXODI1, BPXODI2, BPXODI3: Diastolic blood pressure readings
    * BPXOPLS1, BPXOPLS2, BPXOPLS3: Pulse rate measurements

3.  Anthropometric Measures
    * BMXBMI: Body mass index
    * BMXWAIST: Waist circumference
    * BMXHIP: Hip circumference
    * BMXWT: Weight
    * LUXSMED : Median liver stiffness

4.  Demographics
    * RIDAGEYR: Age in years
    * RIAGENDR: Gender
    * RIDRETH3 : Ethnicity
    * INDFMPIR: Income-to-poverty ratio

"""

varlist = ['SEQN','LBXHSCRP','URDACT','LBXTC','LBDHDD','LBDLDLM','LBXGH','LBXGLU','SSAGP','LBXTR','LBXWBCSI','BMXBMI','BMXHIP','BMXWAIST','BMXWT','LUXSMED',
'BPXOSY1','BPXODI1','BPXOSY2','BPXODI2','BPXOSY3','BPXODI3','BPXOPLS1','BPXOPLS2','BPXOPLS3','RIAGENDR','RIDAGEYR','RIDRETH3','INDFMPIR']
print(len(varlist))

"""
Merging Laboratory, Examination and Demographics Data for the selected variables on "SEQN" key
"""

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the repository root
repo_root = os.path.dirname(script_dir)

# Construct the absolute path to the data file
data_path = os.path.join(repo_root, 'data','raw_csvData')

output_path = os.path.join(repo_root, 'outputs')


#Output folders for output files and plots
plots_outputFolder = os.path.join(output_path, 'plots')
os.makedirs(plots_outputFolder, exist_ok=True)

files_outputFolder = os.path.join(output_path, 'files')
os.makedirs(files_outputFolder, exist_ok=True)

dataDf = pd.DataFrame()

for filename in os.listdir(data_path):

    strdfname = str(str(filename).strip('.csv').split('_')[1])+str('_df')
    strdf = pd.read_csv(os.path.join(data_path, filename))

    if len(list(strdf['SEQN'].unique())) != strdf.shape[0]:
        print("Duplicate SEQN ids in file:",filename)

    cols = [i for i in varlist if i in strdf.columns]
    strdf = strdf[cols]
    strdf.dropna(subset=strdf.columns.difference(['SEQN']), how='all', inplace=True)
    if dataDf.empty:
        dataDf = dataDf.append(strdf)
    else:
        dataDf = dataDf.merge(strdf, on='SEQN', how='outer')

#Checking the data info
print(dataDf.shape)
print(dataDf.info())

#Descriptive overview of the dataset

print(dataDf.describe())

#Checking the null values

print(dataDf.isnull().sum())

#Calculating total precentage of missing values in each column

print(dataDf.isnull().sum() * 100/len(dataDf))

#Correlation Heatmap

corrmat = dataDf.corr()
corrmat = corrmat.where(np.triu(np.ones(corrmat.shape), k=1).astype(bool))
corr = corrmat.stack().transpose().sort_values(ascending=False).dropna()[0:10]
print("Top 5 Column Pairs with Highest Correlation:\n", corr)
plt.figure(figsize=(16,14))
ax = sns.heatmap(dataDf.corr(),annot=True,fmt='.2f',annot_kws={"size": 8})
plt.savefig(os.path.join(plots_outputFolder,"Correlation_Heatmap.png"),bbox_inches='tight',dpi=1500)
plt.show()

#Distribution Plots

for col in dataDf.columns:
  if col != 'SEQN':
    sns.displot(dataDf[col], kde=True)
    plt.title(f'Distribution of {col}')
    plt.savefig(os.path.join(plots_outputFolder,str(col)+".png"), bbox_inches="tight", dpi=300)
    plt.show()

dataDf.to_csv(os.path.join(files_outputFolder,"mergedData.csv"),index=False)

