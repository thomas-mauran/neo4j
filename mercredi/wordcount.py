from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, StringType
from pyspark.sql.functions import col

# Define input CSV file
csv_data_file = "stackoverflow.csv"

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Stackoverflow Application") \
    .config("spark.driver.memory", "8G") \
    .master("local[*]") \
    .getOrCreate()

# Set log level to reduce clutter
spark.sparkContext.setLogLevel("WARN")

# Define schema
schema = StructType() \
    .add("postTypeId", IntegerType(), nullable=True) \
    .add("id", IntegerType(), nullable=True) \
    .add("acceptedAnswer", StringType(), nullable=True) \
    .add("parentId", IntegerType(), nullable=True) \
    .add("score", IntegerType(), nullable=True) \
    .add("tag", StringType(), nullable=True)

# Read CSV file with schema, excluding header, and drop 'acceptedAnswer' column
df = spark.read \
    .option("header", "false") \
    .schema(schema) \
    .csv(csv_data_file) \
    .drop("acceptedAnswer")

# Count of records in CSV file
count = df.count()
print(f"\nCount of records in CSV file: {count}")

# Count null values in 'tag' and 'parentId' columns
tag_null_count = df.filter(col("tag").isNull()).count()
parentId_null_count = df.filter(col("parentId").isNull()).count()
print(f"\nCount tag null: {tag_null_count}")
print(f"Count parentId null: {parentId_null_count}")

# Filter posts with a score greater than 20
high_score_posts = df.filter(col("score") > 20)

# Print schema
df.printSchema()

# Show first 5 rows
df.show(5, truncate=False)

# Show first 5 rows of high score posts
print("\nPosts with score greater than 20:")
high_score_posts.show(5, truncate=False)

# Stop Spark session
spark.stop()
