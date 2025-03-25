from pyspark.sql import SparkSession
from pyspark.sql.functions import col, collect_list

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("UsersTest") \
        .master("local[*]") \
        .getOrCreate()

    # Read the CSV file
    users_df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv("data/users.csv")

    # Filter, group by city, and collect names
    result = users_df \
        .filter(col("age") >= 25) \
        .groupBy("city") \
        .agg(collect_list("name").alias("names")) \
        .select("city", "names")

    # Collect and print results
    result_collected = result.collect()
    for row in result_collected:
        city = row["city"]
        names = row["names"]
        print(f"Users in {city}: {', '.join(names)}")

    # Stop Spark Session
    spark.stop()

if __name__ == "__main__":
    main()
