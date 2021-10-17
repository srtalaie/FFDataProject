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
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns


# %%
#Can either be: 'STD', 'PPR', or 'HALF_PPR
scoring_format = 'HALF_PPR'

ecr_df = pd.read_csv(f'https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/ecr/2021/9_6_2021/{scoring_format}.csv').dropna()

num_teams = 12
num_roster_spots = 16

draft_pool = num_teams * num_roster_spots

ecr_df = ecr_df[:draft_pool]


# %%
pd.set_option('display.max_rows', None)

X = ecr_df[['AVG.']].values

#Boris Chen uses 25 for k
k = 13

model = KMeans(n_clusters=k)

model.fit(X)

labels = model.predict(X)


# %%
#Map labels to the teirs
tiers = functions.assign_tiers(labels)

ecr_df['Tier'] = tiers


# %%
sns.set_style('whitegrid')

def make_clustering_viz(df, pos=None, figsize=(20, 20)):
    if pos:
        df = df.loc[df['POS'].str.contains(pos)]
    colors = [
        'purple', 'magenta', 'red', 'blue', 'orange', 'green', 'salmon', 'yellow', 'black', 'grey', '#3498db', '#16a085', '#f4d03f', '#f1948a', '#48c9b0', '#3498db', '#e74c3c', '#d7bde2', '#d0d3d4'
    ]
    colors = dict(zip(range(1, k+1), colors[:k]))

    plt.figure(figsize=figsize)

    plt.scatter(
        x=df['AVG.'],
        y=df['RK'],
        c='#212f3d',
        alpha=0.9,
        s=7
    )

    yticks = []

    for _, row in df.iterrows():
       xmin = row['BEST']
       xmax = row['WORST']
       ymin, ymax = row['RK'], row['RK']

       player = row['PLAYER NAME']

       tier = row['Tier']

       plt.plot(
           (xmin, xmax), (ymin, ymax), c=colors.get(tier, 'black'), alpha=0.8
       )

       yticks.append(player)
    
    patches = []

    for tier, color  in colors.items():
        patch = mpatches.Patch(color=color, label=f'Tier {tier}')
        patches.append(patch)

    plt.legend(handles=patches, borderpad=1, fontsize=12)

    plt.xlabel('Avg. Expert Rank', fontsize=12)
    plt.ylabel('Expert Consensus Rank', fontsize=12)
    plt.yticks(df['RK'], yticks, fontsize=12)

    plt.title('Tiers for 2021 draft. ECR vs. Average Expert Rank', fontsize=12)

    plt.gca().invert_yaxis()
    plt.show()


# %%
make_clustering_viz(ecr_df, figsize=(10,40))


