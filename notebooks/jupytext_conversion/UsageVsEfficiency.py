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

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt

from sklearn.metrics import mean_squared_error
import math


from sklearn.metrics import r2_score


# %%
#Create DFs
yearly_stats_df = pd.read_csv(GLOBAL.STATS_2020)


# %%
#Calculate Fantasy Scoring for all formats, Usage, Usage/G, and Pts/G (by format)

#Fantasy score
yearly_stats_df['FantasyPointsPPR'] = functions.scoringCalculator(
    yearly_stats_df['Rec'], yearly_stats_df['ReceivingYds'], yearly_stats_df['ReceivingTD'], yearly_stats_df['FumblesLost'], yearly_stats_df['RushingYds'], yearly_stats_df['RushingTD'], yearly_stats_df['PassingYds'], yearly_stats_df['PassingTD'], yearly_stats_df['Int'], GLOBAL.PPR_SCORING)

yearly_stats_df['FantasyPointsHalfPPR'] = functions.scoringCalculator(
    yearly_stats_df['Rec'], yearly_stats_df['ReceivingYds'], yearly_stats_df['ReceivingTD'], yearly_stats_df['FumblesLost'], yearly_stats_df['RushingYds'], yearly_stats_df['RushingTD'], yearly_stats_df['PassingYds'], yearly_stats_df['PassingTD'], yearly_stats_df['Int'], GLOBAL.HALF_PPR_SCORING)

yearly_stats_df['FantasyPoints'] = functions.scoringCalculator(
    yearly_stats_df['Rec'], yearly_stats_df['ReceivingYds'], yearly_stats_df['ReceivingTD'], yearly_stats_df['FumblesLost'], yearly_stats_df['RushingYds'], yearly_stats_df['RushingTD'], yearly_stats_df['PassingYds'], yearly_stats_df['PassingTD'], yearly_stats_df['Int'], GLOBAL.STANDARD_SCORING)


#Usage & Usage/G
yearly_stats_df['Usage'] = yearly_stats_df['RushingAtt'] + yearly_stats_df['PassingAtt'] + yearly_stats_df['Tgt']
yearly_stats_df['Usage/G'] = (yearly_stats_df['RushingAtt'] + yearly_stats_df['PassingAtt'] + yearly_stats_df['Tgt']) / yearly_stats_df['G']

#Pts/G
yearly_stats_df['StandardPoints/G'] = yearly_stats_df['FantasyPoints'] / yearly_stats_df['G']
yearly_stats_df['HalfPPRPoints/G'] = yearly_stats_df['FantasyPointsHalfPPR'] / yearly_stats_df['G']
yearly_stats_df['PPRPoints/G'] = yearly_stats_df['FantasyPointsPPR'] / yearly_stats_df['G']


# %%
#Create Usage rank & Fantasy Points Rank
yearly_stats_df['UsageRank'] = yearly_stats_df['Usage'].rank(ascending=False)

yearly_stats_df['StandardFantasyPointsRank'] = yearly_stats_df['FantasyPoints'].rank(ascending=False)
yearly_stats_df['HalfPPRFantasyPointsRank'] = yearly_stats_df['FantasyPointsHalfPPR'].rank(ascending=False)
yearly_stats_df['PPRFantasyPointsRank'] = yearly_stats_df['FantasyPointsPPR'].rank(ascending=False)


# %%
#Filter Based on Positions
yearly_RB_stats_df = yearly_stats_df[yearly_stats_df['Pos'] == 'RB']
yearly_WR_stats_df = yearly_stats_df[yearly_stats_df['Pos'] == 'WR']
yearly_TE_stats_df = yearly_stats_df[yearly_stats_df['Pos'] == 'TE']
yearly_QB_stats_df = yearly_stats_df[yearly_stats_df['Pos'] == 'QB']


# %%
#Finding the Correlation based on Usage vs Scoring per format
x = yearly_stats_df['Usage'].values.reshape(-1, 1)
y_std = yearly_stats_df['FantasyPoints'].values.reshape(-1, 1)
y_half_ppr = yearly_stats_df['FantasyPointsHalfPPR'].values.reshape(-1, 1)
y_ppr = yearly_stats_df['FantasyPointsPPR'].values.reshape(-1, 1)

standard_correlation = functions.correlation(x, y_std)
half_ppr_correlation = functions.correlation(x, y_half_ppr)
ppr_correlation = functions.correlation(x, y_ppr)


# %%
#Use Machine Learning to test/train data

#Can change out Y (dependent var) var with above vars based on scoring format you want to use
X = x
Y = y_half_ppr

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
regressor = LinearRegression()  
regressor.fit(x_train, y_train) #training the algorithm
y_pred = regressor.predict(x_test)


# %%
prediction_df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
prediction_df.head()


# %%
#Calculate Std Deviviation, determine predictors accuracy
mse = mean_squared_error(y_test,y_pred)
rmse = math.sqrt(mse)
rmse


# %%
#Determine correlation coefficient of Y var to determine accuracy
coeff_of_determination = r2_score(y_test, y_pred)
print('The coefficient of determination is', coeff_of_determination)


