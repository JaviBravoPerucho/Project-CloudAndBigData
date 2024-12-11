<h1 align="center"><b>Project</b></h1>

<h2 align="center"><b>Javier Bravo Perucho</b></h2>

## Description of the problem
Analyze and manipulate data from a database about the NBA to get information about shooting statistics and player performance.

## Need for Big Data processing and Cloud Computing.
I need to collect a lot of data about NBA players and seasons to classify players and analyze their performance through the years. I will use a database
from Kaggle that has 2.35 GB, and to search through it I will need to use libraries like Pandas and Spark. It takes a lot of time to process
such a big database with information about each basketball game and each player, so using resources from Cloud Computing like Dataproc clusters and Cloud storage
buckets will help me do it faster. 

## Description of the data: Where does it come from? How was it acquired? What does it mean? What format is it? How big is it (1 GB minimum)?
It is an SQLite database from Kaggle which contains information about 30 teams, 4800+ players and 65000+ games (every game since the NBA started). Its size 
is 2.35 GB and it has 11 tables: common_player_info, draft_combine_stats, draft_history, game, game_info, game_summary, inactive_players, line_score, officials,
other_stats and play_by_play. The most useful ones to me will probably be common_player_info, game, game_info and play_by_play.

## Description of the application, programming model(s), platform and infrastructure.
The analysis is performed using the Apache Spark framework, leveraging distributed computing to process large datasets efficiently.
The application scrapes NBA data for multiple seasons, processes the raw data, and stores it for further analysis. The data is loaded
into a Spark DataFrame for computation and sorted to extract insights like top 3-point shooters, field goal accuracy, and overall scoring performance.
Spark DataFrames provide a high-level abstraction for working with structured data, making it easier to perform transformations, filtering, and aggregations. Also, I
will use Google Cloud Dataproc clusters to process the dataset and Google Cloud Storage to store the results and scripts. I will use a Debian-based Virtual Machine to 
test the application locally before deploying it to the cloud.

## Software design (architectural design, code baseline, dependencies…)
## Usage (including screenshots that demonstrate how it works).
## Performance evaluation (speed-up) on the Cloud and discussion about identified overheads and optimizations done.
## Advanced features, like tools/models/platforms not explained in class, advanced functions, techniques to mitigate overheads, challenging implementation aspects...
## Conclusions, including goals achieved, improvements suggested, lessons learnt, future work, interesting insights…
## References.
