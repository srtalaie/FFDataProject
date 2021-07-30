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


# %%
#Projections for current year
proj_df = pd.read_csv(GLOBAL.PROJECTIONS_2021, index_col=0)

#ADP for current year and scoring format
adp_df = pd.read_csv(GLOBAL.ADP_2021_HALF_PPR, index_col=0)

#Either Standard, Half PPR, or PPR
FANTASY_SCORING_FORMAT = 'Half PPR'

#VOR dataframe based on scoring format
vor_df = proj_df[['Player', 'Pos', 'Tm', FANTASY_SCORING_FORMAT]]

vor_df = vor_df.rename(columns={
    FANTASY_SCORING_FORMAT: 'Projected Fantasy Total'
})


# %%
#Get dataframes of specific pos
rb_proj_df = proj_df[proj_df['Pos'] == 'RB']
wr_proj_df = proj_df[proj_df['Pos'] == 'WR']
te_proj_df = proj_df[proj_df['Pos'] == 'TE']
qb_proj_df = proj_df[proj_df['Pos'] == 'QB']


# %%
adp_df['ADP RANK'] = adp_df['AVG'].rank()

adp_df_cutoff = adp_df[:100]

replacement_players = {
    'RB': '',
    'WR': '',
    'TE': '',
    'QB': ''
}


# %%
for _, row in adp_df_cutoff.iterrows():
    position = row['POS'][:2]
    player = row['Player']

    if position in replacement_players:
        replacement_players[position] = player


# %%
replacement_values = {}

for position, player_name in replacement_players.items():
    player = vor_df.loc[vor_df['Player'] == player_name]
    replacement_values[position] = player['Projected Fantasy Total'].tolist()[0]


# %%
pd.set_option('chained_assignment', None)
pd.set_option('display.max_rows', None)

vor_df = vor_df.loc[vor_df['Pos'].isin(['QB', 'RB', 'WR', 'TE'])]

vor_df['VOR'] = vor_df.apply(
    lambda row: row['Projected Fantasy Total'] - replacement_values.get(row['Pos']), axis=1
)


# %%
vor_df['VOR Rank'] = vor_df['VOR'].rank(ascending=False)
# vor_df.sort_values(by='VOR Rank')


# %%
min_vor = vor_df['VOR'].min()
max_vor = vor_df['VOR'].max()
vor_range = max_vor - min_vor

vor_df['VOR'] = vor_df['VOR'].apply(
    lambda x: (x - min_vor) / vor_range
)


# %%
vor_df = vor_df.sort_values(by= 'VOR', ascending=False)


# %%
vor_df = vor_df.rename({
    'VOR': 'Value',
    'VOR Rank': 'Value Rank',
    'Tm': 'Team'
}, axis=1)


# %%
adp_df = adp_df[['Player', 'POS', 'Bye', 'AVG', 'ADP RANK']]

adp_df = adp_df.rename(columns={
    'POS': 'Pos Rank',
    'AVG': 'Average ADP',
    'ADP RANK': 'ADP Rank'
})


# %%
adp_df['Pos'] = adp_df.apply(
    lambda row: str(row['Pos Rank'])[:2]
, axis=1)

adp_df.head()


# %%
final_df = vor_df.merge(adp_df, how='left', on=['Player', 'Pos'])


# %%
final_df['Diff in ADP and Value'] = final_df['ADP Rank'] - final_df['Value Rank']
final_df = final_df.dropna()


# %%
# Number of Teams * Spots on Each Team
draft_pool = final_df.sort_values(by='ADP Rank')[:196]


# %%
rb_df_draft_pool = draft_pool.loc[draft_pool['Pos'] == 'RB']
wr_df_draft_pool = draft_pool.loc[draft_pool['Pos'] == 'WR']
te_df_draft_pool = draft_pool.loc[draft_pool['Pos'] == 'TE']
qb_df_draft_pool = draft_pool.loc[draft_pool['Pos'] == 'QB']

# %% [markdown]
# #Sleepers and Over Valued by Pos.
# %% [markdown]
# RBs
# %% [markdown]
# Sleepers

# %%
rb_df_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False).head(10)

# %% [markdown]
# Over Valued

# %%
rb_df_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True).head(10)

# %% [markdown]
# WRs
# %% [markdown]
# Sleepers

# %%
wr_df_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False).head(10)

# %% [markdown]
# Over Valued

# %%
wr_df_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True).head(10)

# %% [markdown]
# TEs
# %% [markdown]
# Sleepers

# %%
te_df_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False).head(10)

# %% [markdown]
# Over Valued

# %%
te_df_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True).head(10)

# %% [markdown]
# QBs
# %% [markdown]
# Sleepers

# %%
qb_df_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False).head(10)

# %% [markdown]
# Over Valued

# %%
qb_df_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True).head(10)


# %%
final_df = final_df[['Player', 'Pos Rank', 'Team', 'Bye', 'Value', 'Value Rank', 'Average ADP', 'ADP Rank', 'Diff in ADP and Value', 'Projected Fantasy Total']]


# %%
final_df.to_csv(r'../FinalData/ValueOverReplacement.csv', encoding='utf-8', index=False);


