import os
import sys
src_dir = os.path.join(os.getcwd(), '..', 'src')
sys.path.append(src_dir)

UNV_PATH = '/'.join((sys.path[-1].split('/')[:5])) + '/data'

#Dataframes
PROJECTIONS_2021 = UNV_PATH + '/2021projections.csv'