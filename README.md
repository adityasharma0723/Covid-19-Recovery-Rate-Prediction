# COVID-19 Recovery Rate Prediction Using Apache Spark & Machine Learning

A distributed big data pipeline and predictive modeling system designed to analyze patient clinical outcomes, clean large-scale epidemiological datasets, and predict COVID-19 patient recovery durations using **Apache Spark (PySpark)** and **Random Forest Regression**. Includes an interactive **Streamlit** dashboard for exploration, model diagnostics, and patient recovery estimation.

---

## 📌 Project Overview

- **Data Ingestion**: Distributed ingestion of 70,000 multi-centre COVID-19 patient records.
- **Exploratory Data Analysis & Validation**: Identification of contradictory records, missing-value profiling, outcome distributions, and ICU/ventilator correlations.
- **Data Cleaning**: Strict cohort filtration (70,000 records down to 4,059 valid recovered cases with complete timelines), whitespace normalization, and categorical imputation.
- **Feature Engineering Pipeline**: 80/20 train-test split, median imputation for numerical features, StringIndexing and OneHotEncoding for multi-class categorical features, StandardScaler, and VectorAssembler.
- **Machine Learning**: 100-tree Random Forest Regressor trained on Apache Spark MLlib, benchmarked against a baseline mean predictor.
- **Diagnostics & Visual Analytics**: RMSE, MAE, R² metrics, residual error distributions, actual vs. predicted analyses, and top 15 feature importances.
- **Interactive Dashboard**: Full-featured Streamlit application for live patient recovery estimation and cohort exploration.

---

## 📁 Repository Structure

```text
COVID-19-Recovery-Prediction/
├── data/
│   ├── covid_dataset.csv             # Raw multi-centre dataset (70,000 records)
│   ├── cleaned_covid_dataset/        # Filtered & cleaned recovery cohort (4,059 records)
│   ├── train_features/               # Spark MLlib training features (Parquet)
│   ├── test_features/                # Spark MLlib testing features (Parquet)
│   └── model_predictions/            # Exported test predictions (CSV)
├── models/
│   ├── feature_pipeline/             # Fitted PySpark ML Pipeline stages
│   └── random_forest_model/          # Fitted PySpark Random Forest Regressor
├── results/
│   ├── actual_vs_predicted.png       # Scatter plot of actual vs. predicted recovery days
│   ├── feature_importance.png        # Bar chart of top 15 model features
│   ├── prediction_errors.png         # Histogram of residual errors
│   ├── feature_importance.csv        # Numerical feature importance scores
│   ├── model_comparison.csv          # Random Forest vs. Baseline metrics table
│   └── predictions.csv               # Test set predictions and residual error values
├── app.py                            # Interactive Streamlit dashboard & clinical predictor
├── main.py                           # Spark session setup & raw dataset ingestion
├── data_analysis.py                  # Exploratory data analysis & statistical profiling
├── data_validation.py                # Data quality, ICU, ventilator & date validation
├── data_cleaning.py                  # Cohort filtration & preprocessing pipeline
├── feature_engineering.py            # Feature transformation & vector assembly
├── model_training.py                 # PySpark Random Forest model training & evaluation
├── model_diagnostics.py              # Diagnostics, residual analysis & visualization export
├── PROJECT_OUTPUTS.md                # Complete terminal logs and output metrics
├── requirements.txt                  # Python dependencies
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11+
- Java 8 or Java 11 (required for Apache Spark / PySpark execution)

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/adityasharma0723/Covid-19-Recovery-Rate-Prediction.git
cd Covid-19-Recovery-Rate-Prediction
python -m venv .venv

# On Windows:
.\.venv\Scripts\Activate.ps1

# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 🛠️ Execution Pipeline

Execute the pipeline in sequential order:

```bash
# 1. Initialize Spark session and load raw dataset
python main.py

# 2. Exploratory Data Analysis & Statistics
python data_analysis.py

# 3. Data validation and outcome consistency checks
python data_validation.py

# 4. Clean dataset & filter valid recovery cohort
python data_cleaning.py

# 5. Build feature engineering pipeline & vector representations
python feature_engineering.py

# 6. Train Random Forest regression model
python model_training.py

# 7. Generate diagnostic metrics & visual comparison plots
python model_diagnostics.py
```

All terminal logs and results are documented in detail in [PROJECT_OUTPUTS.md](PROJECT_OUTPUTS.md).

---

## 🩺 Interactive Streamlit Dashboard

Launch the interactive web application:

```bash
streamlit run app.py
```

### Dashboard Capabilities:
- **Executive Overview & KPIs**: Ingested vs. validated recovery cohort counts, viral variant breakdown, disease severity distribution.
- **Exploratory Data Analysis**: Interactive filters by variant, severity, age slider, and comorbidity/treatment impact charts.
- **Model Diagnostics**: Interactive actual vs. predicted scatter plots, residual error distribution, and top 15 feature importance scores.
- **Live Recovery Predictor**: Clinical calculator taking patient demographics, clinical status, and interventions to predict expected recovery days with 95% confidence intervals and acuity risk profiles.
- **Dataset Explorer**: Paginated table view of the cleaned dataset with CSV export.

---

## 📊 Key Results

| Metric | Random Forest Model | Baseline Predictor |
| :--- | :--- | :--- |
| **Root Mean Squared Error (RMSE)** | **7.4898 Days** | 7.4662 Days |
| **Mean Absolute Error (MAE)** | **6.5084 Days** | 6.4930 Days |
| **R² Score** | **-0.0064** | -0.0001 |

- **Top Features**: Scaled numerical features (patient age and diagnostic tests conducted) along with steroid administration, region of reporting, and antibiotic treatments exhibited the highest relative importance within the ensemble trees.
