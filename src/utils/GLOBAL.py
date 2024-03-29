import os
import sys

src_dir = os.path.join(os.getcwd())
abs_path = os.path.abspath(os.path.join(src_dir, os.pardir))
sys.path.append(abs_path)

os_path_sep = os.path.sep

UNV_PATH = sys.path[-1] + os_path_sep + "data" + os_path_sep

##########Dataframes##########
# Machine Learning Cleaned Data 2014-1018
CLEANED_DATA_2014_2019 = UNV_PATH + "2014_2019_weekly_data_cleaned.csv"

# Projections
PROJECTIONS_2020 = "https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/fp_projections.csv"
PROJECTIONS_2021 = UNV_PATH + "2021projections.csv"
PROJECTIONS_2022 = "https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/master/2022/06-Data%20Munging/1-Fantasy%20Pros%20Projections%20-%20(2022.08.23).csv"
PROJECTIONS_2023 = "https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/master/2023/06-Data%20Munging/01-Fantasy%20Pros%20Projections%20-%20(2023.08.17).csv"

# ADP
ADP_2020_STANDARD = "https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/adp/STANDARD_ADP.csv"
ADP_2020_HALF_PPR = "https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/adp/HALF_PPR_ADP.csv"
ADP_2020_PPR = "https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/adp/PPR_ADP.csv"
ADP_2021_STANDARD = UNV_PATH + "2021ADPStd.csv"
ADP_2021_HALF_PPR = UNV_PATH + "2021ADPHalfPPR.csv"
ADP_2021_PPR = UNV_PATH + "2021ADPPPR.csv"
ADP_2022_STANDARD = "https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/master/2022/06-Data%20Munging/02-ADP%20(Standard)%20-%20(2022.08.23).csv"
ADP_2022_HALF_PPR = "https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/master/2022/06-Data%20Munging/02-ADP%20(Half%20PPR)%20-%20(2022.08.23).csv"
ADP_2022_PPR = "https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/master/2022/06-Data%20Munging/02-ADP%20(PPR)%20-%20(2022.08.23).csv"
ADP_2023_HALF_PPR = "https://raw.githubusercontent.com/fantasydatapros/LearnPythonWithFantasyFootball/master/2023/06-Data%20Munging/02-ADP%20Data%20-%20(2023.08.17).csv"

# Yearly Stats
STATS_2022 = "https://raw.githubusercontent.com/srtalaie/FFDataProject/master/data/2022_Stats.csv"
STATS_2021 = (
    "https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2021.csv"
)
STATS_2020 = (
    "https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2020.csv"
)
STATS_2019 = (
    "https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2019.csv"
)
STATS_2018 = (
    "https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2018.csv"
)
STATS_2017 = (
    "https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2017.csv"
)
STATS_2016 = (
    "https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2016.csv"
)
STATS_2015 = (
    "https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2015.csv"
)


##########FantasyScoring##########
STANDARD_SCORING = {
    "Receptions": 0,
    "ReceivingYds": 0.1,
    "ReceivingTD": 6,
    "FL": -2,
    "RushingAtt": 0,
    "RushingYds": 0.1,
    "RushingTD": 6,
    "PassingYds": 0.04,
    "PassingTD": 4,
    "Int": -2,
}

HALF_PPR_SCORING = {
    "Receptions": 0.5,
    "ReceivingYds": 0.1,
    "ReceivingTD": 6,
    "FL": -2,
    "RushingAtt": 0,
    "RushingYds": 0.1,
    "RushingTD": 6,
    "PassingYds": 0.04,
    "PassingTD": 4,
    "Int": -2,
}

PPR_SCORING = {
    "Receptions": 1,
    "ReceivingYds": 0.1,
    "ReceivingTD": 6,
    "FL": -2,
    "RushingAtt": 0,
    "RushingYds": 0.1,
    "RushingTD": 6,
    "PassingYds": 0.04,
    "PassingTD": 4,
    "Int": -2,
}
