ExxonMobil DataWorks Challenge 2026

Machine Learning-Assisted History Matching and Production Forecasting

Project Overview

This project explores the application of machine learning to production history matching and forecasting. It uses production history and reservoir uncertainty parameters to develop a data-driven workflow for predicting cumulative oil, gas, and water production.

The project focuses on preparing production data, training a baseline machine learning model, evaluating predictions on validation cases, and generating predictions for test cases.

Objectives

Prepare and combine reservoir uncertainty parameters with historical production data.

Develop a baseline machine learning model to predict cumulative production.

Evaluate model performance using validation data.

Generate predictions for test cases.

Prepare predicted production values for the required Excel deliverable template.

Compare model performance against a simple baseline forecasting approach.

Technologies Used

Python — data processing, model development, and prediction generation.

Pandas — data manipulation and preparation.

NumPy — numerical operations.

Scikit-learn — machine learning pipelines, imputation, Extra Trees regression, and model evaluation.

OpenPyXL — Excel workbook processing.

Git and GitHub — source code version control.

Project Workflow

1. Data Inspection and Preparation

The workflow examines the reservoir uncertainty parameters and historical production datasets. The uncertainty parameters include:

Fault Transmissibility

Porosity Multiplier

Permeability Multiplier

Aquifer Pore Volume

The production datasets contain cumulative oil, gas, and water production observations.

The preparation process combines the uncertainty parameters with the corresponding production records and creates a structured dataset for model development.

2. Dataset Splitting

The current workflow uses the following case groups:

Dataset

Cases

Purpose

Training

1–70

Train the machine learning model

Validation

71–85

Evaluate model performance

Testing

86–100

Generate predictions for unseen cases

The split is based on case IDs. The test cases are kept separate from model training.

3. Baseline Machine Learning Model

An Extra Trees Regressor is used as the baseline machine learning model.

The model uses the four reservoir uncertainty parameters and elapsed time as input features to predict cumulative production.

The current model configuration includes:

200 decision trees

Minimum samples per leaf of 2

Maximum features set to 1.0

Random state of 42

Median imputation within a scikit-learn pipeline

Separate models are trained for cumulative oil, gas, and water production.

4. Model Evaluation

The model is evaluated using validation cases and Root Mean Squared Error (RMSE).

The validation results are also compared with a simple baseline approach to assess relative performance. Model performance should be interpreted in the context of the validation design, prediction horizon, and baseline methodology.

5. Test Case Predictions

The trained models generate predictions for Test Cases 86–100. The prediction output is saved as a CSV file for further processing.

6. Excel Deliverable Preparation

The fill_template.py script prepares a filled Excel workbook using the generated test predictions and the supplied deliverable template.

The current implementation maps template Cases 1–10 to Test Cases 86–95. This mapping is an assumption and must be confirmed against the official challenge requirements.

The current script also extends predictions beyond the available historical prediction dates using a simple final-year trend. These extended values are preliminary and should not be treated as validated long-term forecasts.

Source Code

The repository contains Python scripts for different stages of the workflow, including:

Script

Purpose

prepare_forecasting_data.py

Combines uncertainty parameters and production records into a structured dataset.

train_baseline_model.py

Trains the baseline Extra Trees models and evaluates validation performance.

predict_test_cases.py

Generates production predictions for the test cases.

compare_baselines.py

Compares the machine learning model with a simple baseline approach.

evaluate_validation.py

Evaluates predictions on the validation dataset.

check_forecasting_dates.py

Checks date coverage and observation counts across the dataset splits.

fill_template.py

Transfers test predictions into the Excel deliverable template.

Additional scripts in the repository support data inspection, history matching, and analysis of candidate cases.

Running the Workflow

Install the required Python packages:

pip install pandas numpy scikit-learn openpyxl joblib

Run the main workflow scripts from the project root:

python prepare_forecasting_data.py
python train_baseline_model.py
python predict_test_cases.py
python fill_template.py

Ensure that the required input datasets and Excel template are available in the locations expected by each script. Run the preparation and training stages before generating test predictions and filling the template.

The exact script execution order may depend on the paths and output files configured in each script.

Limitations and Future Improvements

The Extra Trees model is a baseline model and does not naturally extrapolate production trends beyond the range of dates represented in its training data.

Long-term forecasts extending to 2028 require a more appropriate forecasting strategy and additional validation.

The current Excel template case mapping must be confirmed against the official deliverable instructions.

Further testing is needed to assess forecast plausibility, cumulative production behaviour, and performance over different forecast horizons.

Additional forecasting approaches and time-based validation strategies can be explored to improve reliability.

Data and Confidentiality

This repository is intended to document the source code and modelling workflow.

Challenge-provided datasets, starter workbooks, and generated deliverables are not included in the public repository. The challenge materials should be handled in accordance with the official competition rules and confidentiality requirements.



