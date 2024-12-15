import sys
import re
import time
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def best_three_pointers(input_path, num_players):

    start_time = time.time()

   # Initialize Spark session
    spark = SparkSession.builder \
        .appName("NBA Best Three Point Shooters") \
        .getOrCreate()

    # Load the CSV file
    shooting_df = spark.read.csv(input_path, header=True, inferSchema=True)

    # Add a new column for the scoring metric
    scoring_df = shooting_df.withColumn(
        "scoring_metric",
        (F.col("3pm") * F.col("3p_pct") / 100) + F.col("3pa")
    )
    num_players = int(num_players)
    # Find the top num_players players by scoring metric
    top_scorers = scoring_df.orderBy(F.col("scoring_metric").desc()).limit(num_players)

    # Show the results
    top_scorers.select("player1_name", "3pm", "3pa", "3p_pct", "scoring_metric").show()

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

if len(sys.argv) != 3:
    print("Usage: best_three_pointers <input> <num_players>")
    sys.exit(1)

best_three_pointers(sys.argv[1], sys.argv[2])