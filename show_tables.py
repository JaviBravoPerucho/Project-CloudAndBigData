import sqlite3

# Path to the SQLite database file
db_path = "nba.sqlite"  # Replace with the actual path to your file

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    print(f"Connected to the database: {db_path}")

    # Create a cursor to execute SQL queries
    cursor = conn.cursor()

    # List all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(f"- {table[0]}")

    # Replace 'player_stats' with the actual table name containing shooting stats
    query = """
    SELECT team_id_home, season_id, fga3_home
    FROM game
    WHERE fg3a_home > 50  -- Filter players with at least 50 attempts
    ORDER BY fg3a_home DESC
    LIMIT 10;
    """
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch the results
    rows = cursor.fetchall()

    # Display results
    print("\nTop 3-point Shooters:")
    print("Player Name | Season | Team | Made | Attempted | Percentage")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]:.2f}")
    
except sqlite3.Error as e:
    print(f"SQLite error: {e}")
finally:
    if conn:
        conn.close()
        print("Database connection closed.")
