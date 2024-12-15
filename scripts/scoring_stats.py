import sys
import re
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, round

def extract_shooting_stats(input_path, output_path):

    start_time = time.time()

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("NBA Shooting Stats") \
        .getOrCreate()

    # Load the CSV file
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    # Filter for shooting-related events (eventmsgtype = 1 or 2)
    shooting_df = df.filter((col("eventmsgtype") == 1) | (col("eventmsgtype") == 2))

    # Compute shooting stats per player
    stats_df = shooting_df.groupBy("player1_name").agg(
        count(when(col("eventmsgtype") == 1, 1)).alias("fgm"),  # Count made shots
        count(when((col("eventmsgtype") == 1) | (col("eventmsgtype") == 2), 1)).alias("fga")  # Count attempts
    )

    # Add field goal percentage (FG%)
    stats_df = stats_df.withColumn("fg_pct", round(col("fgm") / col("fga") * 100, 2))

    # Save the result to a CSV file
    stats_df.write.option("header", "true").csv(output_path)

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")

if len(sys.argv) != 3:
    print("Usage: extract_shooting_stats <input> <output>")
    sys.exit(1)

extract_shooting_stats(sys.argv[1], sys.argv[2])