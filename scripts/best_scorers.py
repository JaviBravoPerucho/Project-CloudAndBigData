import sys
import re
import time
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def best_scorers(input_path, num_players):

    start_time = time.time()

   # Initialize Spark session
    spark = SparkSession.builder \
        .appName("NBA Best Scorers") \
        .getOrCreate()

    # Load the CSV file
    shooting_df = spark.read.csv(input_path, header=True, inferSchema=True)

    # Add a new column for the scoring metric
    scoring_df = shooting_df.withColumn(
        "scoring_metric",
        (F.col("fgm") * F.col("fg_pct") / 100) + F.col("fga")
    )
    num_players = int(num_players)
    # Find the top num_players players by scoring metric
    top_scorers = scoring_df.orderBy(F.col("scoring_metric").desc()).limit(num_players)

    # Show the results
    top_scorers.select("player1_name", "fgm", "fga", "fg_pct", "scoring_metric").show()

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")

if len(sys.argv) != 3:
    print("Usage: best_scorers <input> <num_players>")
    sys.exit(1)

best_scorers(sys.argv[1], sys.argv[2])