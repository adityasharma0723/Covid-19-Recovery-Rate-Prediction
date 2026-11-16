from pyspark.sql import SparkSession
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

spark = SparkSession.builder \
    .appName("COVID_Random_Forest_Training") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("\nSpark Session Created Successfully!")

train_data = spark.read.parquet("data/train_features")
test_data = spark.read.parquet("data/test_features")

print("\n========== DATASET INFORMATION ==========")
print("Training Records:", train_data.count())
print("Testing Records:", test_data.count())

rf = RandomForestRegressor(
    featuresCol="features",
    labelCol="label",
    predictionCol="prediction",
    numTrees=100,
    maxDepth=5,
    seed=42
)

print("\n========== MODEL TRAINING ==========")
print("Training Random Forest Regression Model...")

model = rf.fit(train_data)

print("Model Training Completed Successfully!")

predictions = model.transform(test_data)

print("\n========== SAMPLE PREDICTIONS ==========")

predictions.select(
    "label",
    "prediction"
).show(15, truncate=False)

rmse_evaluator = RegressionEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="rmse"
)

mae_evaluator = RegressionEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="mae"
)

r2_evaluator = RegressionEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="r2"
)

rmse = rmse_evaluator.evaluate(predictions)
mae = mae_evaluator.evaluate(predictions)
r2 = r2_evaluator.evaluate(predictions)

print("\n========== MODEL EVALUATION ==========")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"R2 Score: {r2:.4f}")

model.write().overwrite().save(
    "models/random_forest_model"
)

print("\nTrained Model Saved Successfully!")

predictions.select(
    "label",
    "prediction"
).write.mode("overwrite").option(
    "header", True
).csv("data/model_predictions")

print("Predictions Saved Successfully!")

print("\nRANDOM FOREST MODEL TRAINING COMPLETED!")

spark.stop()
