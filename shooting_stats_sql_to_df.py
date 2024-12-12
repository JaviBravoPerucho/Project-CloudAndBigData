import sqlite3
import pandas as pd
from pyspark.sql import SparkSession

# Path to your SQLite file
sqlite_file = "path_to_dataset.sqlite"

# Connect to the SQLite database
conn = sqlite3.connect(sqlite_file)

# List all tables in the database (optional)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:", tables)

# Query the specific table you need
query = "SELECT common_player_info FROM shooting_stats"  # Replace with your table name
pandas_df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Initialize Spark session
spark = SparkSession.builder \
    .appName("SQLite to Spark") \
    .getOrCreate()

# Convert Pandas DataFrame to Spark DataFrame
spark_df = spark.createDataFrame(pandas_df)

# Show the Spark DataFrame
spark_df.show()