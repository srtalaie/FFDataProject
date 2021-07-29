import os
import sys
src_dir = os.path.join(os.getcwd(), '..', 'src')
sys.path.append(src_dir)

#######Scoring Calculator#######
def scoringCalculator (rec, recYds, recTD, fl, rushYds, rushTD, passYds, passTD, int, SCORING_WEIGHTS):
    fantasy_score = rec * SCORING_WEIGHTS['Receptions'] + recYds * SCORING_WEIGHTS['ReceivingYds'] + recTD * SCORING_WEIGHTS['ReceivingTD'] + fl * SCORING_WEIGHTS['FL'] + rushYds * SCORING_WEIGHTS['RushingYds'] + rushTD * SCORING_WEIGHTS['RushingTD'] + passYds * SCORING_WEIGHTS['PassingYds'] + passTD * SCORING_WEIGHTS['PassingTD'] + int * SCORING_WEIGHTS['Int']

    return fantasy_score
