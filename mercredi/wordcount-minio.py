from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def main():
    # Configuration for MinIO
    s3_endpoint = "http://minio.minio.svc.cluster.local:9000"  # MinIO endpoint in Kubernetes
    s3_access_key = "minio-access-key"  # Replace with your actual MinIO access key
    s3_secret_key = "minio-secret-key"  # Replace with your actual MinIO secret key
    s3_bucket = "spark"
    s3_readme = "README.md"  # Path to README.md in MinIO bucket

    # Initialize Spark session
    spark = (
        SparkSession.builder.appName("README Processing")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .getOrCreate()
    )

    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    # Set MinIO configurations for S3 access
    sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", s3_endpoint)
    sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", s3_access_key)
    sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", s3_secret_key)
    sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
    sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")

    # Construct the URI to the README.md on MinIO
    s3_readme_uri = f"s3a://{s3_bucket}/{s3_readme}"

    # Read the README.md file from MinIO as a plain text file
    print("\n=== Processing README.md from MinIO ===")
    readme_df = spark.read.text(s3_readme_uri)

    # Show schema and first 5 records
    print("\nSchema of README.md:")
    readme_df.printSchema()

    print("\nFirst 5 records in README.md:")
    readme_df.show(5, truncate=False)

    # Count total records in README.md
    total_count = readme_df.count()
    print(f"\nTotal records in README.md: {total_count}")

    # Count lines containing the word "Spark"
    spark_lines_count = readme_df.filter(col("value").contains("Spark")).count()
    print(f"\nNumber of lines containing the word 'Spark': {spark_lines_count}")

    # Query: Lines with more than 100 characters
    print("\n=== Lines with more than 100 characters ===")
    long_lines = readme_df.filter(col("value").rlike(r".{100,}"))
    long_lines.show(truncate=False)

    # Stop Spark session
    spark.stop()

if __name__ == "__main__":
    main()
