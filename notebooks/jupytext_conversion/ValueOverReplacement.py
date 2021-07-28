# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: 'Python 3.7.10 64-bit (''FFDataProject'': conda)'
#     name: python3
# ---

# +
import os
import sys
src_dir = os.path.join(os.getcwd(), '..', 'src')
sys.path.append(src_dir)

from utils import GLOBAL, functions
# -

import pandas as pd

proj_df = pd.read_csv(GLOBAL.PROJECTIONS_2021, index_col=0)

# +
### DO NOT RUN IF USING 2021 PROJECTIONS OR HIGHER ####
### Section is for older projections newer ones have the scoring columns ###

#Get rid of odd column if there are any[row indexer, column indexer], change 0 to 1 if there are
proj_df = proj_df.iloc[:, 0:]

#Add in Fantasy Points based on scoring type
proj_df['FantasyPoints'] = (
    functions.scoringCalculator(
        proj_df['Receptions'], proj_df['ReceivingYds'], proj_df['ReceivingTD'], proj_df['FL'], proj_df['RushingYds'], proj_df['RushingTD'], proj_df['PassingYds'], proj_df['PassingTD'], proj_df['Int'], GLOBAL.HALF_PPR_SCORING
    )
)

#Get dataframes of specific pos
rb_proj_df = proj_df[proj_df['Pos'] == 'RB', ['Player, Team, Pos, Receptions, ReceivingYds, FL, ReceivingTD, RushingAtt, RushingYds, RushingTD, PassingAtt, PassingYds, PassingTD, Int']]
wr_proj_df = proj_df[proj_df['Pos'] == 'WR', ['Player, Team, Pos, Receptions, ReceivingYds, FL, ReceivingTD, RushingAtt, RushingYds, RushingTD, PassingAtt, PassingYds, PassingTD, Int']]
te_proj_df = proj_df[proj_df['Pos'] == 'TE', ['Player, Team, Pos, Receptions, ReceivingYds, FL, ReceivingTD, RushingAtt, RushingYds, RushingTD, PassingAtt, PassingYds, PassingTD, Int']]
qb_proj_df = proj_df[proj_df['Pos'] == 'QB', ['Player, Team, Pos, Receptions, ReceivingYds, FL, ReceivingTD, RushingAtt, RushingYds, RushingTD, PassingAtt, PassingYds, PassingTD, Int']]
# -

#Get dataframes of specific pos
rb_proj_df = proj_df[proj_df['Pos'] == 'RB']
wr_proj_df = proj_df[proj_df['Pos'] == 'WR']
te_proj_df = proj_df[proj_df['Pos'] == 'TE']
qb_proj_df = proj_df[proj_df['Pos'] == 'QB']

# +
#ADP for current year and scoring format
adp_df = pd.read_csv(GLOBAL.ADP_2021_HALF_PPR, index_col=0)

adp_df['ADP RANK'] = adp_df['AVG'].rank()

adp_df_cutoff = adp_df[:100]

replacement_players = {
    'RB': '',
    'WR': '',
    'TE': '',
    'QB': ''
}
# -

#ONLY FOR OLDER DATASETS
for _, row in adp_df_cutoff.iterrows():
    position = row['POS'][:1]
    print(position)
    player = row['Player']

    if position in replacement_players:
        replacement_players[position] = player

replacement_players

adp_df


