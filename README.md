# khl-playoffs

A way to convert NHL player stats to fantasy hockey stats as a fill in for the 2020 NHL playoffs. This requires CSVs of player stats, and a roster CSV for each team. Examples from the 2019-2020 season are currently in this repository.

# Running

Run the `csv-converter.py` program to generate the csv. Output csv will follow `%m-%d-%Y_%H-%M_khl_2020_playoff_stats.csv` naming convention.

## Setup
You will need to ensure that the csv names specified in the top of `csv-converter.py` are all in the same root directory. You need to set the following variables:
* khl_roster_csv
* skater_stats_csv
* goalie_stats_csv

Default spreadsheets have been provided, but will need to be updated manually when you obtain new stats.

Examples of all CSVs included under `examples/`. Order is extremely important for the CSVS, it expects the headers and specific order found in the examples.

An example output in the same folder, called `khl_2020_playoff_DUMMY_stats.csv`
