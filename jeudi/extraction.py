import re
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, udf, desc
from pyspark.sql.types import StringType, BooleanType, ArrayType, StructType, StructField

start_time = time.time()

spark = SparkSession.builder \
    .appName("Spark Wikipedia Analysis") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

file_path = "wikipedia.dat"
raw_data = spark.read.text(file_path)

def parse_wiki_page(page_string):
    title_match = re.search(r"<title>(.*?)</title>", page_string)
    text_match = re.search(r"<text>(.*?)</text>", page_string, re.DOTALL)
    
    title = title_match.group(1) if title_match else ""
    text = text_match.group(1) if text_match else ""
    is_redirect = "#REDIRECT" in text  # Boolean check for redirects
    
    return (title, text, is_redirect)

parsed_rdd = raw_data.rdd.map(lambda row: parse_wiki_page(row.value))

schema = StructType([
    StructField("title", StringType(), True),
    StructField("text", StringType(), True),
    StructField("isRedirect", BooleanType(), True)
])

wiki_df = spark.createDataFrame(parsed_rdd, schema)

wiki_df.show(5, truncate=False)

wiki_df.groupBy("isRedirect").count().show()

category_pattern = re.compile(r"\[\[Category:(.*?)\]\]")

def extract_categories(text):
    return category_pattern.findall(text) if text else []

extract_categories_udf = udf(extract_categories, ArrayType(StringType()))

wiki_with_categories = wiki_df.withColumn("categories", extract_categories_udf(col("text")))

wiki_with_categories.select("title", "categories").show(truncate=False)

exploded_df = wiki_with_categories.withColumn("category", explode(col("categories")))

top_categories = exploded_df.groupBy("category").count().orderBy(desc("count")).limit(50)

top_categories.show(50, truncate=False)

execution_time = round(time.time() - start_time, 2)
print(f"\nProgram execution time: {execution_time} seconds")
print(".......Program *****Completed***** Successfully.....!\n")

# Stop Spark Session
spark.stop()
