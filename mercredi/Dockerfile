# Use the official Spark base image
FROM spark:3.5.3

# Copy the Python script and README file into the container
COPY spark-pi.py /opt/spark/input/spark-pi.py
COPY README.md /opt/spark/input/README.md

# Set the working directory to the location where the files are copied
WORKDIR /opt/spark/input
