from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("WordCount").getOrCreate()

# Read input file
input_file = "README.md"
text_rdd = spark.sparkContext.textFile(input_file)

# Word count logic
word_counts = (
    text_rdd.flatMap(lambda line: line.split())  # Split lines into words
    .map(lambda word: (word, 1))                 # Map each word to (word, 1)
    .reduceByKey(lambda a, b: a + b)             # Reduce by key (word)
)

# Print results
for word, count in word_counts.collect():
    print(f"{word}: {count}")

# Stop Spark session
spark.stop()
