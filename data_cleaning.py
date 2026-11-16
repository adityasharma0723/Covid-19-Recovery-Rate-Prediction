from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, trim

spark = SparkSession.builder \
    .appName("COVID_Data_Cleaning") \
    .master("local[*]") \
    .getOrCreate()

print("\nSpark Session Created Successfully!")

df = spark.read.csv(
    "data/covid_dataset.csv",
    header=True,
    inferSchema=True
)

print("\n========== ORIGINAL DATASET ==========")
print("Original Records:", df.count())
print("Original Columns:", len(df.columns))

clean_df = df.filter(
    (col("recovered") == 1) &
    (col("death") == 0) &
    (col("days_to_recovery").isNotNull())
)

print("\n========== FILTERED DATASET ==========")
print("Valid Recovery Records:", clean_df.count())

categorical_columns = [
    "gender",
    "region/state",
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

clean_df = clean_df.fillna(
    "Unknown",
    subset=categorical_columns
)

print("\nMissing categorical values handled!")

columns_to_drop = [
    "patient_id",
    "country",
    "date_reported",
    "recovered",
    "death",
    "date_of_recovery",
    "date_of_death",
    "hospital_name",
    "doctor_assigned",
    "source_url"
]

clean_df = clean_df.drop(*columns_to_drop)

print("\nUnnecessary columns removed!")

for column_name in categorical_columns:
    clean_df = clean_df.withColumn(
        column_name,
        trim(col(column_name))
    )

print("\n========== WHITESPACE CLEANING ==========")

clean_df.select(
    "treatment_given_1",
    "treatment_given_2"
).show(10, truncate=False)

print("\n========== REMAINING MISSING VALUES ==========")

clean_df.select([
    count(
        when(col(c).isNull(), c)
    ).alias(c)
    for c in clean_df.columns
]).show(truncate=False)

print("\n========== CLEANED DATASET ==========")

print("Total Records:", clean_df.count())
print("Total Columns:", len(clean_df.columns))

print("\nDataset Schema:")
clean_df.printSchema()

print("\nFirst 10 Cleaned Records:")
clean_df.show(10, truncate=False)

print("\n========== RECOVERY STATISTICS ==========")

clean_df.select(
    "days_to_recovery"
).describe().show()

clean_df.coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("data/cleaned_covid_dataset")

print("\nCleaned Dataset Saved Successfully!")

spark.stop()

print("\nDATA CLEANING COMPLETED SUCCESSFULLY!")
