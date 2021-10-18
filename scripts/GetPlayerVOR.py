import sys

try:
    import requests
except ImportError:
    sys.exit('requests was not properly installed. Try again. Are you sure you are in a venv?')

#Select which scoring format: 'standard', 'half_ppr', or 'ppr'
scoring_format = 'half_ppr'

def get_fantasy_points(player, pos):
    if player.get('position') == pos:
        return player.get('fantasy_points').get(scoring_format)

pos = 'WR'
year = '2019'
week = 1 #Enter 'all' to get whole year

res = requests.get(f'https://www.fantasyfootballdatapros.com/api/players/{year}/{week}')

if res.ok:
    print('Season {0}, week {1} VOR for {2}s'.format(year, week, pos))
    print('-'*40)

    data = res.json()

    player_fantasy_points = [get_fantasy_points(player, pos) for player in data]

    player_fantasy_points = list(filter(lambda x: x is not None, player_fantasy_points))

    mean = lambda x: sum(x)/len(x)

    replacement_value = mean(player_fantasy_points)

    for player in data:
        if player.get('position') == pos:
            vor = player.get('fantasy_points').get(scoring_format) - replacement_value
            print(
                player.get('player_name'), 'had a VOR of', vor
            )