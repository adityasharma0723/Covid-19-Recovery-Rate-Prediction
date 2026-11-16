from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct

spark = SparkSession.builder \
    .appName("COVID_Data_Validation") \
    .master("local[*]") \
    .getOrCreate()

df = spark.read.csv(
    "data/covid_dataset.csv",
    header=True,
    inferSchema=True
)
print("\n========== SOURCE URL ANALYSIS ==========")
df.groupBy("source_url").count().show(20, truncate=False)

print("\n========== OUTCOME VALIDATION ==========")
df.groupBy("recovered", "death").count().show()

print("\n========== ICU DISTRIBUTION ==========")
df.groupBy("icu_admission").count().show()

print("\n========== VENTILATOR DISTRIBUTION ==========")
df.groupBy("ventilator_support").count().show()

print("\n========== RECOVERY DAYS BY OUTCOME ==========")
df.groupBy("recovered", "death") \
    .agg(
        countDistinct("days_to_recovery")
        .alias("distinct_recovery_values")
    ).show()

print("\n========== DATE SAMPLE ==========")
df.select(
    "date_reported",
    "date_of_recovery",
    "date_of_death"
).show(10)
spark.stop()
print("\nDATA VALIDATION COMPLETED!")
