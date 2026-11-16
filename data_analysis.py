from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, isnan

spark = SparkSession.builder \
    .appName("COVID_Data_Analysis") \
    .master("local[*]") \
    .getOrCreate()
df = spark.read.csv(
    "data/covid_dataset.csv",
    header=True,
    inferSchema=True
)
print("\n========== DATASET OVERVIEW ==========")
print("Total Records:", df.count())
print("Total Columns:", len(df.columns))
print("\nColumn Names:")
print(df.columns)
print("\nDataset Schema:")
df.printSchema()
print("\n========== STATISTICAL SUMMARY ==========")
df.describe().show()
print("\n========== MISSING VALUES ==========")
missing_values = df.select([
    count(
        when(
            col(c).isNull() |
            isnan(col(c)) if dict(df.dtypes)[c] in
            ["double", "float"] else col(c).isNull(),
            c

            
        )
    ).alias(c)
    for c in df.columns
])

missing_values.show(truncate=False)

print("\n========== DUPLICATE RECORDS ==========")

total_records = df.count()
unique_records = df.dropDuplicates().count()

print("Total Records:", total_records)
print("Unique Records:", unique_records)
print("Duplicate Records:", total_records - unique_records)

print("\n========== RECOVERY DAYS ANALYSIS ==========")

df.select("days_to_recovery").describe().show()

print("\n========== PATIENT OUTCOMES ==========")

df.groupBy("recovered", "death").count().show()

print("\n========== CONTRADICTORY RECORDS ==========")

df.filter(
    (col("recovered") == 1) &
    (col("death") == 1)
).count()

print("Patients marked both recovered and dead:",
      df.filter(
          (col("recovered") == 1) &
          (col("death") == 1)
      ).count())

spark.stop()

print("\nDATA ANALYSIS COMPLETED!")
