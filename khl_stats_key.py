khl_stats = [
    {
    'name': 'Goals',
    'display_name': 'G',
    'khl_points': '6'
    },
    {
    'name': 'Assists',
    'display_name': 'A',
    'khl_points': '4'
    },
    {
    'name': 'Powerplay Points',
    'display_name': 'PPP',
    'khl_points': '2'
    },
    # since there is no PPP in spreadsheet, will inflate PPG by 2 and count PPA as 2
    {
    'name': 'Powerplay Goal',
    'display_name': 'PPG',
    'khl_points': '4'
    },
    {
    'name': 'Shorthanded Goals',
    'display_name': 'SHG',
    'khl_points': '3'
    },
    {
    'name': 'Powerplay Assist',
    'display_name': 'PPA',
    'khl_points': '2'
    },
    {
    'name': 'Shorthanded Assists',
    'display_name': 'SHA',
    'khl_points': '2'
    },
    {
    'name': 'Game-Winning Goals',
    'display_name': 'GWG',
    'khl_points': '1'
    },
    {
    'name': 'Shots on Goal',
    'display_name': 'SOG',
    'khl_points': '0.9'
    },
    {
    'name': 'Hits',
    'display_name': 'HIT',
    'khl_points': '1'
    },
    {
    'name': 'Blocks',
    'display_name': 'BLK',
    'khl_points': '1'
    },
    {
    'name': 'Wins',
    'display_name': 'WIN',
    'khl_points': '5'
    },
    {
    'name': 'Goals Against',
    'display_name': 'GA',
    'khl_points': '-3'
    },
    {
    'name': 'Saves',
    'display_name': 'SV',
    'khl_points': '0.6'
    },
    {
    'name': 'Shutouts',
    'display_name': 'SHO',
    'khl_points': '6'
    }
]

def khl_value(name):
    stat_name = name
    for s in khl_stats:
        if stat_name in s['display_name']:
            return s['khl_points']

