import csv
import json
import requests
import time
from datetime import datetime
from khl_stats_key import khl_value


## KHL roster CSV name/location
khl_roster_csv = "khl_rosters.csv"

## Running list of teams still active in the playoffs
active_playoff_teams = ['DAL',
                        'NYI',
                        'PHI',
                        'TBL',
                        'VGK']

## Any special case exemptions for players on active teams
inactive_players_active_teams = ['Tuukka Rask', 'Vladimir Tarasenko']
inactive_teams =['NJD', 'DET', 'BUF', 'SJS', 'ANH', 'LAK', 'OTT']

# Initialize dicts and lists
khl_player_dict = {}
khl_team_dict = {}
no_nhl_stats = []
player_dict = {}

# make file names
now = datetime.now()
stats_csv_name = now.strftime("%m-%d-%Y_%H-%M_khl_2020_playoff_stats.csv")
player_dict_json = now.strftime("reference_stat_output/%m-%d-%Y_%H-%M_stat_reference_stats.json")


### Functions
# base function for all api requests, returning requests in json
def nhl_api(path):
    base_url = 'https://statsapi.web.nhl.com/api/v1/'
    r = requests.get('{0}{1}'.format(base_url, path))
    return r.json()


# function that determines value of the ACTIVE stat based on team status and special case exceptions
def is_active(player_name, nhl_team, GP):
    if nhl_team in active_playoff_teams and player_name not in inactive_players_active_teams and GP > 0:
        ACTIVE = 'Active'
        return ACTIVE
    else:
        ACTIVE = 'Inactive'
        return ACTIVE


# function for writing skater stats to player_dict, zeros out goalie stats
def skater_stats(team, player, stats):
    player_name = player['person']['fullName']
    G = stats[0]['stat']['goals']
    A = stats[0]['stat']['assists']
    PPG = stats[0]['stat']['powerPlayGoals']
    SHG = stats[0]['stat']['shortHandedGoals']
    GWG = stats[0]['stat']['gameWinningGoals']
    PPA = (stats[0]['stat']['powerPlayPoints'] - stats[0]['stat']['powerPlayGoals'])
    SHA = (stats[0]['stat']['shortHandedPoints'] - stats[0]['stat']['shortHandedGoals'])
    SOG = stats[0]['stat']['shots']
    BLK = stats[0]['stat']['blocked']
    HIT = stats[0]['stat']['hits']
    GP = stats[0]['stat']['games']
    K_G = (int(G) * (int(khl_value('G'))))
    K_A = (int(A) * (int(khl_value('A'))))
    K_PPG = (int(PPG) * (int(khl_value('PPP'))))
    K_SHG = (int(SHG) * (int(khl_value('SHG'))))
    K_GWG = (int(GWG) * (int(khl_value('GWG'))))
    K_PPA = (int(PPA) * (int(khl_value('PPP'))))
    K_SHA = (int(SHA) * (int(khl_value('SHA'))))
    K_SOG = (float(SOG) * (float(khl_value('SOG'))))
    K_BLK = (int(BLK) * (int(khl_value('BLK'))))
    K_HIT = (int(HIT) * (int(khl_value('HIT'))))
    ACTIVE = is_active(player_name, team, GP)
    # put all of the KHL points into a list to be summed below
    ksum = [K_G, K_A, K_PPG, K_SHG, K_GWG, K_PPA, K_SHA, K_SOG, K_BLK, K_HIT]
    # add the player and stats into the player_dict
    player_dict[player_name] = {
        'Name': player_name,
        'Team': team,
        'Pos': player['position']['abbreviation'],
        'G': G,
        'A': A,
        'PPG': PPG,
        'SHG': SHG,
        'GWG': GWG,
        'PPA': PPA,
        'SHA': SHA,
        'SOG': SOG,
        'BLK': BLK,
        'HIT': HIT,
        # # zero out goalie stats
        'WIN': 0,
        'GA': 0,
        'SV': 0,
        'SO': 0,
        # calculate the khl point conversion by looking up the value with khl_value()
        'K_G': K_G,
        'K_A': K_A,
        'K_PPG': K_PPG,
        'K_SHG': K_SHG,
        'K_GWG': K_GWG,
        'K_PPA': K_PPA,
        'K_SHA': K_SHA,
        'K_SOG': K_SOG,
        'K_BLK': K_BLK,
        'K_HIT': K_HIT,
        # # zero out goalie points
        'K_WIN': 0,
        'K_GA': 0,
        'K_SV': 0,
        'K_SO': 0,
        'K_TOT': sum(ksum),
        'GP': GP,
        'ACTIVE': ACTIVE
    }


# function for writing goalie stats to player_dict, zeros out skater stats
def goalie_stats(team, player, stats):
    player_name = player['person']['fullName']
    WIN = stats[0]['stat']['wins']
    GA = stats[0]['stat']['goalsAgainst']
    SV = stats[0]['stat']['saves']
    SO = stats[0]['stat']['shutouts']
    GP = stats[0]['stat']['games']
    K_WIN = (int(WIN) * (int(khl_value('WIN'))))
    K_GA = (int(GA) * (int(khl_value('GA'))))
    K_SV = (float(SV) * (float(khl_value('SV'))))
    K_SO = (int(SO) * (int(khl_value('SHO'))))
    ACTIVE = is_active(player_name, team, GP)
    # put all of the KHL points into a list to be summed below
    ksum = [K_WIN, K_GA, K_SV, K_SO]
    # add the player and stats into the player_dict
    player_dict[player_name] = {
        'Name': player_name,
        'Team': team,
        'Pos': player['position']['abbreviation'],
        # # zero out skater stats
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
        'WIN': WIN,
        'GA': GA,
        'SV': SV,
        'SO': SO,
        # # zero out skater stats
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
        'K_WIN': K_WIN,
        'K_GA': K_GA,
        'K_SV': K_SV,
        'K_SO': K_SO,
        'K_TOT': sum(ksum),
        'GP': GP,
        'ACTIVE': ACTIVE
    }


# get KHL rosters from the khl_roster_csv location defined in the beginning and build dicts
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


# use the api to build the player_dict by looping through every player of every team
team_count = 1
teams = nhl_api('teams')
for t in teams['teams']:
    if t['abbreviation'] not in inactive_teams:
        roster = nhl_api(f"teams/{t['id']}/?expand=team.roster")
        roster = roster['teams'][0]['roster']
        print(f"\n# {team_count} {t['name']} with {len(roster['roster'])} listed players")
        team_count = team_count + 1
        nostats = 0
        for p in roster['roster']:
            stats = nhl_api(f"people/{p['person']['id']}/stats?stats=statsSingleSeasonPlayoffs")
            stats = stats['stats'][0]['splits']
            if len(stats) == 0:
                nostats = nostats + 1
                print(f"{nostats}. NHL reports no stats for {p['person']['fullName']} - {p['position']['abbreviation']}")
                no_nhl_stats.append(p['person']['fullName'])
            else:
                if p['position']['abbreviation'] is not "G":
                    skater_stats(t['abbreviation'], p, stats)
                else:
                    goalie_stats(t['abbreviation'], p, stats)
    else:
        print(f"\n# {team_count} {t['name']} did not qualify, skipping...")
        team_count = team_count + 1



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
        'K_TOTAL',
        'GP',
        'ACTIVE'
        ]
    )
# write the players into the stats_csv_name by iterating through the khl_player_dict + writing their stats from player_dict
    not_found = 0
    for player in khl_player_dict.values():
        pn = player['Name']
        pkt = player['KHL_Team']
        pnt = player['NHL_Team']
        if pn in player_dict:
            player['KHL_Points'] = player_dict[pn]['K_TOT']
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
                player_dict[pn]['K_TOT'],
                player_dict[pn]['GP'],
                player_dict[pn]['ACTIVE'],
                ])
        elif pn in 'Name':
            pass
            print(f"")  # this is my lazy way of dealing with the name column in the roster csv
        elif pn in no_nhl_stats:
            pass
            # if no player stats are found zero them out and print it out
            print(f"WARNING {pn} ({pnt}) on {pkt} has no NHL stats, stats will be zero in the spreadsheet")
            not_found = not_found + 1
            csvwriter.writerow([
                pn,
                pkt,
                pnt,
                'NOSTAT', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'INACTIVE'
                ])
        else:
            pass
            # if no player stats are found zero them out and print it out
            print(f"WARNING {pn} ({pnt}) on {pkt} can't be found ANYWHERE!! stats will be zero")
            not_found = not_found + 1
            csvwriter.writerow([
                pn,
                pkt,
                pnt,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'INACTIVE'
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
print(f"\njson dump of the stats collected can be found in {player_dict_json}")
json = json.dumps(player_dict)
f = open(player_dict_json,"w")
f.write(json)
f.close()

x = input("Press any key to exit")
