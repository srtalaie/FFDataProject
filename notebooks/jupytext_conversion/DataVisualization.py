# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
get_ipython().magic(u'matplotlib inline')

import os
import sys
src_dir = os.path.join(os.getcwd())
abs_path = os.path.abspath(os.path.join(src_dir, os.pardir, 'src'))
sys.path.append(abs_path)

from utils import GLOBAL, functions


# %%
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

pd.set_option('chained_assignment', None)


# %%
#Import yearly stats
stats_df = pd.read_csv(GLOBAL.STATS_2020)

#Override FantasyPoints Column with your League scoring
stats_df['FantasyPoints'] = functions.scoringCalculator(
    stats_df['Rec'], stats_df['ReceivingYds'], stats_df['ReceivingTD'], stats_df['FumblesLost'], stats_df['RushingYds'], stats_df['RushingTD'], stats_df['PassingYds'], stats_df['PassingTD'], stats_df['Int'], GLOBAL.PPR_SCORING
)


# %%
#Set Pts/G
stats_df['Pts/G'] = round((stats_df['FantasyPoints'] / stats_df['G']), 2)

#Set Usage/G (Tgts + RushingAtt)
stats_df['Usage/G'] = round((stats_df['Tgt'] + stats_df['RushingAtt']) / stats_df['G'], 2)


# %%
#Set up separate DFs by Pos
rb_stats_df = stats_df[stats_df['Pos'] == 'RB']
wr_stats_df = stats_df[stats_df['Pos'] == 'WR']
te_stats_df = stats_df[stats_df['Pos'] == 'TE']
qb_stats_df = stats_df[stats_df['Pos'] == 'QB']


# %%
#Rushing Attempts vs Targets for RBs
sns.set_style('darkgrid')

plt.figure(figsize=(15, 15))
plt.title('Rushing Atts vs Tgts for RBs', fontsize=16)

sns.scatterplot(x=rb_stats_df['RushingAtt'], y=rb_stats_df['Tgt']);


# %%
fig, ax = plt.subplots(figsize=(10, 10))

notable_players = ['Derrick Henry', 'Alvin Kamara', 'Johnathan Taylor', 'Miles Sander', 'Aaron Jones', 'Josh Jacobs', 'Chris Carson', 'Joe Mixon', 'Ronald Jones II', 'D\'Andre Swift', 'David Montgomery', 'Clyde Edwards-Helaire']

for player_name in notable_players:
    player = rb_stats_df[rb_stats_df['Player'] == player_name]

    if not player.empty:
        targets = player['Tgt']
        rushes = player['RushingAtt']

        ax.annotate(player_name, xy=(rushes+2, targets+2), color='red', fontsize=12)
        ax.scatter(rushes, targets, color='red')

sns.kdeplot(x=rb_stats_df['RushingAtt'], y=rb_stats_df['Tgt']);


# %%
plt.figure(figsize=(15, 15))

sns.jointplot(x=rb_stats_df['RushingAtt'], y=rb_stats_df['Tgt'], kind='kde');

sns.jointplot(x=rb_stats_df['RushingAtt'], y=rb_stats_df['Tgt'], kind='hex');


# %%
#RB Usage/G vs Pts/G Regression Plot
plt.figure(figsize=(12, 10))

sns.regplot(x=rb_stats_df['Usage/G'], y=rb_stats_df['Pts/G']);


# %%
#Dist of RB carries
plt.figure(figsize=(10, 10))
sns.kdeplot(rb_stats_df['RushingAtt']);


# %%
plt.figure(figsize=(10, 10))
sns.displot(rb_stats_df['RushingAtt']);


# %%
plt.figure(figsize=(10, 10))
sns.displot(rb_stats_df['Tgt'], bins=30);


# %%
#FFPts/G for RBs
plt.figure(figsize=(10, 10))
sns.displot(rb_stats_df['Pts/G'], bins=30);


# %%
sns.set_style('dark')
sns.residplot(x=rb_stats_df['Usage/G'], y=rb_stats_df['Pts/G'])
plt.title('Residual Plot')
plt.xlabel('Usage/G')
plt.ylabel('Pts/G');


# %%
rb_stats_df_copy = rb_stats_df[[
    'RushingAtt',
    'RushingTD',
    'Pts/G',
    'Tgt'
]]

sns.pairplot(rb_stats_df_copy)


# %%
final_df = pd.DataFrame()

final_df = functions.scoreByWeek(final_df, '2019', 1, 18)


# %%
lamar_jackson = final_df.loc[final_df['Player'] == 'Lamar Jackson']
patrick_mahomes = final_df.loc[final_df['Player'] == 'Patrick Mahomes']
russell_wilson = final_df.loc[final_df['Player'] == 'Russell Wilson']


# %%
sns.set_style('whitegrid')
plt.figure(figsize=(10, 8))
plt.plot(russell_wilson['Week'], russell_wilson['StandardFantasyPoints'])
plt.plot(patrick_mahomes['Week'], patrick_mahomes['StandardFantasyPoints'])
plt.plot(lamar_jackson['Week'], lamar_jackson['StandardFantasyPoints'])
plt.legend(['Wilson', 'Mahomes', 'Jackson'])
plt.xlabel('Week')
plt.ylabel('Fantasy Pts.')
plt.title('Wilson v. Mahomes v. Jackson Fantasy Performance');


# %%
lamar_jackson.corr()[['StandardFantasyPoints']]


# %%
sns.heatmap(lamar_jackson.corr()[['StandardFantasyPoints']], annot=True);


# %%
stats_df['Usage/G'] = (stats_df['RushingAtt'] + stats_df['PassingAtt'] + stats_df['Tgt']) / stats_df['G']


# %%
sns.lmplot(data=stats_df, x='Usage/G', y='Pts/G', hue='Pos', height=7);


# %%
te_corr = stats_df[stats_df['Pos'] == 'TE'].corr()[['Pts/G']]

plt.figure(figsize=(15, 10))

sns.heatmap(te_corr, annot=True);


# %%
COMBINE_URL = "https://raw.githubusercontent.com/fantasydatapros/data/master/combine/combine00to20.csv"

"""
The first two columns of this CSV file are messed up. Using iloc to grab all rows (:), and then grab the column indexed at 2 (so the third column), all the way to the last.
"""
combine_df = pd.read_csv(COMBINE_URL).iloc[:, 2:] # this is subject to change as I clean the data


# %%
combine_df.groupby('Pos')['40YD'].describe()


# %%
plt.figure(figsize=(10,10))
sns.boxplot(x='Pos', y='40YD', data=combine_df, palette=sns.color_palette('husl', n_colors=4));


