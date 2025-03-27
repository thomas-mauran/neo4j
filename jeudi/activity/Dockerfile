# Use the official Spark base image
FROM spark:3.5.3

# Download required Hadoop AWS and AWS SDK jars
# You can add the `hadoop-aws` and `aws-java-sdk` jars here, or copy them from your local system

ENV HADOOP_AWS_VERSION=3.3.4
ENV AWS_BUNDLE_VERSION=1.11.1026
ENV NEO4J_CONNECTOR_VERSION=5.3.5_for_spark_3

RUN mkdir -p /opt/spark/jars && \
    curl -L -o /opt/spark/jars/hadoop-aws.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar && \
    curl -L -o /opt/spark/jars/aws-java-sdk-bundle.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_BUNDLE_VERSION}/aws-java-sdk-bundle-${AWS_BUNDLE_VERSION}.jar && \
    curl -L -o /opt/spark/jars/neo4j-connector-apache-spark.jar https://repo1.maven.org/maven2/org/neo4j/neo4j-connector-apache-spark_2.12/${NEO4J_CONNECTOR_VERSION}/neo4j-connector-apache-spark_2.12-5.3.5_for_spark_3.jar  

# Set the working directory
WORKDIR /opt/spark/input


COPY stream.py /opt/spark/input/stream.py
COPY kafka.py /opt/spark/input/kafka.py

# Switch to root user to modify file permissions
USER root

RUN chmod -R 777 /opt/spark/input

RUN ls -l /opt/spark/input

# Set environment variables (optional but recommended)
ENV SPARK_HOME /opt/spark
ENV PATH $SPARK_HOME/bin:$PATH

# Optional: Switch back to the original Spark user if needed
# USER spark

