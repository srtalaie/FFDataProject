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
import numpy as np
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


# %%
data_df = pd.DataFrame()

yearStart = 2014
yearEnd = 2021

WEEKLY_BASE_URL = "https://raw.githubusercontent.com/fantasydatapros/data/master/weekly/{year}/week{week}.csv"

for year in range(yearStart, yearEnd):
    for week in range(1, 18):
        weekly_df = pd.read_csv(WEEKLY_BASE_URL.format(year=year, week=week))
        weekly_df['Year'] = year
        weekly_df['Week'] = week
        weekly_df['Usage'] = (weekly_df['PassingAtt'] + weekly_df['RushingAtt'] + weekly_df['Tgt'])
        data_df = pd.concat([data_df, weekly_df])


# %%
#Cleaning up TM values
data_df.loc[(data_df['Tm'] == 'OTI'), 'Tm'] = 'TEN'
data_df.loc[(data_df['Tm'] == 'RAM'), 'Tm'] = 'LAR'
data_df.loc[(data_df['Tm'] == 'STL'), 'Tm'] = 'LAR'
data_df.loc[(data_df['Tm'] == 'HTX'), 'Tm'] = 'HOU'
data_df.loc[(data_df['Tm'] == 'SDG'), 'Tm'] = 'LAC'
data_df.loc[(data_df['Tm'] == 'OAK'), 'Tm'] = 'LV'
data_df.loc[(data_df['Tm'] == 'RAI'), 'Tm'] = 'LV'
data_df.loc[(data_df['Tm'] == 'CLT'), 'Tm'] = 'IND'
data_df.loc[(data_df['Tm'] == 'RAV'), 'Tm'] = 'BAL'
data_df.loc[(data_df['Tm'] == 'CRD'), 'Tm'] = 'ARI'
data_df.loc[(data_df['Tm'] == 'NOR'), 'Tm'] = 'NO'


# %%
data_df = data_df.groupby(['Player', 'Pos', 'Tm', 'Year'], as_index=False)    .agg({
        'Usage': np.sum,
        'PassingYds': np.sum,
        'PassingTD': np.sum,
        'PassingAtt': np.sum,
        'RushingAtt': np.sum,
        'RushingYds': np.sum,
        'RushingTD': np.sum,
        'Rec': np.sum,
        'Tgt': np.sum,
        'ReceivingYds': np.sum,
        'ReceivingTD': np.sum,
        'PPRFantasyPoints': np.sum,
        'StandardFantasyPoints': np.sum,
        'HalfPPRFantasyPoints': np.sum
    })


# %%
#Set Scoring format that will be used below ('HalfPPR', 'PPR', or 'Standard')
scoring_format = 'HalfPPR'


# %%
pd.set_option('chained_assignment', None)

lag_features = [
    'RushingAtt',
    'Tgt',
    'Usage', 
    f'{scoring_format}FantasyPoints', 
    'PassingAtt', 
    'PassingTD'
]

for lag in range(1, 7):
    shifted = data_df.groupby('Player').shift(lag)

    for column in lag_features:
        data_df[f'lag_{column}_{lag}'] = shifted[column]
        
data_df = data_df.fillna(-1)


# %%
#Separate by pos
wr_df = data_df.loc[data_df['Pos'] == 'WR']
rb_df = data_df.loc[data_df['Pos'] == 'RB']
te_df = data_df.loc[data_df['Pos'] == 'TE']
qb_df = data_df.loc[data_df['Pos'] == 'QB']

# %% [markdown]
# WRs

# %%
X = wr_df[['lag_Tgt_1', 'lag_RushingAtt_1', 'lag_PassingAtt_1', 'lag_Usage_1', f'lag_{scoring_format}FantasyPoints_1']]
y = wr_df[f'{scoring_format}FantasyPoints'].values

WR_X_train, WR_X_test, WR_y_train, WR_y_test = train_test_split(X, y, test_size=0.2, random_state=10)

lr = LinearRegression()

lr.fit(WR_X_train, WR_y_train)

WR_y_predict = lr.predict(WR_X_test)

mean_absolute_error(WR_y_test, WR_y_predict)


# %%
wr_df_pred = wr_df.loc[
    (wr_df['Usage'] > 50) & (wr_df['Year'] == 2020),
     ['Player', 'Tgt', 'RushingAtt', 'PassingAtt', 'Usage', f'{scoring_format}FantasyPoints']
]

wr_df_pred['Predicted_2021'] = lr.predict(
    wr_df_pred[['Tgt', 'RushingAtt', 'PassingAtt', 'Usage', f'{scoring_format}FantasyPoints']].values
)

wr_df_pred.sort_values(by='Predicted_2021', ascending=False).head(100)

# %% [markdown]
# RBs

# %%
X = rb_df[['lag_Tgt_1', 'lag_RushingAtt_1', 'lag_PassingAtt_1', 'lag_Usage_1', f'lag_{scoring_format}FantasyPoints_1']]
y = rb_df[f'{scoring_format}FantasyPoints'].values

RB_X_train, RB_X_test, RB_y_train, RB_y_test = train_test_split(X, y, test_size=0.2, random_state=10)

lr = LinearRegression()

lr.fit(RB_X_train, RB_y_train)

RB_y_predict = lr.predict(RB_X_test)

mean_absolute_error(RB_y_test, RB_y_predict)


# %%
rb_df_pred = rb_df.loc[
    (rb_df['Usage'] > 50) & (rb_df['Year'] == 2020),
     ['Player', 'Tgt', 'RushingAtt', 'PassingAtt', 'Usage', f'{scoring_format}FantasyPoints']
]

rb_df_pred['Predicted_2021'] = lr.predict(
    rb_df_pred[['Tgt', 'RushingAtt', 'PassingAtt', 'Usage', f'{scoring_format}FantasyPoints']].values
)

rb_df_pred.sort_values(by='Predicted_2021', ascending=False).head(100)

# %% [markdown]
# TEs

# %%
X = te_df[['lag_Tgt_1', 'lag_RushingAtt_1', 'lag_PassingAtt_1', 'lag_Usage_1', f'lag_{scoring_format}FantasyPoints_1']]
y = te_df[f'{scoring_format}FantasyPoints'].values

TE_X_train, TE_X_test, TE_y_train, TE_y_test = train_test_split(X, y, test_size=0.2, random_state=10)

lr = LinearRegression()

lr.fit(TE_X_train, TE_y_train)

TE_y_predict = lr.predict(TE_X_test)

mean_absolute_error(TE_y_test, TE_y_predict)


# %%
te_df_pred = te_df.loc[
    (te_df['Usage'] > 50) & (te_df['Year'] == 2020),
     ['Player', 'Tgt', 'RushingAtt', 'PassingAtt', 'Usage', f'{scoring_format}FantasyPoints']
]

te_df_pred['Predicted_2021'] = lr.predict(
    te_df_pred[['Tgt', 'RushingAtt', 'PassingAtt', 'Usage', f'{scoring_format}FantasyPoints']].values
)

te_df_pred.sort_values(by='Predicted_2021', ascending=False).head(100)

# %% [markdown]
# QBs

# %%
X = qb_df[['lag_Tgt_1', 'lag_RushingAtt_1', 'lag_PassingAtt_1', 'lag_Usage_1', f'lag_{scoring_format}FantasyPoints_1']]
y = qb_df[f'{scoring_format}FantasyPoints'].values

QB_X_train, QB_X_test, QB_y_train, QB_y_test = train_test_split(X, y, test_size=0.2, random_state=10)

lr = LinearRegression()

lr.fit(QB_X_train, QB_y_train)

QB_y_predict = lr.predict(QB_X_test)

mean_absolute_error(QB_y_test, QB_y_predict)


# %%
qb_df_pred = qb_df.loc[
    (qb_df['Usage'] > 50) & (qb_df['Year'] == 2020),
     ['Player', 'Tgt', 'RushingAtt', 'PassingAtt', 'Usage', f'{scoring_format}FantasyPoints']
]

qb_df_pred['Predicted_2021'] = lr.predict(
    qb_df_pred[['Tgt', 'RushingAtt', 'PassingAtt', 'Usage', f'{scoring_format}FantasyPoints']].values
)

qb_df_pred.sort_values(by='Predicted_2021', ascending=False).head(100)


