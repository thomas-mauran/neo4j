from pyspark.sql import SparkSession

# Replace with your actual Neo4j credentials and connection URI
url = "neo4j://localhost:7687"  # URL of your Neo4j instance
username = "neo4j"  # Your Neo4j username
password = "password"  # Your Neo4j password
dbname = "neo4j"  # Your Neo4j database name (optional for Neo4j 4.x and higher)

# Create a Spark session and connect it to Neo4j
spark = (
    SparkSession.builder.config("neo4j.url", url)
    .config("neo4j.authentication.basic.username", username)
    .config("neo4j.authentication.basic.password", password)
    .config("neo4j.database", dbname)
    .getOrCreate()
)

# Read all nodes from Neo4j
# Use a Cypher query to get all nodes from the graph database
df = (
    spark.read.format("org.neo4j.spark.DataSource")
    .option("query", "MATCH (n) RETURN n")  # Cypher query to get all nodes
    .load()
)

# Show the DataFrame, which contains the nodes
df.show(truncate=False)

# Optionally, you can also print the schema of the DataFrame to understand the structure
df.printSchema()

# Stop the Spark session
spark.stop()
