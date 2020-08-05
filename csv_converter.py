import csv
from shutil import copyfile
from datetime import datetime
from khl_stats_key import khl_value

##########################################
### Edit these variables for CSV names ###
##########################################
### see examples folder for mock csvs ####
##########################################

## KHL roster
khl_roster_csv = "khl_rosters.csv"

## Stats
# make sure these CSV names point the the latest stats for the week
skater_stats_csv = "2020_nhl_playoffs_skater_stats.csv"
goalie_stats_csv = "2020_nhl_playoffs_goalie_stats.csv"

# Skater data source: https://www.hockey-reference.com/playoffs/NHL_2020_skaters.html
# Goalie data source: https://www.hockey-reference.com/playoffs/NHL_2020_goalies.html

##########################################
################## END ###################
##########################################


# generate output csv name
now = datetime.now()
stats_csv_name = now.strftime("%m-%d-%Y_%H-%M_khl_2020_playoff_stats.csv")
nhl_skater_stats_name = now.strftime("reference_stat_output/%m-%d-%Y_%H-%M_skater_reference_stats.csv")
nhl_goalie_stats_name = now.strftime("reference_stat_output/%m-%d-%Y_%H-%M_goalie_reference_stats.csv")

# initialize yo dicts
stats_dict = {}
player_dict = {}
khl_team_dict = {}
khl_player_dict = {}

# build player_dict for skater stats using the skater_stats_csv
with open(skater_stats_csv, encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        split_name = (row[1].split('\\')[0])
        if split_name in player_dict.keys():
            pass
        else:
            player_dict[split_name] = {
                'Name': (split_name),
                'Team': row[3],
                'Pos': row[4],
                'G': row[6],
                'A': row[7],
                'PPG': row[12],
                'SHG': row[13],
                'GWG': row[14],
                'PPA': row[16],
                'SHA': row[17],
                'SOG': row[18],
                'BLK': row[22],
                'HIT': row[23],
                # zero out goalie stats
                'WIN': 0,
                'GA': 0,
                'SV': 0,
                'SO': 0,
                # calculate the khl point conversion by looking up the value with khl_value()
                'K_G': (int(row[6]) * (int(khl_value('G')))),
                'K_A': (int(row[7]) * (int(khl_value('A')))),
                'K_PPG': (int(row[12]) * (int(khl_value('PPP')))),
                'K_SHG': (int(row[13]) * (int(khl_value('SHG')))),
                'K_GWG': (int(row[14]) * (int(khl_value('GWG')))),
                'K_PPA': (int(row[16]) * (int(khl_value('PPP')))),
                'K_SHA': (int(row[17]) * (int(khl_value('SHA')))),
                'K_SOG': (float(row[18]) * (float(khl_value('SOG')))),
                'K_BLK': (int(row[22]) * (int(khl_value('BLK')))),
                'K_HIT': (int(row[23]) * (int(khl_value('HIT')))),
                # zero out goalie points
                'K_WIN': 0,
                'K_GA': 0,
                'K_SV': 0,
                'K_SO': 0
            }

# add goalies to the player_dict for skater stats using the goalie_stats_csv
with open(goalie_stats_csv, encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        split_name = (row[1].split('\\')[0])
        if split_name in player_dict.keys():
            pass
        else:
            player_dict[split_name] = {
                'Name': (split_name),
                'Team': row[3],
                'Pos': 'G',
                # zero out skater stats
                'G': 0,
                'A': 0,
                'PPG': 0,
                'SHG': 0,
                'GWG': 0,
                'PPA': 0,
                'SHA': 0,
                'SOG': 0,
                'BLK': 0,
                'HIT': 0,
                'WIN': row[6],
                'GA': row[8],
                'SV': row[10],
                'SO': row[13],
                # zero out skater stats
                'K_G': 0,
                'K_A': 0,
                'K_PPG': 0,
                'K_SHG': 0,
                'K_GWG': 0,
                'K_PPA': 0,
                'K_SHA': 0,
                'K_SOG': 0,
                'K_BLK': 0,
                'K_HIT': 0,
                # calculate the khl point conversion by looking up the value with khl_value()
                'K_WIN': (int(row[6]) * (int(khl_value('WIN')))),
                'K_GA': (int(row[8]) * (int(khl_value('GA')))),
                'K_SV': (float(row[10]) * (float(khl_value('SV')))),
                'K_SO': (int(row[13]) * (int(khl_value('SHO'))))
            }

# get KHL rosters from the
with open(khl_roster_csv, encoding="utf-8-sig") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    for row in csvreader:
        khl_player_dict[row[0]] = {
                'Name': row[0],
                'KHL_Team': row[1],
                'NHL_Team': row[2],
                'KHL_Points': 0
            }
        khl_team_dict[row[1]] ={
                'KHL_Team': row[1],
                'Team_Points': 0
        }

# write all of the stats to the stats_csv_name output & generate point totals per player while doing so
with open(stats_csv_name, 'w', newline='') as newcsv:
    csvwriter = csv.writer(newcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # write the header row for the CSV, make sure that this order matches the write output of the player_dict below
    csvwriter.writerow([
        'Name',
        'KHL_Team',
        'Team',
        'Pos',
        'G',
        'A',
        'PPG',
        'SHG',
        'GWG',
        'PPA',
        'SHA',
        'SOG',
        'BLK',
        'HIT',
        'WIN',
        'GA',
        'SV',
        'SO',
        'K_G',
        'K_A',
        'K_PPG',
        'K_SHG',
        'K_GWG',
        'K_PPA',
        'K_SHA',
        'K_SOG',
        'K_BLK',
        'K_HIT',
        'K_WIN',
        'K_GA',
        'K_SV',
        'K_SO',
        'K_TOTAL'
        ]
    )
# write the players into the stats_csv_name by iterating through the khl_player_dict and writing their stats from player_dict
    not_found = 0
    for player in khl_player_dict.values():
        pn = player['Name']
        pkt = player['KHL_Team']
        pnt = player['NHL_Team']
        if pn in player_dict:
            # ksum gathers all of the KHL points into a list to be summed
            # TODO: maybe put this crap into the khl_stats_key.py and call it as a function
            ksum = (player_dict[pn]['K_G'], player_dict[pn]['K_A'], player_dict[pn]['K_PPG'], player_dict[pn]['K_SHG'], player_dict[pn]['K_GWG'], player_dict[pn]['K_PPA'], player_dict[pn]['K_SHA'], player_dict[pn]['K_SOG'], player_dict[pn]['K_BLK'], player_dict[pn]['K_HIT'], player_dict[pn]['K_WIN'], player_dict[pn]['K_GA'], player_dict[pn]['K_SV'], player_dict[pn]['K_SO'])
            # add the summed khl points into the player_dict
            player['KHL_Points'] = sum(ksum)
            # write the csv row for the player by looking most values up in player_dict
            csvwriter.writerow([
                player_dict[pn]['Name'],
                pkt,
                pnt,
                player_dict[pn]['Pos'],
                player_dict[pn]['G'],
                player_dict[pn]['A'],
                player_dict[pn]['PPG'],
                player_dict[pn]['SHG'],
                player_dict[pn]['GWG'],
                player_dict[pn]['PPA'],
                player_dict[pn]['SHA'],
                player_dict[pn]['SOG'],
                player_dict[pn]['BLK'],
                player_dict[pn]['HIT'],
                player_dict[pn]['WIN'],
                player_dict[pn]['GA'],
                player_dict[pn]['SV'],
                player_dict[pn]['SO'],
                player_dict[pn]['K_G'],
                player_dict[pn]['K_A'],
                player_dict[pn]['K_PPG'],
                player_dict[pn]['K_SHG'],
                player_dict[pn]['K_GWG'],
                player_dict[pn]['K_PPA'],
                player_dict[pn]['K_SHA'],
                player_dict[pn]['K_SOG'],
                player_dict[pn]['K_BLK'],
                player_dict[pn]['K_HIT'],
                player_dict[pn]['K_WIN'],
                player_dict[pn]['K_GA'],
                player_dict[pn]['K_SV'],
                player_dict[pn]['K_SO'],
                sum(ksum)  # TODO: put this shit into a function like above
                ])
        elif pn in 'Name':
            pass
            print(f"This is name!!!!!!")  # this is my lazy way of dealing with the name column in the roster csv
        else:
            pass
            # if no player stats are found zero them out and print it out
            print(f"WARNING {pn} on {pkt} was not found!! stats will be zero")
            not_found = not_found + 1
            csvwriter.writerow([
                pn,
                pkt,
                pnt,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                ])

# total up the team scores to be printed as an output
for player in khl_player_dict.values():
    tsum = khl_team_dict[player['KHL_Team']]['Team_Points']
    psum = player['KHL_Points']
    khl_team_dict[player['KHL_Team']]['Team_Points'] = psum + tsum

# print out team totals for fun
print(f"\nTotal number of players not found: {not_found} \n")
for r in khl_team_dict.values():
    if r['KHL_Team'] in 'Team':
        pass
    else:
        print(f"{r['KHL_Team']} - {round(r['Team_Points'], 2)}")

print(f"\nStats can be found in {stats_csv_name}")
copyfile(skater_stats_csv, nhl_skater_stats_name)
print(f"{skater_stats_csv} copied to {nhl_skater_stats_name}")
copyfile(goalie_stats_csv, nhl_goalie_stats_name)
print(f"{goalie_stats_csv} copied to {nhl_goalie_stats_name}")

x = input("Press any key to exit")
