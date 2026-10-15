# ExxonMobil DataWorks Challenge 2026

## Machine Learning-Assisted History Matching and Production Forecasting

## 📌 Project Overview

This project explores the use of machine learning for production history matching and forecasting. It uses reservoir uncertainty parameters and historical production data to predict cumulative oil, gas, and water production.

The project covers data preparation, model training, validation, test prediction generation, and Excel deliverable preparation.

## 🎯 Objectives

- Prepare and combine reservoir uncertainty parameters with historical production data.
- Develop a baseline machine learning model.
- Evaluate model performance using validation cases.
- Generate predictions for unseen test cases.
- Prepare predicted production values for the Excel deliverable template.
- Compare model performance against a simple baseline approach.

## 🛠️ Technologies Used

- **Python** — Data processing and model development
- **Pandas** — Data manipulation and preparation
- **NumPy** — Numerical operations
- **Scikit-learn** — Machine learning and model evaluation
- **OpenPyXL** — Excel workbook processing
- **Git and GitHub** — Version control

## 📊 Project Workflow

### 1. Data Preparation

The workflow combines reservoir uncertainty parameters with historical production data.

The uncertainty parameters include:

- Fault Transmissibility
- Porosity Multiplier
- Permeability Multiplier
- Aquifer Pore Volume

The production data contains cumulative oil, gas, and water production records.

### 2. Dataset Splitting

The current workflow uses the following case groups:

| Dataset | Cases | Purpose |
| :--- | :--- | :--- |
| Training | 1–70 | Train the model |
| Validation | 71–85 | Evaluate model performance |
| Testing | 86–100 | Generate predictions for unseen cases |

### 3. Machine Learning Model

An **Extra Trees Regressor** is used as the baseline machine learning model.

**Input features:**
- Fault Transmissibility
- Porosity Multiplier
- Permeability Multiplier
- Aquifer Pore Volume
- Elapsed time

**Model configuration:**
- Number of trees: `200`
- Minimum samples per leaf: `2`
- Maximum features: `1.0`
- Random state: `42`
- Missing-value imputation: Median

Separate models are trained to predict cumulative oil, gas, and water production.

### 4. Model Evaluation

Model performance is evaluated using validation cases and Root Mean Squared Error (RMSE).

The results are compared against a simple baseline approach to assess relative performance.

### 5. Test Predictions

The trained models generate predictions for Test Cases 86–100. The predictions are saved in a CSV file for further processing.

### 6. Excel Deliverable

The `fill_template.py` script transfers the generated predictions into the Excel deliverable template.

The current implementation maps Template Cases 1–10 to Test Cases 86–95. This mapping must be confirmed against the official challenge requirements.

The script also extends predictions beyond the available historical dates using a simple final-year trend. These extended values are preliminary and have not been validated as reliable long-term forecasts.

## 📁 Main Python Scripts

| Script | Description |
| :--- | :--- |
| `prepare_forecasting_data.py` | Prepares the production dataset. |
| `train_baseline_model.py` | Trains the baseline machine learning models. |
| `predict_test_cases.py` | Generates predictions for the test cases. |
| `compare_baselines.py` | Compares model performance against a baseline. |
| `evaluate_validation.py` | Evaluates validation predictions. |
| `check_forecasting_dates.py` | Checks date coverage and observation counts. |
| `fill_template.py` | Fills the Excel deliverable template. |
| `inspect_history.py` | Inspects historical production data. |
| `compare_history_match.py` | Compares history-matching results. |
| `analyze_best_cases.py` | Analyses candidate history-matching cases. |

Additional scripts support data inspection and analysis.

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install pandas numpy scikit-learn openpyxl joblib
```

### 2. Run the Workflow

Run the scripts from the project root directory:

```bash
python prepare_forecasting_data.py
python train_baseline_model.py
python predict_test_cases.py
python fill_template.py
```

Ensure the required input files are available at the paths expected by each script.

## ⚠️ Limitations and Future Improvements

- The Extra Trees model does not naturally extrapolate production trends beyond its training date range.
- Forecasts extending to 2028 require a suitable forecasting method and additional validation.
- The mapping between template cases and test cases must be confirmed.
- Further evaluation is needed to assess forecast plausibility and performance over longer time horizons.

## 🔒 Data Confidentiality

Challenge-provided datasets, starter workbooks, and generated deliverables are excluded from this public repository.

All challenge materials must be handled in accordance with the official competition rules and confidentiality requirements..
