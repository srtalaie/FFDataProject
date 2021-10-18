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
from sklearn.linear_model import LinearRegression
import nflfastpy as nfl
from sklearn.metrics import mean_absolute_error


# %%
SNAPCOUNT_URL = 'https://raw.githubusercontent.com/fantasydatapros/data/master/snapcounts/{year}.csv'
YEARLY_STATS_URL = 'https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/{year}.csv'
ROSTER_URL = 'https://raw.githubusercontent.com/nflverse/nflfastR-roster/master/data/seasons/roster_{year}.csv'
#this is as far back as snapcount data goes
YEAR_START = 2013
YEAR_END = 2020

pd.set_option('display.max_columns', 100)


# %%
#snapcount data
snapcount_data = pd.DataFrame()
for year in range(YEAR_START, YEAR_END+1):
  yearly_snapcount_data = pd.read_csv(SNAPCOUNT_URL.format(year=year))
  yearly_snapcount_data['Season'] = year
  column_names = yearly_snapcount_data.columns.tolist()
  column_names.pop()
  column_names.insert(0, 'Season')
  yearly_snapcount_data = yearly_snapcount_data[column_names]
  snapcount_data = pd.concat([snapcount_data, yearly_snapcount_data])

# snapcount_data = snapcount_data.loc[snapcount_data['Pos'] == 'WR']
snapcount_data.iloc[0, :]


# %%
#yearly stats
yearly_data_df = pd.DataFrame()
for year in range (YEAR_START, YEAR_END+1):
  yearly_data = pd.read_csv(YEARLY_STATS_URL.format(year=year))
  yearly_data['Season'] = year
  column_names = yearly_data.columns.tolist()
  column_names.pop()
  column_names.insert(0, 'Season')
  yearly_data = yearly_data[column_names]
  yearly_data_df = pd.concat([yearly_data_df, yearly_data])

yearly_data_df = yearly_data_df.drop('Unnamed: 0', axis=1)
# yearly_data_df = yearly_data_df.loc[yearly_data_df['Pos'] == 'WR']
yearly_data_df.iloc[0, :]


# %%
#roster data
#yearly stats
roster_data_df = pd.DataFrame()
for year in range (YEAR_START, YEAR_END+1):
  roster_data = pd.read_csv(ROSTER_URL.format(year=year), index_col=0)
  roster_data['Season'] = year
  column_names = roster_data.columns.tolist()
  column_names.pop(); column_names.insert(0, 'Season')
  roster_data = roster_data[column_names]
  roster_data_df = pd.concat([roster_data_df, roster_data])

roster_data_df.iloc[0, :]


# %%
#air yards: new feature!
pbp_data_df = pd.DataFrame()
for year in range(YEAR_START, YEAR_END+1):
  yearly_pbp_df = nfl.load_pbp_data(year)
  #grouping by player id
  yearly_pbp_df = yearly_pbp_df.loc[yearly_pbp_df['pass_attempt'] == 1]
  yearly_pbp_df = yearly_pbp_df.groupby('receiver_id', as_index=False)['air_yards'].sum()
  yearly_pbp_df['Season'] = year
  column_names = yearly_pbp_df.columns.tolist()
  column_names.pop(); column_names.insert(0, 'Season')
  yearly_pbp_df = yearly_pbp_df[column_names]
  pbp_data_df = pd.concat([yearly_pbp_df, pbp_data_df])

pbp_data_df.head()


# %%
#Positiona cleaning
roster_data_df = roster_data_df.replace({
    'Pos': {
        'HB': 'RB',
        'WR/RS': 'WR',
        'WR/PR': 'WR',
        'FB/TE': 'TE',
        'FB/HB': 'RB'
    }
})


# %%
#merging all of this data together
#first ensuring that we don't have duplicate names at the wr position at any season
def remove_suffix(full_name):
  return ' '.join(full_name.split()[0:2])

roster_data_wrs = roster_data_df.loc[roster_data_df['position'] == 'WR', ['Season', 'full_name', 'gsis_id']]

roster_data_rbs = roster_data_df.loc[roster_data_df['position'] == 'RB', ['Season', 'full_name', 'gsis_id']]

roster_data_tes = roster_data_df.loc[roster_data_df['position'] == 'TE', ['Season', 'full_name', 'gsis_id']]

roster_data_qbs = roster_data_df.loc[roster_data_df['position'] == 'QB', ['Season', 'full_name', 'gsis_id']]


# %%
#removing suffixes in names
roster_data_wrs['full_name'] = roster_data_wrs['full_name'].apply(remove_suffix)
counted_results = roster_data_wrs.groupby(['full_name', 'Season']).size()
counted_results[counted_results > 1]

roster_data_rbs['full_name'] = roster_data_rbs['full_name'].apply(remove_suffix)
counted_results = roster_data_rbs.groupby(['full_name', 'Season']).size()
counted_results[counted_results > 1]

roster_data_tes['full_name'] = roster_data_tes['full_name'].apply(remove_suffix)
counted_results = roster_data_tes.groupby(['full_name', 'Season']).size()
counted_results[counted_results > 1]

roster_data_qbs['full_name'] = roster_data_qbs['full_name'].apply(remove_suffix)
counted_results = roster_data_qbs.groupby(['full_name', 'Season']).size()
counted_results[counted_results > 1]


# %%
#removing suffixes from all data sets (note that our air yard df has no player name, and will be merged after these two data sets are merged with roster data)
snapcount_data['Name'] = snapcount_data['Name'].apply(remove_suffix)
yearly_data_df['Player'] = yearly_data_df['Player'].apply(remove_suffix)


# %%
#renaming player name columns for consistency
snapcount_data = snapcount_data.rename({
    'Name': 'Player'
}, axis=1)

roster_data_wrs = roster_data_wrs.rename({
    'full_name': 'Player'
}, axis=1)

roster_data_rbs = roster_data_rbs.rename({
    'full_name': 'Player'
}, axis=1)

roster_data_tes = roster_data_tes.rename({
    'full_name': 'Player'
}, axis=1)

roster_data_qbs = roster_data_qbs.rename({
    'full_name': 'Player'
}, axis=1)


# %%
snapcount_data['Player'] = snapcount_data['Player'].str.lower()
yearly_data_df['Player'] = yearly_data_df['Player'].str.lower()

roster_data_wrs['Player'] = roster_data_wrs['Player'].str.lower()

roster_data_rbs['Player'] = roster_data_rbs['Player'].str.lower()

roster_data_tes['Player'] = roster_data_tes['Player'].str.lower()

roster_data_qbs['Player'] = roster_data_qbs['Player'].str.lower()


# %%
snapcount_data['Player'] = snapcount_data['Player'].str.replace('.', '')
yearly_data_df['Player'] = yearly_data_df['Player'].str.replace('.', '')

roster_data_wrs['Player'] = roster_data_wrs['Player'].str.replace('.', '')

roster_data_rbs['Player'] = roster_data_rbs['Player'].str.replace('.', '')

roster_data_tes['Player'] = roster_data_tes['Player'].str.replace('.', '')

roster_data_qbs['Player'] = roster_data_qbs['Player'].str.replace('.', '')


# %%
#duplicate columns
list(set(snapcount_data.columns.tolist()) & set(yearly_data_df.columns.tolist()))


# %%
WR_snapcount_data = snapcount_data[snapcount_data['Pos'] == 'WR']
WR_yearly_data_df = yearly_data_df[yearly_data_df['Pos'] == 'WR']

RB_snapcount_data = snapcount_data[snapcount_data['Pos'] == 'RB']
RB_yearly_data_df = yearly_data_df[yearly_data_df['Pos'] == 'RB']

TE_snapcount_data = snapcount_data[snapcount_data['Pos'] == 'TE']
TE_yearly_data_df = yearly_data_df[yearly_data_df['Pos'] == 'TE']

QB_snapcount_data = snapcount_data[snapcount_data['Pos'] == 'QB']
QB_yearly_data_df = yearly_data_df[yearly_data_df['Pos'] == 'QB']


# %%
#dropping duplicate and redundant columns
WR_snapcount_data = WR_snapcount_data.drop(['G', 'Pos'], axis=1)
WR_yearly_data_df = WR_yearly_data_df.drop('Pos', axis=1)

RB_snapcount_data = RB_snapcount_data.drop(['G', 'Pos'], axis=1)
RB_yearly_data_df = RB_yearly_data_df.drop('Pos', axis=1)

TE_snapcount_data = TE_snapcount_data.drop(['G', 'Pos'], axis=1)
TE_yearly_data_df = TE_yearly_data_df.drop('Pos', axis=1)

QB_snapcount_data = QB_snapcount_data.drop(['G', 'Pos'], axis=1)
QB_yearly_data_df = QB_yearly_data_df.drop('Pos', axis=1)


# %%
pbp_data_df = pbp_data_df.rename(columns={'receiver_id': 'gsis_id'})

# %% [markdown]
# WRs

# %%
WR_final_df = WR_snapcount_data.merge(
    WR_yearly_data_df, on=['Player', 'Season'], how='left'
)\
.merge(
    roster_data_wrs, on=['Player', 'Season'], how='left'
)\
.merge(
    pbp_data_df, on=['gsis_id', 'Season'], how='left'
)

WR_final_df = WR_final_df[[
  'Season', 'Team', 'Player', 'gsis_id', 'Snaps', 'TeamSnaps', 'G', 'Tgt', 'Rec', 'ReceivingYds', 'ReceivingTD', 'air_yards', 'RushingAtt', 'RushingYds', 'RushingTD', 'PassingAtt', 'PassingYds', 'PassingTD', 'Fumbles', 'Int'
]]\
.rename({
    'Season': 'season', 'Team': 'team', 'Player': 'player_name', 'Snaps': 'snaps', 'TeamSnaps': 'team_snaps', 'G': 'games_played', 'Rec': 'receptions', 'ReceivingYds': 'rec_yards',
    'ReceivingTD': 'rec_tds', 'Tgt': 'targets', 'RushingAtt': 'rush_att', 'RushingYds': 'rush_yards', 'RushingTD': 'rush_tds', 'PassingAtt': 'pass_att', 'PassingYds': 'pass_yards', 'PassingTD': 'pass_tds', 'Fumbles': 'fmb', 'Int': 'int'
}, axis=1)\
.assign(
    standard_fp = lambda x: x.rec_yards*0.1 + x.rec_tds*6 + x.rush_yards*0.1 + x.rush_tds*6 + x.pass_yards*0.04 + x.pass_tds*4 - x.fmb*2 - x.int*2
)\
.assign(
    ppr_fp = lambda x: x.standard_fp + x.receptions
)\
.assign(
    half_ppr_fp = lambda x: x.standard_fp + x.receptions*0.5
).dropna()

WR_final_df.head()


# %%
WR_final_df.to_csv('../FinalData/WR_regression_data.csv', index=False)


# %%
def WR_make_per_game_columns(column_name):
  WR_final_df[f'{column_name}_per_game'] = WR_final_df[column_name] / WR_final_df['games_played']

for column in ['air_yards', 'targets', 'snaps', 'rush_att', 'pass_att', 'standard_fp', 'half_ppr_fp', 'ppr_fp']:
  WR_make_per_game_columns(column)


# %%
WR_lag_features = ['games_played', 'air_yards_per_game', 'targets_per_game', 'snaps', 'snaps_per_game', 'rush_att_per_game', 'pass_att_per_game']
WR_final_df = WR_final_df.sort_values(by='season')

shifted = WR_final_df.groupby('gsis_id').shift(1)
for column in WR_lag_features:
    WR_final_df[f'lag_{column}_1'] = shifted[column]


# %%
WR_pred_df = WR_final_df.loc[WR_final_df['lag_games_played_1'] > 10]
WR_pred_df = WR_pred_df.loc[WR_pred_df['lag_snaps_1'] > 300]
WR_pred_df = WR_pred_df.dropna()


# %%
WR_features = ['lag_targets_per_game_1', 'lag_snaps_per_game_1', 'lag_rush_att_per_game_1', 'lag_pass_att_per_game_1']

#Change based on scoring format: 'standard_fp_per_game', 'half_ppr_fp_per_game', or 'ppr_fp_per_game
WR_target = 'half_ppr_fp_per_game'

WR_training_data = WR_pred_df.loc[WR_pred_df['season'].isin(range(2013, 2019))]
WR_training_data_X = WR_training_data[WR_features].values
WR_training_data_y = WR_training_data[WR_target].values

WR_test_data = WR_pred_df.loc[WR_pred_df['season'] == 2019]
WR_test_data_X = WR_test_data[WR_features].values
WR_test_data_y = WR_test_data[WR_target].values


# %%
WR_lm = LinearRegression().fit(WR_training_data_X, WR_training_data_y)
y_pred = WR_lm.predict(WR_test_data_X)
mean_absolute_error(y_pred, WR_test_data_y)


# %%
#2021 predictions
WR_df_PREDICTED = WR_final_df.loc[WR_final_df['season'] == 2020]
WR_df_PREDICTED = WR_df_PREDICTED.dropna()
WR_df_PREDICTED['predicted_fp_per_game'] = WR_lm.predict((WR_df_PREDICTED[WR_features].values))
WR_df_PREDICTED = WR_df_PREDICTED[['player_name', 'predicted_fp_per_game']]

with pd.option_context('display.max_rows', None):
  display(WR_df_PREDICTED.sort_values(by='predicted_fp_per_game', ascending=False).head(100))

# %% [markdown]
# RBs

# %%
RB_final_df = RB_snapcount_data.merge(
    RB_yearly_data_df, on=['Player', 'Season'], how='left'
)\
.merge(
    roster_data_rbs, on=['Player', 'Season'], how='left'
)\
.merge(
    pbp_data_df, on=['gsis_id', 'Season'], how='left'
)

RB_final_df = RB_final_df[[
  'Season', 'Team', 'Player', 'gsis_id', 'Snaps', 'TeamSnaps', 'G', 'Tgt', 'Rec', 'ReceivingYds', 'ReceivingTD', 'air_yards', 'RushingAtt', 'RushingYds', 'RushingTD', 'PassingAtt', 'PassingYds', 'PassingTD', 'Fumbles', 'Int'
]]\
.rename({
    'Season': 'season', 'Team': 'team', 'Player': 'player_name', 'Snaps': 'snaps', 'TeamSnaps': 'team_snaps', 'G': 'games_played', 'Rec': 'receptions', 'ReceivingYds': 'rec_yards',
    'ReceivingTD': 'rec_tds', 'Tgt': 'targets', 'RushingAtt': 'rush_att', 'RushingYds': 'rush_yards', 'RushingTD': 'rush_tds', 'PassingAtt': 'pass_att', 'PassingYds': 'pass_yards', 'PassingTD': 'pass_tds', 'Fumbles': 'fmb', 'Int': 'int'
}, axis=1)\
.assign(
    standard_fp = lambda x: x.rec_yards*0.1 + x.rec_tds*6 + x.rush_yards*0.1 + x.rush_tds*6 + x.pass_yards*0.04 + x.pass_tds*4 - x.fmb*2 - x.int*2
)\
.assign(
    ppr_fp = lambda x: x.standard_fp + x.receptions
)\
.assign(
    half_ppr_fp = lambda x: x.standard_fp + x.receptions*0.5
).dropna()

RB_final_df.to_csv('../FinalData/RB_regression_data.csv', index=False)

def RB_make_per_game_columns(column_name):
  RB_final_df[f'{column_name}_per_game'] = RB_final_df[column_name] / RB_final_df['games_played']

for column in ['air_yards', 'targets', 'snaps', 'rush_att', 'pass_att', 'standard_fp', 'half_ppr_fp', 'ppr_fp']:
  RB_make_per_game_columns(column)

RB_lag_features = ['games_played', 'air_yards_per_game', 'targets_per_game', 'snaps', 'snaps_per_game', 'rush_att_per_game', 'pass_att_per_game']
RB_final_df = RB_final_df.sort_values(by='season')

shifted = RB_final_df.groupby('gsis_id').shift(1)
for column in RB_lag_features:
    RB_final_df[f'lag_{column}_1'] = shifted[column]

RB_pred_df = RB_final_df.loc[RB_final_df['lag_games_played_1'] > 10]
RB_pred_df = RB_pred_df.loc[RB_pred_df['lag_snaps_1'] > 300]
RB_pred_df = RB_pred_df.dropna()

RB_features = ['lag_targets_per_game_1', 'lag_snaps_per_game_1', 'lag_rush_att_per_game_1', 'lag_pass_att_per_game_1']

#Change based on scoring format: 'standard_fp_per_game', 'half_ppr_fp_per_game', or 'ppr_fp_per_game
RB_target = 'half_ppr_fp_per_game'

RB_training_data = RB_pred_df.loc[RB_pred_df['season'].isin(range(2013, 2019))]
RB_training_data_X = RB_training_data[RB_features].values
RB_training_data_y = RB_training_data[RB_target].values

RB_test_data = RB_pred_df.loc[RB_pred_df['season'] == 2019]
RB_test_data_X = RB_test_data[RB_features].values
RB_test_data_y = RB_test_data[RB_target].values

RB_lm = LinearRegression().fit(RB_training_data_X, RB_training_data_y)
y_pred = RB_lm.predict(RB_test_data_X)
mean_absolute_error(y_pred, RB_test_data_y)

#2021 predictions
RB_df_PREDICTED = RB_final_df.loc[RB_final_df['season'] == 2020]
RB_df_PREDICTED = RB_df_PREDICTED.dropna()
RB_df_PREDICTED['predicted_fp_per_game'] = RB_lm.predict((RB_df_PREDICTED[RB_features].values))
RB_df_PREDICTED = RB_df_PREDICTED[['player_name', 'predicted_fp_per_game']]

with pd.option_context('display.max_rows', None):
  display(RB_df_PREDICTED.sort_values(by='predicted_fp_per_game', ascending=False).head(100))

# %% [markdown]
# TEs

# %%
TE_final_df = TE_snapcount_data.merge(
    TE_yearly_data_df, on=['Player', 'Season'], how='left'
)\
.merge(
    roster_data_tes, on=['Player', 'Season'], how='left'
)\
.merge(
    pbp_data_df, on=['gsis_id', 'Season'], how='left'
)

TE_final_df = TE_final_df[[
  'Season', 'Team', 'Player', 'gsis_id', 'Snaps', 'TeamSnaps', 'G', 'Tgt', 'Rec', 'ReceivingYds', 'ReceivingTD', 'air_yards', 'RushingAtt', 'RushingYds', 'RushingTD', 'PassingAtt', 'PassingYds', 'PassingTD', 'Fumbles', 'Int'
]]\
.rename({
    'Season': 'season', 'Team': 'team', 'Player': 'player_name', 'Snaps': 'snaps', 'TeamSnaps': 'team_snaps', 'G': 'games_played', 'Rec': 'receptions', 'ReceivingYds': 'rec_yards',
    'ReceivingTD': 'rec_tds', 'Tgt': 'targets', 'RushingAtt': 'rush_att', 'RushingYds': 'rush_yards', 'RushingTD': 'rush_tds', 'PassingAtt': 'pass_att', 'PassingYds': 'pass_yards', 'PassingTD': 'pass_tds', 'Fumbles': 'fmb', 'Int': 'int'
}, axis=1)\
.assign(
    standard_fp = lambda x: x.rec_yards*0.1 + x.rec_tds*6 + x.rush_yards*0.1 + x.rush_tds*6 + x.pass_yards*0.04 + x.pass_tds*4 - x.fmb*2 - x.int*2
)\
.assign(
    ppr_fp = lambda x: x.standard_fp + x.receptions
)\
.assign(
    half_ppr_fp = lambda x: x.standard_fp + x.receptions*0.5
).dropna()

TE_final_df.to_csv('../FinalData/TE_regression_data.csv', index=False)

def TE_make_per_game_columns(column_name):
  TE_final_df[f'{column_name}_per_game'] = TE_final_df[column_name] / TE_final_df['games_played']

for column in ['air_yards', 'targets', 'snaps', 'rush_att', 'pass_att', 'standard_fp', 'half_ppr_fp', 'ppr_fp']:
  TE_make_per_game_columns(column)

WR_final_df.head()

TE_lag_features = ['games_played', 'air_yards_per_game', 'targets_per_game', 'snaps', 'snaps_per_game', 'rush_att_per_game', 'pass_att_per_game']
TE_final_df = TE_final_df.sort_values(by='season')

shifted = TE_final_df.groupby('gsis_id').shift(1)
for column in TE_lag_features:
    TE_final_df[f'lag_{column}_1'] = shifted[column]

TE_pred_df = TE_final_df.loc[TE_final_df['lag_games_played_1'] > 10]
TE_pred_df = TE_pred_df.loc[TE_pred_df['lag_snaps_1'] > 300]
TE_pred_df = TE_pred_df.dropna()

TE_features = ['lag_targets_per_game_1', 'lag_snaps_per_game_1', 'lag_rush_att_per_game_1', 'lag_pass_att_per_game_1']

#Change based on scoring format: 'standard_fp_per_game', 'half_ppr_fp_per_game', or 'ppr_fp_per_game
TE_target = 'half_ppr_fp_per_game'

TE_training_data = TE_pred_df.loc[TE_pred_df['season'].isin(range(2013, 2019))]
TE_training_data_X = TE_training_data[TE_features].values
TE_training_data_y = TE_training_data[TE_target].values

TE_test_data = TE_pred_df.loc[TE_pred_df['season'] == 2019]
TE_test_data_X = TE_test_data[TE_features].values
TE_test_data_y = TE_test_data[TE_target].values

TE_lm = LinearRegression().fit(TE_training_data_X, TE_training_data_y)
y_pred = TE_lm.predict(TE_test_data_X)
mean_absolute_error(y_pred, TE_test_data_y)

#2021 predictions
TE_df_PREDICTED= TE_final_df.loc[TE_final_df['season'] == 2020]
TE_df_PREDICTED = TE_df_PREDICTED.dropna()
TE_df_PREDICTED['predicted_fp_per_game'] = TE_lm.predict((TE_df_PREDICTED[TE_features].values))
TE_df_PREDICTED = TE_df_PREDICTED[['player_name', 'predicted_fp_per_game']]

with pd.option_context('display.max_rows', None):
  display(TE_df_PREDICTED.sort_values(by='predicted_fp_per_game', ascending=False).head(100))

# %% [markdown]
# QBs

# %%
QB_final_df = QB_snapcount_data.merge(
    QB_yearly_data_df, on=['Player', 'Season'], how='left'
)\
.merge(
    roster_data_qbs, on=['Player', 'Season'], how='left'
)\
.merge(
    pbp_data_df, on=['gsis_id', 'Season'], how='left'
)

QB_final_df = QB_final_df[[
  'Season', 'Team', 'Player', 'gsis_id', 'Snaps', 'TeamSnaps', 'G', 'Tgt', 'Rec', 'ReceivingYds', 'ReceivingTD', 'air_yards', 'RushingAtt', 'RushingYds', 'RushingTD', 'PassingAtt', 'PassingYds', 'PassingTD', 'Fumbles', 'Int'
]]\
.rename({
    'Season': 'season', 'Team': 'team', 'Player': 'player_name', 'Snaps': 'snaps', 'TeamSnaps': 'team_snaps', 'G': 'games_played', 'Rec': 'receptions', 'ReceivingYds': 'rec_yards',
    'ReceivingTD': 'rec_tds', 'Tgt': 'targets', 'RushingAtt': 'rush_att', 'RushingYds': 'rush_yards', 'RushingTD': 'rush_tds', 'PassingAtt': 'pass_att', 'PassingYds': 'pass_yards', 'PassingTD': 'pass_tds', 'Fumbles': 'fmb', 'Int': 'int'
}, axis=1)\
.assign(
    standard_fp = lambda x: x.rec_yards*0.1 + x.rec_tds*6 + x.rush_yards*0.1 + x.rush_tds*6 + x.pass_yards*0.04 + x.pass_tds*4 - x.fmb*2 - x.int*2
)\
.assign(
    ppr_fp = lambda x: x.standard_fp + x.receptions
)\
.assign(
    half_ppr_fp = lambda x: x.standard_fp + x.receptions*0.5
).dropna()

QB_final_df.to_csv('../FinalData/QB_regression_data.csv', index=False)

def QB_make_per_game_columns(column_name):
  QB_final_df[f'{column_name}_per_game'] = QB_final_df[column_name] / QB_final_df['games_played']

for column in ['air_yards', 'targets', 'snaps', 'rush_att', 'pass_att', 'standard_fp', 'half_ppr_fp', 'ppr_fp']:
  QB_make_per_game_columns(column)

QB_lag_features = ['games_played', 'air_yards_per_game', 'targets_per_game', 'snaps', 'snaps_per_game', 'rush_att_per_game', 'pass_att_per_game']
QB_final_df = QB_final_df.sort_values(by='season')

shifted = QB_final_df.groupby('gsis_id').shift(1)
for column in QB_lag_features:
    QB_final_df[f'lag_{column}_1'] = shifted[column]

QB_pred_df = QB_final_df.loc[QB_final_df['lag_games_played_1'] > 10]
QB_pred_df = QB_pred_df.loc[QB_pred_df['lag_snaps_1'] > 300]
QB_pred_df = QB_pred_df.dropna()

QB_features = ['lag_targets_per_game_1', 'lag_snaps_per_game_1', 'lag_rush_att_per_game_1', 'lag_pass_att_per_game_1']

#Change based on scoring format: 'standard_fp_per_game', 'half_ppr_fp_per_game', or 'ppr_fp_per_game
QB_target = 'half_ppr_fp_per_game'

QB_training_data = QB_pred_df.loc[QB_pred_df['season'].isin(range(2013, 2019))]
QB_training_data_X = QB_training_data[QB_features].values
QB_training_data_y = QB_training_data[QB_target].values

QB_test_data = QB_pred_df.loc[QB_pred_df['season'] == 2019]
QB_test_data_X = QB_test_data[QB_features].values
QB_test_data_y = QB_test_data[QB_target].values

QB_lm = LinearRegression().fit(QB_training_data_X, QB_training_data_y)
y_pred = QB_lm.predict(QB_test_data_X)
mean_absolute_error(y_pred, QB_test_data_y)

#2021 predictions
QB_df_PREDICTED = QB_final_df.loc[QB_final_df['season'] == 2020]
QB_df_PREDICTED = QB_df_PREDICTED.dropna()
QB_df_PREDICTED['predicted_fp_per_game'] = QB_lm.predict((QB_df_PREDICTED[QB_features].values))
QB_df_PREDICTED = QB_df_PREDICTED[['player_name', 'predicted_fp_per_game']]

with pd.option_context('display.max_rows', None):
  display(QB_df_PREDICTED.sort_values(by='predicted_fp_per_game', ascending=False).head(100))


# %%
QB_snapcount_data.head()


# %%



