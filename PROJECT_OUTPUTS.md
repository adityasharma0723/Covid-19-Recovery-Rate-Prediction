# COVID-19 Recovery Rate Prediction - Complete Project Outputs

This document compiles the complete terminal logs, statistical outputs, metrics, and dataset summaries produced across all stages of the project execution.

---

## 1. Spark Session & Dataset Ingestion (`main.py`)

**Description:** Initialization of Spark Session, loading original 70,000-record COVID-19 dataset, displaying schema, columns, and initial records.

```text
Spark Session Created Successfully!

Dataset Loaded Successfully!

First 10 Records:
+----------+--------+------------+-------------+---+------+-------------+-------------+-------------+-------------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------+-----+----------------+-------------+---------------+---------+---------------+---------------+----------------------+
|patient_id|country |region/state|date_reported|age|gender|comorbidities|symptoms_1   |symptoms_2   |symptoms_3   |severity|hospitalized|icu_admission|ventilator_support|vaccination_status|variant|treatment_given_1|treatment_given_2|days_to_recovery|recovered|death|date_of_recovery|date_of_death|tests_conducted|test_type|hospital_name  |doctor_assigned|source_url            |
+----------+--------+------------+-------------+---+------+-------------+-------------+-------------+-------------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------+-----+----------------+-------------+---------------+---------+---------------+---------------+----------------------+
|P000001   |India   |Sindh       |44447        |95 |Female|Diabetes     |Cough        |NULL         |NULL         |Moderate|0           |1            |1                 |Full              |Omicron|Antibiotics      |NULL             |18              |0        |1    |44465           |NULL         |1              |PCR      |Aga Khan       |Dr. Müller     |https://who.int/sample|
|P000002   |Pakistan|London      |43930        |92 |Female|Diabetes     |Loss of Smell|Fatigue      |Fatigue      |Moderate|0           |1            |1                 |None              |Omicron|Remdesivir       | Antibiotics     |9               |0        |1    |43939           |NULL         |3              |PCR      |Jinnah Hospital|Dr. Silva      |https://who.int/sample|
|P000003   |Germany |Berlin      |44718        |78 |Female|None         |Headache     |Loss of Smell|Loss of Smell|Critical|0           |0            |0                 |None              |Omicron|Antibiotics      | Oxygen          |27              |0        |1    |44745           |NULL         |2              |Antigen  |Jinnah Hospital|Dr. Smith      |https://who.int/sample|
|P000004   |India   |Cape Town   |44107        |36 |Female|Cancer       |Cough        |Fatigue      |Fatigue      |Mild    |1           |1            |1                 |Full              |Omicron|Antibiotics      |NULL             |25              |1        |1    |44132           |NULL         |2              |PCR      |Mayo Clinic    |Dr. Silva      |https://who.int/sample|
|P000005   |UK      |Berlin      |44083        |99 |Male  |Diabetes     |Fatigue      |NULL         |NULL         |Mild    |1           |1            |1                 |None              |Omicron|Oxygen           | Steroids        |17              |0        |0    |NULL            |44123        |4              |PCR      |AIIMS          |Dr. Smith      |https://who.int/sample|
|P000006   |Brazil  |Cape Town   |44441        |75 |Female|Hypertension |Cough        |NULL         |NULL         |Mild    |1           |1            |1                 |None              |Alpha  |Oxygen           |NULL             |25              |1        |1    |44466           |NULL         |4              |PCR      |Mayo Clinic    |Dr. Silva      |https://who.int/sample|
|P000007   |China   |São Paulo   |44722        |71 |Male  |Cancer       |Fever        |Loss of Smell|Loss of Smell|Moderate|0           |1            |1                 |None              |Delta  |Steroids         |NULL             |5               |1        |0    |NULL            |44746        |3              |PCR      |NHS Trust      |Dr. Khan       |https://who.int/sample|
|P000008   |UK      |California  |44666        |48 |Male  |Heart Disease|Fever        |Loss of Smell|Loss of Smell|Mild    |1           |1            |1                 |None              |Delta  |Oxygen           | Paracetamol     |12              |1        |0    |NULL            |44675        |1              |PCR      |Charité        |Dr. Silva      |https://who.int/sample|
|P000009   |USA     |California  |43954        |85 |Female|Heart Disease|Fatigue      |NULL         |NULL         |Mild    |1           |1            |1                 |Full              |Omicron|Remdesivir       |NULL             |17              |0        |0    |NULL            |43974        |3              |Antigen  |NHS Trust      |Dr. Silva      |https://who.int/sample|
|P000010   |UK      |Punjab      |44050        |44 |Male  |Heart Disease|Cough        |Loss of Smell|Loss of Smell|Mild    |1           |1            |1                 |Full              |Alpha  |Paracetamol      |NULL             |15              |0        |1    |44065           |NULL         |2              |Antigen  |Charité        |Dr. Silva      |https://who.int/sample|
+----------+--------+------------+-------------+---+------+-------------+-------------+-------------+-------------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------+-----+----------------+-------------+---------------+---------+---------------+---------------+----------------------+
only showing top 10 rows

Dataset Columns:
['patient_id', 'country', 'region/state', 'date_reported', 'age', 'gender', 'comorbidities', 'symptoms_1', 'symptoms_2', 'symptoms_3', 'severity', 'hospitalized', 'icu_admission', 'ventilator_support', 'vaccination_status', 'variant', 'treatment_given_1', 'treatment_given_2', 'days_to_recovery', 'recovered', 'death', 'date_of_recovery', 'date_of_death', 'tests_conducted', 'test_type', 'hospital_name', 'doctor_assigned', 'source_url']

Dataset Schema:
root
 |-- patient_id: string (nullable = true)
 |-- country: string (nullable = true)
 |-- region/state: string (nullable = true)
 |-- date_reported: integer (nullable = true)
 |-- age: integer (nullable = true)
 |-- gender: string (nullable = true)
 |-- comorbidities: string (nullable = true)
 |-- symptoms_1: string (nullable = true)
 |-- symptoms_2: string (nullable = true)
 |-- symptoms_3: string (nullable = true)
 |-- severity: string (nullable = true)
 |-- hospitalized: integer (nullable = true)
 |-- icu_admission: integer (nullable = true)
 |-- ventilator_support: integer (nullable = true)
 |-- vaccination_status: string (nullable = true)
 |-- variant: string (nullable = true)
 |-- treatment_given_1: string (nullable = true)
 |-- treatment_given_2: string (nullable = true)
 |-- days_to_recovery: integer (nullable = true)
 |-- recovered: integer (nullable = true)
 |-- death: integer (nullable = true)
 |-- date_of_recovery: integer (nullable = true)
 |-- date_of_death: integer (nullable = true)
 |-- tests_conducted: integer (nullable = true)
 |-- test_type: string (nullable = true)
 |-- hospital_name: string (nullable = true)
 |-- doctor_assigned: string (nullable = true)
 |-- source_url: string (nullable = true)

Total Records: 70000

Spark Session Closed Successfully!
```

---

## 2. Exploratory Data Analysis (EDA) (`data_analysis.py`)

**Description:** Statistical summary of features, missing values analysis, duplicate checks, patient recovery duration distributions, and outcome checks.

```text
========== DATASET OVERVIEW ==========
Total Records: 70000
Total Columns: 28

Column Names:
['patient_id', 'country', 'region/state', 'date_reported', 'age', 'gender', 'comorbidities', 'symptoms_1', 'symptoms_2', 'symptoms_3', 'severity', 'hospitalized', 'icu_admission', 'ventilator_support', 'vaccination_status', 'variant', 'treatment_given_1', 'treatment_given_2', 'days_to_recovery', 'recovered', 'death', 'date_of_recovery', 'date_of_death', 'tests_conducted', 'test_type', 'hospital_name', 'doctor_assigned', 'source_url']

Dataset Schema:
root
 |-- patient_id: string (nullable = true)
 |-- country: string (nullable = true)
 |-- region/state: string (nullable = true)
 |-- date_reported: integer (nullable = true)
 |-- age: integer (nullable = true)
 |-- gender: string (nullable = true)
 |-- comorbidities: string (nullable = true)
 |-- symptoms_1: string (nullable = true)
 |-- symptoms_2: string (nullable = true)
 |-- symptoms_3: string (nullable = true)
 |-- severity: string (nullable = true)
 |-- hospitalized: integer (nullable = true)
 |-- icu_admission: integer (nullable = true)
 |-- ventilator_support: integer (nullable = true)
 |-- vaccination_status: string (nullable = true)
 |-- variant: string (nullable = true)
 |-- treatment_given_1: string (nullable = true)
 |-- treatment_given_2: string (nullable = true)
 |-- days_to_recovery: integer (nullable = true)
 |-- recovered: integer (nullable = true)
 |-- death: integer (nullable = true)
 |-- date_of_recovery: integer (nullable = true)
 |-- date_of_death: integer (nullable = true)
 |-- tests_conducted: integer (nullable = true)
 |-- test_type: string (nullable = true)
 |-- hospital_name: string (nullable = true)
 |-- doctor_assigned: string (nullable = true)
 |-- source_url: string (nullable = true)

========== STATISTICAL SUMMARY ==========
+-------+----------+-------+------------+-----------------+------------------+------+-------------+-----------+-----------+-----------+--------+-------------------+-------------------+-------------------+------------------+-------+-----------------+-----------------+------------------+-------------------+-------------------+------------------+------------------+------------------+---------+-------------+---------------+--------------------+
|summary|patient_id|country|region/state|    date_reported|               age|gender|comorbidities| symptoms_1| symptoms_2| symptoms_3|severity|       hospitalized|      icu_admission| ventilator_support|vaccination_status|variant|treatment_given_1|treatment_given_2|  days_to_recovery|          recovered|              death|  date_of_recovery|     date_of_death|   tests_conducted|test_type|hospital_name|doctor_assigned|          source_url|
+-------+----------+-------+------------+-----------------+------------------+------+-------------+-----------+-----------+-----------+--------+-------------------+-------------------+-------------------+------------------+-------+-----------------+-----------------+------------------+-------------------+-------------------+------------------+------------------+------------------+---------+-------------+---------------+--------------------+
|  count|     70000|  70000|       70000|            70000|             70000| 70000|        70000|      70000|      46729|      46726|   70000|              70000|              70000|              70000|             70000|  70000|            70000|            35034|             70000|              70000|              70000|             53456|             16544|             70000|    70000|        70000|          70000|               70000|
|   mean|      NULL|   NULL|        NULL|44282.16924285714| 50.51202857142857|  NULL|         NULL|       NULL|       NULL|       NULL|    NULL| 0.5989571428571429| 0.8497857142857143| 0.9487714285714286|              NULL|   NULL|             NULL|             NULL|17.520714285714284|0.23635714285714285| 0.7636571428571428|44299.147878629155|44306.385819632495|3.0060714285714285|     NULL|         NULL|           NULL|                NULL|
| stddev|      NULL|   NULL|        NULL|259.9410799542566|28.900784252155127|  NULL|         NULL|       NULL|       NULL|       NULL|    NULL|0.49011316597502036|0.35728388947510104|0.22046518830342096|              NULL|   NULL|             NULL|             NULL| 7.509428697886681| 0.4248470576311795|0.42483819203682055| 260.1325503420151| 259.9926398589625|1.4141348663722535|     NULL|         NULL|           NULL|                NULL|
|    min|   P000001| Brazil|     Beijing|            43831|                 1|Female|       Asthma|      Cough|      Cough|      Cough|Critical|                  0|                  0|                  0|           Booster|  Alpha|      Antibiotics|      Antibiotics|                 5|                  0|                  0|             43836|             43837|                 1|  Antigen|        AIIMS|       Dr. Khan|https://who.int/s...|
|    max|   P070000|    USA|   São Paulo|            44731|               100|  Male|         None|Sore Throat|Sore Throat|Sore Throat|  Severe|                  1|                  1|                  1|           Partial|Omicron|         Steroids|         Steroids|                30|                  1|                  1|             44761|             44770|                 5|      PCR|    NHS Trust|      Dr. Smith|https://who.int/s...|
+-------+----------+-------+------------+-----------------+------------------+------+-------------+-----------+-----------+-----------+--------+-------------------+-------------------+-------------------+------------------+-------+-----------------+-----------------+------------------+-------------------+-------------------+------------------+------------------+------------------+---------+-------------+---------------+--------------------+

========== MISSING VALUES ==========
+----------+-------+------------+-------------+---+------+-------------+----------+----------+----------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------+-----+----------------+-------------+---------------+---------+-------------+---------------+----------+
|patient_id|country|region/state|date_reported|age|gender|comorbidities|symptoms_1|symptoms_2|symptoms_3|severity|hospitalized|icu_admission|ventilator_support|vaccination_status|variant|treatment_given_1|treatment_given_2|days_to_recovery|recovered|death|date_of_recovery|date_of_death|tests_conducted|test_type|hospital_name|doctor_assigned|source_url|
+----------+-------+------------+-------------+---+------+-------------+----------+----------+----------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------+-----+----------------+-------------+---------------+---------+-------------+---------------+----------+
|0         |0      |0           |0            |0  |0     |0            |0         |23271     |23274     |0       |0           |0            |0                 |0                 |0      |0                |34966            |0               |0        |0    |16544           |53456        |0              |0        |0            |0              |0         |
+----------+-------+------------+-------------+---+------+-------------+----------+----------+----------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------+-----+----------------+-------------+---------------+---------+-------------+---------------+----------+

========== DUPLICATE RECORDS ==========
Total Records: 70000
Unique Records: 70000
Duplicate Records: 0

========== RECOVERY DAYS ANALYSIS ==========
+-------+------------------+
|summary|  days_to_recovery|
+-------+------------------+
|  count|             70000|
|   mean|17.520714285714284|
| stddev| 7.509428697886681|
|    min|                 5|
|    max|                30|
+-------+------------------+

========== PATIENT OUTCOMES ==========
+---------+-----+-----+
|recovered|death|count|
+---------+-----+-----+
|        1|    0| 4059|
|        1|    1|12486|
|        0|    0|12485|
|        0|    1|40970|
+---------+-----+-----+

========== CONTRADICTORY RECORDS ==========
Patients marked both recovered and dead: 12486

DATA ANALYSIS COMPLETED!
```

---

## 3. Data Validation & Quality Checks (`data_validation.py`)

**Description:** Source URL checks, outcome consistency, ICU and ventilator distribution, and recovery days analysis across patient groups.

```text
========== SOURCE URL ANALYSIS ==========
+----------------------+-----+
|source_url            |count|
+----------------------+-----+
|https://who.int/sample|70000|
+----------------------+-----+

========== OUTCOME VALIDATION ==========
+---------+-----+-----+
|recovered|death|count|
+---------+-----+-----+
|        1|    0| 4059|
|        1|    1|12486|
|        0|    0|12485|
|        0|    1|40970|
+---------+-----+-----+

========== ICU DISTRIBUTION ==========
+-------------+-----+
|icu_admission|count|
+-------------+-----+
|            1|59485|
|            0|10515|
+-------------+-----+

========== VENTILATOR DISTRIBUTION ==========
+------------------+-----+
|ventilator_support|count|
+------------------+-----+
|                 1|66414|
|                 0| 3586|
+------------------+-----+

========== RECOVERY DAYS BY OUTCOME ==========
+---------+-----+------------------------+
|recovered|death|distinct_recovery_values|
+---------+-----+------------------------+
|        1|    0|                      26|
|        1|    1|                      26|
|        0|    0|                      26|
|        0|    1|                      26|
+---------+-----+------------------------+

========== DATE SAMPLE ==========
+-------------+----------------+-------------+
|date_reported|date_of_recovery|date_of_death|
+-------------+----------------+-------------+
|        44447|           44465|         NULL|
|        43930|           43939|         NULL|
|        44718|           44745|         NULL|
|        44107|           44132|         NULL|
|        44083|            NULL|        44123|
|        44441|           44466|         NULL|
|        44722|            NULL|        44746|
|        44666|            NULL|        44675|
|        43954|            NULL|        43974|
|        44050|           44065|         NULL|
+-------------+----------------+-------------+
only showing top 10 rows

DATA VALIDATION COMPLETED!
```

---

## 4. Data Cleaning & Preprocessing (`data_cleaning.py`)

**Description:** Filtering valid recovery cohort (70,000 -> 4,059), imputing categorical missing values with Unknown, trimming whitespace, dropping irrelevant columns, and exporting cleaned dataset.

```text
Spark Session Created Successfully!

========== ORIGINAL DATASET ==========
Original Records: 70000
Original Columns: 28

========== FILTERED DATASET ==========
Valid Recovery Records: 4059

Missing categorical values handled!

Unnecessary columns removed!

========== WHITESPACE CLEANING ==========
+-----------------+-----------------+
|treatment_given_1|treatment_given_2|
+-----------------+-----------------+
|Steroids         |Unknown          |
|Oxygen           |Paracetamol      |
|Oxygen           |Unknown          |
|Steroids         |Oxygen           |
|Oxygen           |Steroids         |
|Paracetamol      |Unknown          |
|Oxygen           |Unknown          |
|Steroids         |Oxygen           |
|Paracetamol      |Unknown          |
|Paracetamol      |Unknown          |
+-----------------+-----------------+
only showing top 10 rows

========== REMAINING MISSING VALUES ==========
+------------+---+------+-------------+----------+----------+----------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------------+---------+
|region/state|age|gender|comorbidities|symptoms_1|symptoms_2|symptoms_3|severity|hospitalized|icu_admission|ventilator_support|vaccination_status|variant|treatment_given_1|treatment_given_2|days_to_recovery|tests_conducted|test_type|
+------------+---+------+-------------+----------+----------+----------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------------+---------+
|0           |0  |0     |0            |0         |0         |0         |0       |0           |0            |0                 |0                 |0      |0                |0                |0               |0              |0        |
+------------+---+------+-------------+----------+----------+----------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------------+---------+

========== CLEANED DATASET ==========
Total Records: 4059
Total Columns: 18

Dataset Schema:
root
 |-- region/state: string (nullable = false)
 |-- age: integer (nullable = true)
 |-- gender: string (nullable = false)
 |-- comorbidities: string (nullable = false)
 |-- symptoms_1: string (nullable = false)
 |-- symptoms_2: string (nullable = false)
 |-- symptoms_3: string (nullable = false)
 |-- severity: string (nullable = false)
 |-- hospitalized: integer (nullable = true)
 |-- icu_admission: integer (nullable = true)
 |-- ventilator_support: integer (nullable = true)
 |-- vaccination_status: string (nullable = false)
 |-- variant: string (nullable = false)
 |-- treatment_given_1: string (nullable = false)
 |-- treatment_given_2: string (nullable = false)
 |-- days_to_recovery: integer (nullable = true)
 |-- tests_conducted: integer (nullable = true)
 |-- test_type: string (nullable = false)

First 10 Cleaned Records:
+------------+---+------+-------------+----------+-------------+-------------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------------+---------+
|region/state|age|gender|comorbidities|symptoms_1|symptoms_2   |symptoms_3   |severity|hospitalized|icu_admission|ventilator_support|vaccination_status|variant|treatment_given_1|treatment_given_2|days_to_recovery|tests_conducted|test_type|
+------------+---+------+-------------+----------+-------------+-------------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------------+---------+
|São Paulo   |71 |Male  |Cancer       |Fever     |Loss of Smell|Loss of Smell|Moderate|0           |1            |1                 |None              |Delta  |Steroids         |Unknown          |5               |3              |PCR      |
|California  |48 |Male  |Heart Disease|Fever     |Loss of Smell|Loss of Smell|Mild    |1           |1            |1                 |None              |Delta  |Oxygen           |Paracetamol      |12              |1              |PCR      |
|Berlin      |6  |Female|Diabetes     |Cough     |Fatigue      |Fever        |Moderate|0           |1            |1                 |Booster           |Delta  |Oxygen           |Unknown          |10              |2              |Antigen  |
|London      |26 |Male  |None         |Cough     |Fever        |Unknown      |Critical|0           |0            |0                 |Full              |Omicron|Steroids         |Oxygen           |27              |4              |Antigen  |
|Cape Town   |69 |Male  |Asthma       |Fatigue   |Cough        |Unknown      |Mild    |1           |1            |1                 |None              |Delta  |Oxygen           |Steroids         |9               |5              |PCR      |
|Beijing     |90 |Female|Cancer       |Fever     |Unknown      |Cough        |Mild    |1           |1            |1                 |None              |Omicron|Paracetamol      |Unknown          |12              |2              |Antigen  |
|São Paulo   |58 |Male  |Diabetes     |Fever     |Unknown      |Unknown      |Mild    |1           |1            |1                 |None              |Omicron|Oxygen           |Unknown          |15              |3              |PCR      |
|Cape Town   |45 |Male  |Hypertension |Fatigue   |Unknown      |Unknown      |Critical|0           |0            |0                 |None              |Omicron|Steroids         |Oxygen           |11              |3              |Antigen  |
|Sindh       |86 |Male  |Cancer       |Fever     |Unknown      |Unknown      |Mild    |1           |1            |1                 |None              |Delta  |Paracetamol      |Unknown          |22              |2              |Antigen  |
|Berlin      |83 |Male  |Asthma       |Fever     |Loss of Smell|Loss of Smell|Moderate|0           |1            |1                 |None              |Delta  |Paracetamol      |Unknown          |11              |5              |PCR      |
+------------+---+------+-------------+----------+-------------+-------------+--------+------------+-------------+------------------+------------------+-------+-----------------+-----------------+----------------+---------------+---------+
only showing top 10 rows

========== RECOVERY STATISTICS ==========
+-------+------------------+
|summary|  days_to_recovery|
+-------+------------------+
|  count|              4059|
|   mean|17.575511209657552|
| stddev| 7.436400387159563|
|    min|                 5|
|    max|                30|
+-------+------------------+

Cleaned Dataset Saved Successfully!

DATA CLEANING COMPLETED SUCCESSFULLY!
```

---

## 5. Feature Engineering & ML Pipeline (`feature_engineering.py`)

**Description:** Dataset splitting (80% train, 20% test), median imputation of numerical features, StringIndexing and OneHotEncoding of categorical variables, VectorAssembler, StandardScaler, and fitted Pipeline export.

```text
Spark Session Created Successfully!

========== LOADED CLEANED DATASET ==========
Total Records: 4059
Total Columns: 18

========== DATASET SPLITTING ==========
Training Records: 3305
Testing Records: 754

========== FEATURE ENGINEERING RESULTS ==========
Training Records: 3305
Testing Records: 754

Processed Training Data:
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+
|features                                                                                                                                                                                                 |label|
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+
|(77,[0,1,2,3,4,6,15,20,25,32,40,47,53,59,62,67,75],[-1.940290055030614,0.9863264597959708,0.6242639116644927,0.359309604398472,-0.017370773758250947,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])   |23.0 |
|(77,[0,1,2,3,4,6,15,20,28,35,43,47,53,57,65,71,74],[-1.940290055030614,0.9863264597959708,0.6242639116644927,0.359309604398472,1.4001701465135874,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])      |7.0  |
|(77,[0,1,2,3,4,6,15,21,29,37,45,48,54,59,63,67,74],[-1.940290055030614,-1.0135563313854299,0.6242639116644927,0.359309604398472,1.4001701465135874,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])     |7.0  |
|(77,[0,1,2,3,4,6,15,17,26,35,43,50,52,57,63,69,74],[-1.940290055030614,-1.0135563313854299,-1.6014019222633915,-2.782273047815681,-0.017370773758250947,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])|8.0  |
|(77,[0,1,2,3,4,6,15,22,24,31,39,48,52,58,62,67,75],[-1.940290055030614,-1.0135563313854299,0.6242639116644927,0.359309604398472,-1.4349116940300892,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])    |9.0  |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+
only showing top 5 rows

Processed Data Schema:
root
 |-- features: vector (nullable = true)
 |-- label: double (nullable = true)

Processed datasets saved successfully!
Feature pipeline saved successfully!

FEATURE ENGINEERING COMPLETED!
```

---

## 6. Random Forest Model Training (`model_training.py`)

**Description:** Training 100-tree Random Forest Regressor on Spark, sample prediction evaluations, RMSE, MAE, R2 evaluation metrics, and saving predictions and trained model.

```text
Spark Session Created Successfully!

========== DATASET INFORMATION ==========
Training Records: 3305
Testing Records: 754

========== MODEL TRAINING ==========
Training Random Forest Regression Model...
Model Training Completed Successfully!

========== SAMPLE PREDICTIONS ==========
+-----+------------------+
|label|prediction        |
+-----+------------------+
|9.0  |18.30334932881446 |
|26.0 |17.61687973349931 |
|11.0 |17.494984744442196|
|15.0 |17.872912070704988|
|16.0 |17.647821161302858|
|27.0 |18.052911901057172|
|29.0 |17.54687810817452 |
|12.0 |18.21062328276133 |
|21.0 |17.83189760263484 |
|15.0 |17.974707663889816|
|21.0 |16.912877330326616|
|26.0 |17.126129153588405|
|19.0 |17.535786923984748|
|19.0 |18.1657861744199  |
|6.0  |17.700489908701698|
+-----+------------------+
only showing top 15 rows

========== MODEL EVALUATION ==========
Root Mean Squared Error (RMSE): 7.4898
Mean Absolute Error (MAE): 6.5084
R2 Score: -0.0064

Trained Model Saved Successfully!
Predictions Saved Successfully!

RANDOM FOREST MODEL TRAINING COMPLETED!
```

---

## 7. Model Diagnostics & Baseline Comparison (`model_diagnostics.py`)

**Description:** Evaluation of Random Forest vs Baseline mean model, feature importances computation, actual vs predicted and residual error analyses.

```text
Spark Session Created Successfully!

========== DATASET INFORMATION ==========
Training Records: 3305
Testing Records: 754

========== MODEL TRAINING ==========
Random Forest Model Trained Successfully!

========== SAMPLE PREDICTIONS ==========
+-----+------------------+
|label|prediction        |
+-----+------------------+
|9.0  |18.30334932881446 |
|26.0 |17.61687973349931 |
|11.0 |17.494984744442196|
|15.0 |17.872912070704988|
|16.0 |17.647821161302858|
|27.0 |18.052911901057172|
|29.0 |17.54687810817452 |
|12.0 |18.21062328276133 |
|21.0 |17.83189760263484 |
|15.0 |17.974707663889816|
+-----+------------------+
only showing top 10 rows

========== MODEL COMPARISON ==========
Metric  Random Forest  Baseline
  RMSE       7.489780  7.466238
   MAE       6.508420  6.492975
    R2      -0.006396 -0.000080

========== FEATURE IMPORTANCE ==========

Top 15 Important Features:
                              Feature  Importance
                     scaled_numeric_0    0.123259
                     scaled_numeric_4    0.056315
   treatment_given_1_encoded_Steroids    0.025874
       region_state_encoded_São Paulo    0.024999
treatment_given_2_encoded_Antibiotics    0.023263
 treatment_given_2_encoded_Remdesivir    0.022761
       region_state_encoded_Cape Town    0.022254
   treatment_given_2_encoded_Steroids    0.019926
             symptoms_1_encoded_Cough    0.018578
         comorbidities_encoded_Asthma    0.017747
treatment_given_1_encoded_Paracetamol    0.017199
                  gender_encoded_Male    0.016856
                test_type_encoded_PCR    0.016540
       symptoms_1_encoded_Sore Throat    0.016039
          region_state_encoded_Punjab    0.015902

========== DIAGNOSTIC SUMMARY ==========
Training Average: 17.59 days
Random Forest RMSE: 7.4898
Baseline RMSE: 7.4662
Random Forest MAE: 6.5084
Baseline MAE: 6.4930
Random Forest R2: -0.0064
Baseline R2: -0.0001

All diagnostic files saved in results/

MODEL DIAGNOSTICS COMPLETED!
```

---

