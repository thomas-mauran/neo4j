from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, udf, desc
from pyspark.sql.types import StringType, BooleanType, ArrayType
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import re

spark = SparkSession.builder \
    .appName("WikipediaStreamProcessing") \
    .master("local[*]") \
    .getOrCreate()

ssc = StreamingContext(spark.sparkContext, batchDuration=5)  # Process every 5 seconds

# Kafka Configuration
kafka_broker = "localhost:9092"
topic_name = "wikipedia_topic"

kafka_stream = KafkaUtils.createDirectStream(ssc, [topic_name], {"metadata.broker.list": kafka_broker})

def parse_wiki_page(page_string):
    title_match = re.search(r"<title>(.*?)</title>", page_string)
    text_match = re.search(r"<text>(.*?)</text>", page_string, re.DOTALL)
    
    title = title_match.group(1) if title_match else ""
    text = text_match.group(1) if text_match else ""
    is_redirect = "#REDIRECT" in text  # Boolean check for redirects
    
    return (title, text, is_redirect)

def process_rdd(time, rdd):
    if not rdd.isEmpty():
        # Parse each message (i.e., Wikipedia page data)
        parsed_data = rdd.map(lambda x: parse_wiki_page(x[1]))

        # Define schema and convert to DataFrame
        schema = ["title", "text", "isRedirect"]
        df = spark.createDataFrame(parsed_data, schema)

        category_pattern = re.compile(r"\[\[Category:(.*?)\]\]")

        def extract_categories(text):
            return category_pattern.findall(text) if text else []

        extract_categories_udf = udf(extract_categories, ArrayType(StringType()))

        wiki_with_categories = df.withColumn("categories", extract_categories_udf(col("text")))

        wiki_with_categories.select("title", "categories").show(truncate=False)

        exploded_df = wiki_with_categories.withColumn("category", explode(col("categories")))
        top_categories = exploded_df.groupBy("category").count().orderBy(desc("count")).limit(50)

        top_categories.show(50, truncate=False)

kafka_stream.foreachRDD(process_rdd)

ssc.start()
ssc.awaitTermination()
