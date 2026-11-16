from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    StringIndexer,
    OneHotEncoder,
    Imputer,
    VectorAssembler,
    StandardScaler
)

spark = SparkSession.builder \
    .appName("COVID_Feature_Engineering") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("\nSpark Session Created Successfully!")

df = spark.read.csv(
    "data/cleaned_covid_dataset",
    header=True,
    inferSchema=True
)

print("\n========== LOADED CLEANED DATASET ==========")
print("Total Records:", df.count())
print("Total Columns:", len(df.columns))

df = df.withColumnRenamed("region/state", "region_state")

target_column = "days_to_recovery"

categorical_columns = [
    "region_state",
    "gender",
    "comorbidities",
    "symptoms_1",
    "symptoms_2",
    "symptoms_3",
    "severity",
    "vaccination_status",
    "variant",
    "treatment_given_1",
    "treatment_given_2",
    "test_type"
]

numeric_columns = [
    "age",
    "hospitalized",
    "icu_admission",
    "ventilator_support",
    "tests_conducted"
]

df = df.filter(
    col(target_column).isNotNull()
)

train_data, test_data = df.randomSplit(
    [0.8, 0.2],
    seed=42
)

print("\n========== DATASET SPLITTING ==========")
print("Training Records:", train_data.count())
print("Testing Records:", test_data.count())

imputed_columns = [
    column + "_imputed"
    for column in numeric_columns
]

imputer = Imputer(
    inputCols=numeric_columns,
    outputCols=imputed_columns
).setStrategy("median")

indexer = StringIndexer(
    inputCols=categorical_columns,
    outputCols=[
        column + "_index"
        for column in categorical_columns
    ],
    handleInvalid="keep"
)

encoder = OneHotEncoder(
    inputCols=[
        column + "_index"
        for column in categorical_columns
    ],
    outputCols=[
        column + "_encoded"
        for column in categorical_columns
    ],
    handleInvalid="keep"
)

numeric_assembler = VectorAssembler(
    inputCols=imputed_columns,
    outputCol="numeric_features",
    handleInvalid="keep"
)

scaler = StandardScaler(
    inputCol="numeric_features",
    outputCol="scaled_numeric",
    withStd=True,
    withMean=True
)

final_assembler = VectorAssembler(
    inputCols=["scaled_numeric"] + [
        column + "_encoded"
        for column in categorical_columns
    ],
    outputCol="features",
    handleInvalid="keep"
)

pipeline = Pipeline(
    stages=[
        imputer,
        indexer,
        encoder,
        numeric_assembler,
        scaler,
        final_assembler
    ]
)

pipeline_model = pipeline.fit(train_data)

train_processed = pipeline_model.transform(train_data)
test_processed = pipeline_model.transform(test_data)

train_final = train_processed.select(
    "features",
    col(target_column).cast("double").alias("label")
)

test_final = test_processed.select(
    "features",
    col(target_column).cast("double").alias("label")
)

print("\n========== FEATURE ENGINEERING RESULTS ==========")

print("Training Records:", train_final.count())
print("Testing Records:", test_final.count())

print("\nProcessed Training Data:")
train_final.show(5, truncate=False)

print("\nProcessed Data Schema:")
train_final.printSchema()

train_final.write.mode("overwrite").parquet(
    "data/train_features"
)

test_final.write.mode("overwrite").parquet(
    "data/test_features"
)

pipeline_model.write().overwrite().save(
    "models/feature_pipeline"
)

print("\nProcessed datasets saved successfully!")
print("Feature pipeline saved successfully!")

print("\nFEATURE ENGINEERING COMPLETED!")

spark.stop()
