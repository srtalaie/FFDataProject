import os
import sys
src_dir = os.path.join(os.getcwd(), '..', 'src')
sys.path.append(src_dir)

UNV_PATH = '/'.join((sys.path[-1].split('/')[:5])) + '/data'

##########Dataframes##########
#Projections
PROJECTIONS_2021 = UNV_PATH + '/2021projections.csv'
PROJECTIONS_2020 = 'https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/fp_projections.csv'

#ADP
ADP_2020_STANDARD = 'https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/adp/STANDARD_ADP.csv'
ADP_2020_HALF_PPR = 'https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/adp/HALF_PPR_ADP.csv'
ADP_2020_PPR = 'https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/adp/PPR_ADP.csv'
ADP_2021_STANDARD= UNV_PATH + '/2021ADPStd.csv'
ADP_2021_HALF_PPR= UNV_PATH + '/2021ADPHalfPPR.csv'
ADP_2021_PPR= UNV_PATH + '2021ADPPPR.csv'

#Yearly Stats
STATS_2020 = 'https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2020.csv'
STATS_2019 = 'https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2019.csv'
STATS_2018 = 'https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2018.csv'
STATS_2017 = 'https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2017.csv'
STATS_2016 = 'https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2016.csv'
STATS_2015 = 'https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2015.csv'


##########FantasyScoring##########
STANDARD_SCORING = {
    'Receptions': 0,
    'ReceivingYds': 0.1,
    'ReceivingTD': 6,
    'FL': -2,
    'RushingAtt': 0,
    'RushingYds': 0.1,
    'RushingTD': 6,
    'PassingYds': 0.04,
    'PassingTD': 4,
    'Int': -2
}

HALF_PPR_SCORING = {
    'Receptions': 0.5,
    'ReceivingYds': 0.1,
    'ReceivingTD': 6,
    'FL': -2,
    'RushingAtt': 0,
    'RushingYds': 0.1,
    'RushingTD': 6,
    'PassingYds': 0.04,
    'PassingTD': 4,
    'Int': -2
}

PPR_SCORING = {
    'Receptions': 1,
    'ReceivingYds': 0.1,
    'ReceivingTD': 6,
    'FL': -2,
    'RushingAtt': 0,
    'RushingYds': 0.1,
    'RushingTD': 6,
    'PassingYds': 0.04,
    'PassingTD': 4,
    'Int': -2
}