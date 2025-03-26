from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("MongoDB Integration") \
    .config("spark.mongodb.input.uri", "mongodb://mongo:27017/database_name.collection_name") \
    .config("spark.mongodb.output.uri", "mongodb://mongo:27017/database_name.collection_name") \
    .getOrCreate()

# Example dataframe
data = [("John", 28), ("Anna", 22), ("Peter", 35)]
df = spark.createDataFrame(data, ["name", "age"])

# Write to MongoDB
df.write.format("mongo").mode("overwrite").save()
