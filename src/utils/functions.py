import os
import sys
src_dir = os.path.join(os.getcwd(), '..', 'src')
sys.path.append(src_dir)

import pandas as pd
import numpy as np

#######Scoring Calculator#######
def scoringCalculator (rec, recYds, recTD, fl, rushYds, rushTD, passYds, passTD, int, SCORING_WEIGHTS):
    fantasy_score = rec * SCORING_WEIGHTS['Receptions'] + recYds * SCORING_WEIGHTS['ReceivingYds'] + recTD * SCORING_WEIGHTS['ReceivingTD'] + fl * SCORING_WEIGHTS['FL'] + rushYds * SCORING_WEIGHTS['RushingYds'] + rushTD * SCORING_WEIGHTS['RushingTD'] + passYds * SCORING_WEIGHTS['PassingYds'] + passTD * SCORING_WEIGHTS['PassingTD'] + int * SCORING_WEIGHTS['Int']

    return fantasy_score

#######Score By Week#######
def scoreByWeek (final_df, year, rangeStart, rangeEnd):
    for week in range(rangeStart, rangeEnd):
        df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/data/master/weekly/{year}/week{week}.csv'.format(year=year, week=week))

        df['Week'] = week

        final_df = pd.concat([final_df, df])

    return final_df

#######Correlation#######
def correlation(x, y):
    n = len(x)
    covariance = sum((x - np.mean(x)) * (y - np.mean(y))) * 1/(n-1)
    return covariance/(np.std(x) * np.std(y))

#######Get top player of pos#######
def get_top_n_player_at_eac_position(df, pos, n, scoring_format):
    df = df.loc[df['Pos'] == pos]

    return df.groupby('Tm', as_index=False).apply(
        lambda x: x.nlargest(n, [scoring_format]).min()
    )