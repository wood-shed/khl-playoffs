# khl-playoffs

A way to convert NHL player stats to fantasy hockey stats as a fill in for the 2020 NHL playoffs.

This queries the public NHL API that is documented in [this gitlab project here](https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md#people).2020

This program currently queries for the 2019-2020 playoffs and prints out a CSV of the players specified in the `khl_roster.csv` file.

## Setup
You will need to ensure that the csv named `khl_roster_csv` specified in the top of `generate_khl_stats.py` contains the name, nhl and khl team for each player.

You will need the `requests` module installed on your computer as well as [Python3](https://python.org). Install the requests module by running `python -m pip install requests` in your cmd/terminal.

## Running

Run the `generate_khl_stats.py` program to generate the csv. Output csv will follow `%m-%d-%Y_%H-%M_khl_2020_playoff_stats.csv` naming convention, copies of the stats used for reference will be placed in the `reference_stat_output` folder.

![output](./screenshots/output1.png)

