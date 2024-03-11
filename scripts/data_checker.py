# Data checker for model_xgboost.py
# Coded by @ndre! RATM!
# Should you have any questions: andeeri@protonmail.com / https://github.com/andeeri-k

######## Import packages #######
import pandas as pd
from tabulate import tabulate
################################

def data_checker(data: pd.DataFrame):
    """Function to print statistics of the data"""
    def mean_absolute_error(marker_list: list, sex_list: list):
        return sum(abs(el1 - (el2+1)) for el1, el2 in zip(marker_list, sex_list) if el1 != 5) / len([i for i in marker_list if i != 5])
    print(f'Data checker:')
    print(f'Number of fish: {data[0].count()}')
    print(f'Ratio of males/females: {data[0].value_counts()[0]}/{data[0].value_counts()[1]}')
    tab_dic = {'col1': list(range(1, 16)), 'col2': [], 'col3': []}
    for i in range(1,16):
        tab_dic['col2'].append(round(mean_absolute_error(data[i], data[0]), 3))
        tab_dic['col3'].append(round(len(data[data[i]==5]) / len(data[i]), 3))
    print(tabulate(tab_dic, headers = ['Marker', 'Error rate', 'Missing rate'], tablefmt='pretty'))
    return 0