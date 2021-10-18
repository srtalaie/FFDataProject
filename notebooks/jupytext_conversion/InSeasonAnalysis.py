# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os
import sys
src_dir = os.path.join(os.getcwd(), '..', 'src')
sys.path.append(src_dir)

from utils import GLOBAL, functions


# %%
import pandas as pd
import nflfastpy as nfl
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from IPython.display import HTML


# %%
year = 2020

pbp_df = nfl.load_pbp_data(year=year)


# %%
# Help find relevant stat column based on search term

def search_columns(search_term):
    for column in pbp_df.columns:
        if search_term in column:
            print(column)

# %% [markdown]
# # Player profiles/team logos
# %% [markdown]
# TODO when ben decides to fix his shit
# %% [markdown]
# Player headshots and team logos
# %% [markdown]
# # Receiving Analysis
# %% [markdown]
# Visualizing Air Yards

# %%
pass_df = pbp_df.loc[pbp_df['pass_attempt'] == 1, ['receiver_player_id', 'receiver_player_name', 'posteam', 'air_yards']]


# %%
pass_df = pass_df.dropna()


# %%
pass_df.groupby(['receiver_player_id', 'receiver_player_name', 'posteam'], as_index=False)['air_yards'].sum().sort_values(by='air_yards', ascending=False).head(25).reset_index(drop=True)


# %%
top_n_air_yards = pass_df.groupby(['receiver_player_id'], as_index=False)['air_yards'].sum().sort_values(by='air_yards', ascending=False).head(10)['receiver_player_id']

top_n_air_yards


# %%
pass_df = pass_df.loc[pass_df['receiver_player_id'].isin(top_n_air_yards)]

pass_df.head()


# %%
fig, ax = plt.subplots(figsize=(10, 7))

ax.grid(True)

for receiver in pass_df['receiver_player_id'].unique():
    player_df = pass_df.loc[pass_df['receiver_player_id'] == receiver]
    air_yards_array = player_df['air_yards'].values
    sns.kdeplot(air_yards_array, ax=ax, label=player_df['receiver_player_name'].values[0])

ax.legend();

# %% [markdown]
# Target Shares per Receiver

# %%
target_df = pbp_df.groupby(['game_id', 'receiver_player_id', 'receiver_player_name', 'posteam'], as_index=False)['pass_attempt'].sum().sort_values(by='pass_attempt', ascending=False)


# %%
target_df.loc[target_df['receiver_player_id'].notnull()].groupby(['game_id', 'posteam'], as_index=False)['pass_attempt'].sum()


# %%
target_share_df = target_df.groupby(['game_id', 'receiver_player_id', 'receiver_player_name', 'posteam'], as_index=False)['pass_attempt'].sum().merge(
    target_df.loc[target_df['receiver_player_id'].notnull(), ['game_id', 'posteam', 'pass_attempt']].groupby(['game_id', 'posteam'], as_index=False).sum(), on=['game_id', 'posteam'], suffixes=('_player', '_team')
)


# %%
target_share_df['target_share'] = (target_share_df['pass_attempt_player'] / target_share_df['pass_attempt_team']) * 100


# %%
target_share_df = target_share_df.groupby(['receiver_player_id', 'receiver_player_name', 'posteam'], as_index=False)[['target_share', 'pass_attempt_player']].mean().sort_values(by='target_share', ascending=False)


# %%
target_share_df.head()

# %% [markdown]
# Endzone Targets

# %%
endzone_targets_df = pbp_df.loc[pbp_df['pass_attempt'] == 1, ['yardline_100', 'air_yards', 'pass_touchdown', 'receiver_player_id', 'receiver_player_name', 'posteam']].assign(pass_loc=lambda x: x.yardline_100 - x.air_yards) 

endzone_targets_df.sort_values(by='pass_loc').head(10)


# %%
endzone_targets_df = endzone_targets_df.dropna()


# %%
endzone_targets_df['endzone_target'] = endzone_targets_df['pass_loc'].apply(lambda x: x==0)


# %%
endzone_targets_df = endzone_targets_df.groupby(['receiver_player_id', 'receiver_player_name'], as_index=False)[['endzone_target', 'pass_touchdown']].sum().sort_values(by='endzone_target', ascending=False)


# %%
sns.regplot(x=endzone_targets_df['endzone_target'], y=endzone_targets_df['pass_touchdown']);

# %% [markdown]
# # Rushing Analysis
# %% [markdown]
# Visualizing Carries

# %%
rush_df = pbp_df[['rusher_player_id', 'rusher_player_name', 'yardline_100', 'rush_attempt']]

rush_df = rush_df[rush_df['rush_attempt'] == 1]


# %%
player_ids = rush_df['rusher_player_id'].unique()

rush_player_df = {
    'rusher_player_id': [],
    '1 - 10 yardline': [],
    '11 - 20 yardline': [],
    '21 - 30 yardline': [],
    '31 - 40 yardline': [],
    '41 - 60 yardline': [],
    '61 - 80 yardline': [],
    '81 - 100 yardline': []
}

for player_id in player_ids:
    player_df = rush_df.loc[rush_df['rusher_player_id'] == player_id]

    rushes = player_df['yardline_100'].tolist()

    if len(rushes) < 10:
        continue

    rush_player_df['rusher_player_id'].append(player_id)

    levels = {
        '1 - 10 yardline': (-1, 11),
        '11 - 20 yardline': (10, 21),
        '21 - 30 yardline': (20, 31),
        '31 - 40 yardline': (30, 41),
        '41 - 60 yardline': (40, 61),
        '61 - 80 yardline': (60, 81),
        '81 - 100 yardline': (80, 100)
    }

    for level, (min, max) in levels.items():
        num_level_touches = len(list(filter(lambda x: x> min and x < max, rushes)))

        rush_player_df[level].append(num_level_touches / len(rushes))

carries_dist = pd.DataFrame(rush_player_df)

carries_dist.head()


# %%
player_id_table = rush_df.loc[rush_df['rush_attempt'] == 1, ['rusher_player_id', 'rusher_player_name']].groupby(['rusher_player_id'], as_index=False).first()

player_id_table.head()


# %%
carries_dist = carries_dist.merge(player_id_table, on='rusher_player_id')

carries_dist.head()


# %%
notable_players = pbp_df.loc[pbp_df['rush_attempt'] == 1, ['rusher_player_id', 'rusher_player_name', 'rush_touchdown']]

notable_players = notable_players.groupby(['rusher_player_id', 'rusher_player_name'], as_index=False)['rush_touchdown'].sum()

notable_players = notable_players.sort_values(by='rush_touchdown', ascending=False).head(30)

notable_players = notable_players[['rusher_player_id', 'rusher_player_name']]

notable_players


# %%
carries_dist_copy = carries_dist.copy()

carries_dist_copy = carries_dist_copy.loc[carries_dist_copy['rusher_player_id'].isin(notable_players['rusher_player_id'])]

carries_dist_copy = carries_dist_copy.set_index('rusher_player_name')

carries_dist_copy = carries_dist_copy.sort_values(by='1 - 10 yardline')

ax= carries_dist_copy.plot.barh(stacked=True, colormap='tab20c')

fig = plt.gcf()

fig.set_size_inches(15, 10)

ax.legend(loc=1)

ax.set_title('Where rushers are getting their carries');

# %% [markdown]
# # Passing Analysis
# %% [markdown]
# EPA per Dropback

# %%
search_columns('epa')


# %%
epa_df = pbp_df.loc[pbp_df['pass_attempt'] == 1, ['passer_player_id', 'passer_player_name', 'pass_attempt', 'qb_epa']]

epa_df = epa_df.groupby(['passer_player_id', 'passer_player_name'], as_index=False).sum()

epa_df['epa/dropback'] = epa_df['qb_epa'] / epa_df['pass_attempt']

epa_df.loc[epa_df['pass_attempt'] > 50].sort_values(by='epa/dropback', ascending=False).head(10)


# %%
search_columns('scramble')


# %%
scrambles = pbp_df.loc[pbp_df['qb_scramble'] == 1, ['rusher_player_id', 'rush_attempt', 'epa']]

scrambles = scrambles.groupby(['rusher_player_id'], as_index=False).sum()

scrambles = scrambles.rename(columns={
    'rusher_player_id': 'passer_player_id',
    'epa': 'scramble_epa',
    'rush_attempt': 'scrambles'
})

epa_df = epa_df.merge(scrambles, on='passer_player_id')

epa_df.head()


# %%
epa_df['total_dropbacks'] = epa_df['pass_attempt'] + epa_df['scrambles']

epa_df['total_epa'] = epa_df['qb_epa'] + epa_df['scramble_epa']

epa_df['true_epa/dropback'] = epa_df['total_epa'] / epa_df['total_dropbacks']


# %%
epa_df = epa_df.loc[epa_df['pass_attempt'] > 50, ['passer_player_name', 'true_epa/dropback']].sort_values(by='true_epa/dropback').reset_index(drop=True)


# %%
plt.style.use('seaborn-darkgrid')

ax = epa_df.set_index('passer_player_name').plot.barh()

fig = plt.gcf(); fig.set_size_inches(15, 10)


