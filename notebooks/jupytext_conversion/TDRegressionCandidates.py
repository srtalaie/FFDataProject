# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os
import sys
src_dir = os.path.join(os.getcwd())
abs_path = os.path.abspath(os.path.join(src_dir, os.pardir, 'src'))
sys.path.append(abs_path)

from utils import GLOBAL, functions


# %%
import pandas as pd
import nflfastpy as nfl
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
sns.set_style('darkgrid')


# %%
#Change start and end for range
pbp_df = pd.DataFrame()
year_start = 2015
year_end = 2020


# %%
#Get roster based on last season, change date to last seasons
roster = nfl.load_2020_roster_data()


# %%
#Get yearly pbp data for past 5 years WARNING: Takes a long time
for year in range(year_start, year_end):
    yearly_df = nfl.load_pbp_data(year)
    pbp_df = pd.concat([pbp_df, yearly_df])


# %%
#Filter rushing data

#rush_attempt = 1 if it was a rush_attempt, same with rush_touchdown, & two_point_attempt = 0 to filter out 2pt conversions
rushing_df = pbp_df[['rush_attempt', 'rush_touchdown', 'yardline_100', 'two_point_attempt']]

rushing_df = rushing_df.loc[
    (rushing_df['two_point_attempt'] == 0) & (rushing_df['rush_attempt'] == 1)
]


# %%
#Filter receiving data

#pass_attempt = 1 if it was a rush_attempt, same with pass_touchdown, & two_point_attempt = 0 to filter out 2pt conversions
receiving_df = pbp_df[['pass_attempt', 'pass_touchdown', 'yardline_100', 'two_point_attempt']]

receiving_df = receiving_df.loc[
    (receiving_df['two_point_attempt'] == 0) & (receiving_df['pass_attempt'] == 1)
]


# %%
#Here, we are grouping by the yardline from where the play began, and then using value counts to count the number of times a rushing play was a touchdown (either a 0 or a 1), we can set the argument normalize = True to be able to calculate the proportion of plays that were touchdowns, instead of the count.

rushing_df_probs = rushing_df.groupby('yardline_100')['rush_touchdown'].value_counts(normalize=True)

rushing_df_probs = pd.DataFrame({
    'probability_of_td': rushing_df_probs.values
}, index=rushing_df_probs.index).reset_index()

#Filter out prob of not a td
rushing_df_probs = rushing_df_probs.loc[rushing_df_probs['rush_touchdown'] == 1]

rushing_df_probs = rushing_df_probs.drop('rush_touchdown', axis=1)


# %%
receiving_df_probs = receiving_df.groupby('yardline_100')['pass_touchdown'].value_counts(normalize=True)

receiving_df_probs = pd.DataFrame({
    'probability_of_td': receiving_df_probs.values
}, index=receiving_df_probs.index).reset_index()

#Filter out prob of not a td
receiving_df_probs = receiving_df_probs.loc[receiving_df_probs['pass_touchdown'] == 1]

receiving_df_probs = receiving_df_probs.drop('pass_touchdown', axis=1)


# %%
#Get PBP from the last season which is year_end variable
last_season_pbp_df = nfl.load_pbp_data(year_end)


# %%
#Filter out positions from last years rosters
#RBs
rb_df = roster.loc[roster['position'] == 'RB']['gsis_id']
#WRs
wr_df = roster.loc[roster['position'] == 'WR']['gsis_id']
#TEs
te_df = roster.loc[roster['position'] == 'TE']['gsis_id']

# %% [markdown]
# #RB TD Regression

# %%
#Get rushing data from last season pbp
last_season_RB_rushing_df = last_season_pbp_df.loc[last_season_pbp_df['rush_attempt'] == 1, ['rusher_id', 'rusher_player_name', 'posteam', 'rush_attempt', 'rush_touchdown', 'yardline_100']]

#Filter out RBs
last_season_RB_rushing_df = last_season_RB_rushing_df.loc[last_season_RB_rushing_df['rusher_id'].isin(rb_df)]

#Merge Probability df with Rushing
last_season_RB_rushing_df = last_season_RB_rushing_df.merge(rushing_df_probs, how='left', on='yardline_100')

#Calculate the actual touchdowns rb scored by aggregating all instances where the rush_touchdown == 1 & calculate aggregate of all instances where the probability of scoring a touchdown from that area of the field change names to better reflect what they represent
last_season_RB_rushing_df = last_season_RB_rushing_df.groupby('rusher_id', as_index=False).agg({
    'rusher_player_name': 'first',
    'rush_touchdown': np.sum,
    'probability_of_td': np.sum
}).rename({
    'probability_of_td': 'expected_touchdowns',
    'rush_touchdown': 'actual_touchdowns'
}, axis=1)

#Determine if positive regression candidate by comparing actual scored touchdowns vs expected touchdowns
last_season_RB_rushing_df['positive_regression_candidate'] = last_season_RB_rushing_df['actual_touchdowns'] < last_season_RB_rushing_df['expected_touchdowns']

#Get delta between expected vs actual tds
last_season_RB_rushing_df['delta'] = last_season_RB_rushing_df.apply(
    lambda x: abs(x.expected_touchdowns - x.actual_touchdowns), axis=1
)

last_season_RB_rushing_df = last_season_RB_rushing_df.sort_values(by='expected_touchdowns', ascending=False)

# %% [markdown]
# #WR TD Regression

# %%
#Get receiving data from last season pbp
last_season_WR_receiving_df = last_season_pbp_df.loc[last_season_pbp_df['pass_attempt'] == 1, ['receiver_id', 'receiver_player_name', 'posteam', 'pass_attempt', 'pass_touchdown', 'yardline_100']]

#Filter out WRs
last_season_WR_receiving_df = last_season_WR_receiving_df.loc[last_season_WR_receiving_df['receiver_id'].isin(wr_df)]

#Merge Probability df with receiving
last_season_WR_receiving_df = last_season_WR_receiving_df.merge(receiving_df_probs, how='left', on='yardline_100')

#Calculate the actual touchdowns rb scored by aggregating all instances where the rush_touchdown == 1 & calculate aggregate of all instances where the probability of scoring a touchdown from that area of the field change names to better reflect what they represent
last_season_WR_receiving_df = last_season_WR_receiving_df.groupby('receiver_id', as_index=False).agg({
    'receiver_player_name': 'first',
    'pass_touchdown': np.sum,
    'probability_of_td': np.sum
}).rename({
    'probability_of_td': 'expected_touchdowns',
    'pass_touchdown': 'actual_touchdowns'
}, axis=1)

#Determine if positive regression candidate by comparing actual scored touchdowns vs expected touchdowns
last_season_WR_receiving_df['positive_regression_candidate'] = last_season_WR_receiving_df['actual_touchdowns'] < last_season_WR_receiving_df['expected_touchdowns']

#Get delta between expected vs actual tds
last_season_WR_receiving_df['delta'] = last_season_WR_receiving_df.apply(
    lambda x: abs(x.expected_touchdowns - x.actual_touchdowns), axis=1
)

last_season_WR_receiving_df = last_season_WR_receiving_df.sort_values(by='expected_touchdowns', ascending=False)

# %% [markdown]
# #TE TD Regression

# %%
#Get receiving data from last season pbp
last_season_TE_receiving_df = last_season_pbp_df.loc[last_season_pbp_df['pass_attempt'] == 1, ['receiver_id', 'receiver_player_name', 'posteam', 'pass_attempt', 'pass_touchdown', 'yardline_100']]

#Filter out WRs
last_season_TE_receiving_df = last_season_TE_receiving_df.loc[last_season_TE_receiving_df['receiver_id'].isin(te_df)]

#Merge Probability df with receiving
last_season_TE_receiving_df = last_season_TE_receiving_df.merge(receiving_df_probs, how='left', on='yardline_100')

#Calculate the actual touchdowns rb scored by aggregating all instances where the rush_touchdown == 1 & calculate aggregate of all instances where the probability of scoring a touchdown from that area of the field change names to better reflect what they represent
last_season_TE_receiving_df = last_season_TE_receiving_df.groupby('receiver_id', as_index=False).agg({
    'receiver_player_name': 'first',
    'pass_touchdown': np.sum,
    'probability_of_td': np.sum
}).rename({
    'probability_of_td': 'expected_touchdowns',
    'pass_touchdown': 'actual_touchdowns'
}, axis=1)

#Determine if positive regression candidate by comparing actual scored touchdowns vs expected touchdowns
last_season_TE_receiving_df['positive_regression_candidate'] = last_season_TE_receiving_df['actual_touchdowns'] < last_season_TE_receiving_df['expected_touchdowns']

#Get delta between expected vs actual tds
last_season_TE_receiving_df['delta'] = last_season_TE_receiving_df.apply(
    lambda x: abs(x.expected_touchdowns - x.actual_touchdowns), axis=1
)

last_season_TE_receiving_df = last_season_TE_receiving_df.sort_values(by='expected_touchdowns', ascending=False)


# %%



