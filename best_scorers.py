import sys
import re
from pyspark.sql import functions as F

def best_scorers(input_path):

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

    # Find the top 3 players by scoring metric
    top_scorers = scoring_df.orderBy(F.col("scoring_metric").desc()).limit(3)

    # Show the results
    top_scorers.select("player1_name", "fgm", "fga", "fg_pct", "scoring_metric").show()

if len(sys.argv) != 2:
    print("Usage: best_scorers <input>")
    sys.exit(1)

best_scorers(sys.argv[1])