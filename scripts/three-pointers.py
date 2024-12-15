import sys
import re

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, round, sum

def extract_three_point_stats(input_path, output_path):

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("NBA Three Point Stats") \
        .getOrCreate()

    # Load the CSV file
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    # Filter for shooting-related events (eventmsgtype = 1 or 2)
    shooting_df = df.filter((col("eventmsgtype") == 1) | (col("eventmsgtype") == 2))

    # Filter rows with "3PT"
    three_point_shots = shooting_df.filter(col("homedescription").contains("3PT")|
        col("visitordescription").contains("3PT") |
        col("neutraldescription").contains("3PT"))
        
    # Calculate 3PM, 3PA, and 3P% for each player
    three_point_stats = three_point_shots.groupBy("player1_name").agg(
        sum(when(col("eventmsgtype") == 1, 1).otherwise(0)).alias("3pm"),  # 3-pointers made
        count("*").alias("3pa"),                                               # 3-pointers attempted
    ).withColumn(
        "3p_pct", round((col("3pm") / col("3pa")) * 100, 2)                # 3-point percentage
    )

    # Save the result to a CSV file
    three_point_stats.write.option("header", "true").csv(output_path)

if len(sys.argv) != 3:
    print("Usage: extract_three_point_stats <input> <output>")
    sys.exit(1)

extract_three_point_stats(sys.argv[1], sys.argv[2])