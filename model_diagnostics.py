from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, avg
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

import pandas as pd
import matplotlib.pyplot as plt
import os

spark = SparkSession.builder \
    .appName("COVID_Model_Diagnostics") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("\nSpark Session Created Successfully!")

os.makedirs("results", exist_ok=True)

train_data = spark.read.parquet("data/train_features")
test_data = spark.read.parquet("data/test_features")

print("\n========== DATASET INFORMATION ==========")
print("Training Records:", train_data.count())
print("Testing Records:", test_data.count())

print("\n========== MODEL TRAINING ==========")

rf = RandomForestRegressor(
    featuresCol="features",
    labelCol="label",
    predictionCol="prediction",
    numTrees=100,
    maxDepth=5,
    seed=42
)

model = rf.fit(train_data)

print("Random Forest Model Trained Successfully!")

predictions = model.transform(test_data)

print("\n========== SAMPLE PREDICTIONS ==========")

predictions.select(
    "label", "prediction"
).show(10, truncate=False)

def evaluate_model(data, prediction_col):

    results = {}

    for metric in ["rmse", "mae", "r2"]:

        evaluator = RegressionEvaluator(
            labelCol="label",
            predictionCol=prediction_col,
            metricName=metric
        )

        results[metric] = evaluator.evaluate(data)

    return results

rf_results = evaluate_model(predictions, "prediction")

average_recovery = train_data.select(
    avg("label")
).first()[0]

baseline_predictions = predictions.withColumn(
    "baseline_prediction",
    lit(average_recovery)
)

baseline_results = evaluate_model(
    baseline_predictions,
    "baseline_prediction"
)

comparison = pd.DataFrame({
    "Metric": ["RMSE", "MAE", "R2"],
    "Random Forest": [
        rf_results["rmse"],
        rf_results["mae"],
        rf_results["r2"]
    ],
    "Baseline": [
        baseline_results["rmse"],
        baseline_results["mae"],
        baseline_results["r2"]
    ]
})

print("\n========== MODEL COMPARISON ==========")
print(comparison.to_string(index=False))

comparison.to_csv(
    "results/model_comparison.csv",
    index=False
)

print("\n========== FEATURE IMPORTANCE ==========")

importance_values = model.featureImportances.toArray()

metadata = train_data.schema["features"].metadata

attributes = metadata.get(
    "ml_attr", {}
).get("attrs", {})

feature_names = {}

for attribute_group in attributes.values():
    for attribute in attribute_group:
        feature_names[attribute["idx"]] = attribute["name"]

importance_data = []

for index, importance in enumerate(importance_values):

    importance_data.append({
        "Feature": feature_names.get(
            index, f"Feature_{index}"
        ),
        "Importance": float(importance)
    })

importance_df = pd.DataFrame(importance_data)

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 15 Important Features:")
print(importance_df.head(15).to_string(index=False))

importance_df.to_csv(
    "results/feature_importance.csv",
    index=False
)

top_features = importance_df.head(15).sort_values(
    by="Importance"
)

plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"],
    top_features["Importance"]
)

plt.xlabel("Feature Importance")
plt.ylabel("Features")
plt.title("Top 15 Random Forest Feature Importances")

plt.tight_layout()

plt.savefig(
    "results/feature_importance.png",
    dpi=300
)

plt.close()

prediction_pd = predictions.select(
    "label", "prediction"
).toPandas()

plt.figure(figsize=(8, 6))

plt.scatter(
    prediction_pd["label"],
    prediction_pd["prediction"],
    alpha=0.6
)

minimum = min(
    prediction_pd["label"].min(),
    prediction_pd["prediction"].min()
)

maximum = max(
    prediction_pd["label"].max(),
    prediction_pd["prediction"].max()
)

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)

plt.xlabel("Actual Recovery Days")
plt.ylabel("Predicted Recovery Days")
plt.title("Actual vs Predicted Recovery Days")

plt.tight_layout()

plt.savefig(
    "results/actual_vs_predicted.png",
    dpi=300
)

plt.close()

prediction_pd["Error"] = (
    prediction_pd["label"] -
    prediction_pd["prediction"]
)

plt.figure(figsize=(8, 6))

plt.hist(
    prediction_pd["Error"],
    bins=20,
    edgecolor="black"
)

plt.xlabel("Prediction Error (Days)")
plt.ylabel("Number of Records")
plt.title("Distribution of Prediction Errors")

plt.tight_layout()

plt.savefig(
    "results/prediction_errors.png",
    dpi=300
)

plt.close()

prediction_pd.to_csv(
    "results/predictions.csv",
    index=False
)

print("\n========== DIAGNOSTIC SUMMARY ==========")

print(f"Training Average: {average_recovery:.2f} days")

print(f"Random Forest RMSE: {rf_results['rmse']:.4f}")
print(f"Baseline RMSE: {baseline_results['rmse']:.4f}")

print(f"Random Forest MAE: {rf_results['mae']:.4f}")
print(f"Baseline MAE: {baseline_results['mae']:.4f}")

print(f"Random Forest R2: {rf_results['r2']:.4f}")
print(f"Baseline R2: {baseline_results['r2']:.4f}")

print("\nAll diagnostic files saved in results/")

print("\nMODEL DIAGNOSTICS COMPLETED!")

spark.stop()
