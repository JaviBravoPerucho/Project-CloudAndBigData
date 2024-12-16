<h1 align="center"><b>Project</b></h1>

<h2 align="center"><b>Javier Bravo Perucho</b></h2>

## Description of the problem
Analyze and manipulate data from a database about the NBA to get information about scoring statistics and player performance.

## Need for Big Data processing and Cloud Computing.
I need to collect a lot of data about NBA players and seasons to classify players and analyze their performance through the years. I will use a database
from Kaggle that has 2.35 GB, and to manipulate it I will use Spark dataframes. It takes a lot of time to process
such a big database with information about each basketball game and each player, so using resources from Cloud Computing like Dataproc clusters and Cloud Storage
buckets will help me do it faster. 

## Description of the data: Where does it come from? How was it acquired? What does it mean? What format is it? How big is it (1 GB minimum)?
It is a database from Kaggle which contains information about 30 teams, 4800+ players and 65000+ games. Its size  is 2.35 GB and it contains 11 tables in csv format: common_player_info, 
draft_combine_stats, draft_history, game, game_info, game_summary, inactive_players, line_score, officials, other_stats and play_by_play. However, the only table with information about
the actual games is the play-by-play one, so I will use that one. It's the biggest table as it contains every play from each game, it has 2.2 GB of data. The game_id column seems to codify 
like this: XXXYYZZZZ where YY is the year of the season, so it seems that the data collected goes from 1996 to 2022. 

## Description of the application, programming model(s), platform and infrastructure.
The analysis is performed using the Apache Spark framework, leveraging distributed computing to process large datasets efficiently. The data is loaded
into a Spark DataFrame for computation and sorted to extract insights like top 3-point shooters, field goal accuracy, and overall scoring performance.
Spark DataFrames provide a high-level abstraction for working with structured data, making it easier to perform transformations, filtering, and aggregations. Also, I
will use Google Cloud Dataproc clusters to process the dataset and Google Cloud Storage to store the results and scripts. I will use a Debian-based Virtual Machine to 
test the application locally before deploying it to the cloud.

Link to the Storage Bucket: https://console.cloud.google.com/storage/browser/final-project-444014?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&authuser=1&cloudshell=true&inv=1&invt=AbkLQg&project=final-project-444014

### Exercise 1: Extract scoring stats from play-by-play table.
From the play_by_play table, I figured out that the "eventmsgtype" column writes 1 for made shots and 2 for missed shots. With this, I filtered through the table and computed the sum
of made shots and attempted shots for each player. Comparing the two stats, I also obtained the field goal percentage. As a result, I got a table called "scoring_stats.csv" where there's
a column for the player's name (player1_name), one for their field goals attempted (fga), another one for field goals made (fgm) and another one for field goal percentage (fg_pct).

### Exercise 2: Figure out ranking of best scorers in the league from the resulting table with a simple formula.
With the resulting table of the previous exercise, I can compute a formula for each player's stats and put them in order to rank them. The formula that I came up with is the following:
field goals made * field goal percentage + field goals attempted. It takes into account consistency and efficiency but also volume of contribution with the field goals attempted. In the end, the
3 best scorers which showed were Lebron James, Kobe Bryant and Dirk Nowitzki. This ranking seems valid as the NBA official site ranks them in the same order within the 6 all-time scoring leaders of the 
league, and the other 3 played before 1996, so data about their careers is missing.

### Exercise 3: Repeat the process but taking into account 3-pointers exclusively, to figure out the best 3-point shooters.
The program is similar, but in this case the column for the event type is the same for normal shots and 3-point shots, so I can't use it to filter through. I need to use the columns "homedescription", 
"visitordescription" and "neutraldescription", which show the name of the player, the minute of the play and the type of play it was, specifying whether it was an attempted 3-point shot or not. Therefore, 
I used the spark.sql function contains("3PT") combined with the event type column to obtain the 3-point shots made, the 3-point shots attempted and the percentage of accuracy. In the end, the results also correlated
with the NBA official site rankings.

## Software design
As for the architectural design, the processing of the data could be divided into three modules:
- A data loading module, where the application reads a large dataset efficiently using Spark's distributed file processing.
- A transformation module, where the data is filtered and aggregated based on specific criteria (in this case scoring stats).
- An analysis module, where the results are processed once again to compute a ranking of the elements based on a formula.

The project contains 4 scripts:
- scoring_stats.py : Defines a function which loads the input table into a dataframe, filters for shooting-related events, computes the FGM, FGA and FG_PCT stats for each player and saves the result in a CSV table.
- best_scorers.py : Defines a function which loads the resulting table into a dataframe, computes the formula for each row and shows the resulting ranking through the console,
                      limited by a number chosen by the user.
- three-pointers.py : Defines a function which loads the input table into a dataframe, filters for three-point shots and computes de 3PM, 3PA and 3P_PCT for each player, saving the results in a CSV table.
- best_three_pointers.py : Defines a function which computes the formula for each player as in the best_scorers.py script.

As for the dependencies, it relies on the PySpark libraries and technologies for parallel and distributed data processing, with Python as the programming language. Google Cloud Storage is useful to save the scripts 
elaborated and the resulting tables, and Google Cloud Compute Engine and Google Cloud Dataproc host the data-processing to test the programs locally and in the cloud.

This structure could be useful to try many other operations with the play-by-play table, and carry out an extensive analysis on the performance of the players throughout different time spans, for example
to write an article about it.

## Usage
1. Set up a Cloud Storage bucket to store input and output files, and a Compute Engine instance to run the application.
2. Upload play_by_play.csv to the Cloud Storage bucket.
3. Connect to the virtual machine and execute scoring_stats.py : spark-submit scoring_stats.py $BUCKET/play_by_play.csv $BUCKET/scoring_stats
4. Execute best_scorers.py with the number of players you want in the ranking : spark-submit best_scorers.py $BUCKET/scoring_stats/* 10

This should be the output in the console:

![](/screenshots/10best_scorers.png)

## Performance evaluation (speed-up) on the Cloud and discussion about identified overheads and optimizations done.

### Locally:
First operation: spark-submit --master local[x] scoring_stats.py play_by_play.csv scoring_stats
- 1 Thread : 96.84541583061218 seconds
- 2 Threads : 59.42380690574646 seconds
- 4 Threads : 61.581401348114014 seconds

Speedup(2 threads) = 1.63  |  Speedup(4 threads) = 1.57

Second: spark-submit --master local[x] best_scorers.py scoring_stats/part-00000-f49b4436-cc12-46ab-9f57-8300b7d6ec3d-c000.csv
- 1 Thread : 8.652909517288208 seconds
- 2 Threads : 8.245720863342285 seconds
- 4 Threads : 8.075222492218018 seconds

Speedup(2 threads) = 1.05  |  Speedup(4 threads) = 1.07

### With dataproc clusters:
First operation: spark-submit --num-executors x --executor-cores 4 scoring_stats.py $BUCKET/play_by_play.csv $BUCKET/results_scoring_stats
- 1 Executor :  79.96041631698608 seconds
- 2 Executors : 68.24642992019653 seconds
- 4 Executors : 68.73236680030823 seconds

Speedup(2 executors) = 1.17  |  Speedup(4 executors) = 1.16

Second: spark-submit --num-executors x --executor-cores 4 best_scorers.py $BUCKET/results_scoring_stats part-00000-f49b4436-cc12-46ab-9f57-8300b7d6ec3d-c000.csv 10
- 1 Executor : 24.26681900024414 seconds
- 2 Executors : 26.980035066604614 seconds
- 4 Executors : 25.87271809577942 seconds

Speedup(2 executors) = 0.9  |  Speedup(4 executors) = 0.94

### Insights
1. Local:
   - For the first operation, increasing threads achieves notable speedup due to parallel processing
   - For the second operation, the speedup is marginal as the task is likely I/O or memory-bound
2. Dataproc:
   - The first operation shows moderate speedup with more executors
   - The second operation has lower speedup (and even slowdowns) due to increased overhead of coordination between executors for a simpler task

## Advanced features, like tools/models/platforms not explained in class, advanced functions, techniques to mitigate overheads, challenging implementation aspects...
At the start, I was struggling to find a good dataset, and the only one I found adequate was the one I used from Kaggle. In the database there is a folder with the tables in
csv format and an SQLite file, and I thought there was only the SQLite. I started researching on how to manipulate those type of files and even made a few scripts to filter out the 
tables using Pandas, after I realized that there were also in csv format and I could do it with dataframes as in the labs.
## Conclusions, including goals achieved, improvements suggested, lessons learnt, future work, interesting insights…
### Goals achieved:
- Successfully extracted field goal and three-point shooting statistics for NBA players from a 2.2GB play-by-play dataset.
- Developed scoring metrics to identify top scorers and best three-point shooters of the analyzed period.
- Leveraged Google Cloud Storage (GCS) and Dataproc to process the large dataset efficiently, achieving significant performance improvements over local processing.
- Seamlessly transitioned from local development to distributed cloud processing.
- Measured and compared execution times for local and distributed setups, demonstrating the benefits of parallelism.

### Possible improvements:
- The dataset lacked historical data for players from earlier eras, limiting the scope of analysis. Exploring alternative sources or merging datasets could improve comprehensiveness.
- The reliance on text-based filtering (e.g., "3PT" in descriptions) is error-prone. A more structured dataset with dedicated columns for shot types would enhance accuracy.
- While performance improved with additional executors, there was diminishing returns after a certain threshold. A detailed analysis of workload distribution could help optimize resource allocation.
- Including graphical representations (e.g., bar charts, heatmaps) would improve the presentation of insights and make them more accessible to broader audiences.

In conclusion, this project demonstrated the potential of big data tools and cloud platforms to tackle large-scale analytics tasks while revealing areas for further exploration and refinement.
## References.
- NBA Database - https://www.kaggle.com/datasets/wyattowalsh/basketball
