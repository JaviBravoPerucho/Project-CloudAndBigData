# Step 1: Define the list of years to scrape
years = list(range(1980, 2024))

# Step 2: Initialize an empty list to store all player stats
all_player_stats = []

# Step 3: Loop through each year and scrape data
for year in years:
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_totals.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the table with player stats
    table = soup.find("table", {"id": "totals_stats"})
    
    # Extract headers (column names)
    headers = [th.text for th in table.find_all("th")]

    # Extract player stats
    player_stats = []
    rows = table.find_all("tr")
    
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 0:  # Ignore rows without player data
            player_data = [col.text for col in cols]
            player_stats.append(player_data)
    
    # Convert player stats to DataFrame
    df = pd.DataFrame(player_stats, columns=headers[1:])  # Skip the first column (index)
    df["Season"] = year  # Add the season year

    # Add this season's data to the overall list
    all_player_stats.append(df)

    print(f"Scraped data for {year} season")

# Step 4: Concatenate all seasons' data into one DataFrame
final_df = pd.concat(all_player_stats, ignore_index=True)

# Step 5: Save the data to a CSV file
final_df.to_csv("nba_player_stats_all_seasons.csv", index=False)
