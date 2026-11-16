from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("COVID-19 Recovery Prediction") \
    .master("local[*]") \
    .getOrCreate()

print("Spark Session Created Successfully!")

df = spark.read.csv(
    "data/covid_dataset.csv",
    header=True,
    inferSchema=True
)

print("\nDataset Loaded Successfully!")

print("\nFirst 10 Records:")
df.show(10, truncate=False)

print("\nDataset Columns:")
print(df.columns)

print("\nDataset Schema:")
df.printSchema()

print("\nTotal Records:", df.count())

spark.stop()

print("\nSpark Session Closed Successfully!")
