# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy.stats import skew

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


import warnings

warnings.filterwarnings("ignore")

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

# Load datasets
df_with_ldl = pd.read_csv(os.path.join(files_outputFolder, 'cleanedData_withLDL.csv'))
df_without_ldl = pd.read_csv(os.path.join(files_outputFolder, 'cleanedData.csv'))

# Display basic info
print("\n")
print("Dataset with LDL variable")
print(df_with_ldl.info())
print("\n")
print("Dataset without LDL variable")
print(df_without_ldl.info())
print("\n")

# Define CVD risk label based on clinical thresholds
def create_cvd_risk_label(df, include_ldl=True):
    """
    Create a binary CVD risk label based on clinical thresholds.
    
    Args:
    df (DataFrame): The dataset.
    include_ldl (bool): Whether LDL is included as a feature.
    
    Returns:
    DataFrame: The dataset with a new 'CVD_Risk' column.
    """
    # High BP: Systolic BP >= 130 mmHg or Diastolic BP >= 80 mmHg
    high_bp = (df["BPXOSY"] >= 130) | (df["BPXODI"] >= 80)

    # High Cholesterol: LDL >= 100 mg/dL or Total Cholesterol >= 200 mg/dL
    if include_ldl:
        high_cholesterol = (df["LBDLDLM"] >= 100) | (df["LBXTC"] >= 200)
    else:
        high_cholesterol = df["LBXTC"] >= 200

    # Obesity: BMI >= 30
    obesity = df["BMXBMI"] >= 30

    # Diabetes Indicator: HbA1c >= 6.5%
    diabetes = df["LBXGH"] >= 6.5

    # Assign CVD risk label (1 = High Risk, 0 = Low Risk)
    df["CVD_Risk"] = ((high_bp | high_cholesterol | obesity | diabetes)).astype(int)

    return df

# Apply function to both datasets
df_with_ldl = create_cvd_risk_label(df_with_ldl, include_ldl=True)
df_without_ldl = create_cvd_risk_label(df_without_ldl, include_ldl=False)

# Check label distribution
cvd_risk_counts_with_ldl = df_with_ldl["CVD_Risk"].value_counts(normalize=True)
cvd_risk_counts_without_ldl = df_without_ldl["CVD_Risk"].value_counts(normalize=True)

print("\n")
print("CVD Risk patients label distribution (with LDL variable)")
print(cvd_risk_counts_with_ldl)
print("\n")
print("CVD Risk patients label distribution (without LDL variable)")
print(cvd_risk_counts_without_ldl)


# Train using Logistic Regression and Random Forest for evaluation
def train_selected_models(df):
    # Drop identifier column
    df = df.drop(columns=["SEQN"])

    # Define features and target
    X = df.drop(columns=["CVD_Risk"])
    y = df["CVD_Risk"]

    # Split data into train and test sets (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Standardize numerical features
    scaler = StandardScaler()
    X_train.iloc[:, :-8] = scaler.fit_transform(X_train.iloc[:, :-8])
    X_test.iloc[:, :-8] = scaler.transform(X_test.iloc[:, :-8])

    # Initialize models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
    }

    results = {}

    # Train and evaluate models
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Store performance metrics
        results[name] = {
            "Accuracy": accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred),
            "Recall": recall_score(y_test, y_pred),
            "F1 Score": f1_score(y_test, y_pred)
        }

    return results

# Retrain models on both datasets
results_with_ldl = train_selected_models(df_with_ldl)
results_without_ldl = train_selected_models(df_without_ldl)

# Function to display model performance in a readable format
def print_model_performance(results, dataset_name):
    print(f"\n--- Model Performance ({dataset_name}) ---")
    for model, metrics in results.items():
        print(f"\nModel: {model}")
        print("-" * 30)
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")

# Print results for both datasets
print_model_performance(results_with_ldl, "With LDL")
print_model_performance(results_without_ldl, "Without LDL")

def save_model_performance(results, dataset_name, resfile="modelresults.txt"):
    filename = os.path.join(files_outputFolder, resfile)
    with open(filename, "a") as file:
        file.write(f"\n--- Model Performance ({dataset_name}) ---\n")
        for model, metrics in results.items():
            file.write(f"\nModel: {model}\n")
            file.write("-" * 30 + "\n")
            for metric, value in metrics.items():
                file.write(f"{metric}: {value:.4f}\n")

# Example usage (replace with actual results dictionary)
save_model_performance(results_with_ldl, "With LDL")
save_model_performance(results_without_ldl, "Without LDL")
