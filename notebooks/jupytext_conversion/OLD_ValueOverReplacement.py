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
proj_df = pd.read_csv(GLOBAL.PROJECTIONS_2020, index_col=0)


# %%
### DO NOT RUN IF USING 2021 PROJECTIONS OR HIGHER ####
### Section is for older projections newer ones have the scoring columns ###

#Get rid of odd column if there are any[row indexer, column indexer], change 0 to 1 if there are
proj_df = proj_df.iloc[:, 0:]

#Add in Fantasy Points based on scoring type
proj_df['FantasyPoints'] = (
    functions.scoringCalculator(
        proj_df['Receptions'], proj_df['ReceivingYds'], proj_df['ReceivingTD'], proj_df['FL'], proj_df['RushingYds'], proj_df['RushingTD'], proj_df['PassingYds'], proj_df['PassingTD'], proj_df['Int'], GLOBAL.PPR_SCORING
    )
)


# %%
columns = ['Player', 'Team', 'Pos', 'FantasyPoints', 'Receptions', 'ReceivingYds', 'ReceivingTD', 'RushingAtt', 'RushingYds', 'RushingTD', 'FL']

#Get dataframes of specific pos
rb_proj_df = proj_df.loc[(proj_df['Pos'] == 'RB', columns)]
wr_proj_df = proj_df.loc[(proj_df['Pos'] == 'WR', columns)]
te_proj_df = proj_df.loc[(proj_df['Pos'] == 'TE', columns)]
qb_proj_df = proj_df.loc[(proj_df['Pos'] == 'QB', columns)]


# %%
#ADP for current year and scoring format
adp_df = pd.read_csv(GLOBAL.ADP_2020_PPR, index_col=0)

adp_df['ADP RANK'] = adp_df['AVG'].rank()

adp_df_cutoff = adp_df[:100]


replacement_players = {
    'RB': '',
    'WR': '',
    'TE': '',
    'QB': ''
}

for _, row in adp_df_cutoff.iterrows():
    
    position = row['POS'] # extract out the position and player value from each row as we loop through it
    player = row['PLAYER']
    
    if position in replacement_players: # if the position is in the dict's keys
        replacement_players[position] = player # set that player as the replacement player

vor_df = proj_df[['Player', 'Pos', 'Team', 'FantasyPoints']]


# %%
replacement_values = {} # initialize an empty dictionary

for position, player_name in replacement_players.items():
    
    player = proj_df.loc[proj_df['Player'] == player_name]
    
    # because this is a series object we get back, we need to use the tolist method
    # to get back the series as a list. The list object is of length 1, and the 1 item has the value we need.
    # we tack on a [0] to get the value we need.
    
    replacement_values[position] = player['FantasyPoints'].tolist()[0]


# %%
pd.set_option('chained_assignment', None)

vor_df = vor_df.loc[vor_df['Pos'].isin(['QB', 'RB', 'WR', 'TE'])]

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html
vor_df['VOR'] = vor_df.apply(
    lambda row: row['FantasyPoints'] - replacement_values.get(row['Pos']), axis=1
)


# %%
pd.set_option('display.max_rows', None) # turn off truncation of rows setting inherent to pandas

vor_df['VOR Rank'] = vor_df['VOR'].rank(ascending=False)
vor_df.sort_values(by='VOR', ascending=False).head(100)


# %%
vor_df.groupby('Pos')['VOR'].describe()


# %%
vor_df['VOR'] = vor_df['VOR'].apply(lambda x: (x - vor_df['VOR'].min()) / (vor_df['VOR'].max() - vor_df['VOR'].min()))


# %%
vor_df = vor_df.sort_values(by='VOR Rank')
vor_df.head(100)


# %%
import seaborn as sns # in case you did not import it above

# calculating how many players are in our draft pool.
num_teams = 12
num_spots = 16 # 1 QB, 2RB, 2WR, 1TE, 1FLEX, 1K, 1DST, 7 BENCH
draft_pool = num_teams * num_spots

df_copy =vor_df[:draft_pool]

sns.boxplot(x=df_copy['Pos'], y=df_copy['VOR']);


# %%
vor_df = vor_df.rename({
    'VOR': 'Value',
    'VOR Rank': 'Value Rank'
}, axis=1) # axis = 1 means make the change along the column axis.


# %%
adp_df = adp_df.rename({
    'PLAYER': 'Player',
    'POS': 'Pos',
    'AVG': 'Average ADP',
    'ADP RANK': 'ADP Rank'
}, axis=1) # let's rename some columns first.


# %%
final_df = vor_df.merge(adp_df, how='left', on=['Player', 'Pos'])

final_df.head()


# %%
final_df['Diff in ADP and Value'] = final_df['ADP Rank'] - final_df['Value Rank']
final_df.head()


# %%
draft_pool = final_df.sort_values(by='ADP Rank')[:196]

rb_draft_pool = draft_pool.loc[draft_pool['Pos'] == 'RB']
qb_draft_pool = draft_pool.loc[draft_pool['Pos'] == 'QB']
wr_draft_pool = draft_pool.loc[draft_pool['Pos'] == 'WR']
te_draft_pool = draft_pool.loc[draft_pool['Pos'] == 'TE']


# %%
# top 10 RB sleepers for this year's draft
rb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]


# %%
# top 10 RB overvalued for this year's draft
rb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]


# %%
# top 10 WR sleepers for this year's draft
wr_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]


# %%
# top 10 WR overvalued for this year's draft
wr_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]


# %%
# top 10 TE sleepers for this year's draft
te_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]


# %%
# top 10 TE overvalued for this year's draft
te_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]


# %%
# top 10 QB sleepers for this year's draft
qb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]


# %%
# top 10 QB overvalued for this year's draft
qb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]


