# Data checker for model_xgboost.py
# There is no error handling, code is tailored for use in xgboost program.
# Coded by @ndre! RATM!
# Should you have any questions: andeeri@protonmail.com / https://github.com/andeeri-k

######## Import packages #######
import pandas as pd
from tabulate import tabulate
################################


def data_checker(data: pd.DataFrame):
    """
    Print statistics of the data.

    Args:
        data (pd.DataFrame): Input DataFrame containing marker data.

    Returns:
        int: Always returns None.
    """
    # Define a function to calculate mean absolute error
    def mean_absolute_error(marker_list: list, sex_list: list):
        """
        Calculate the mean absolute error.

        Args:
            marker_list (list): List of marker values.
            sex_list (list): List of sex values.

        Returns:
            float: Mean absolute error.
        """
        return sum(abs(marker - (sex + 1)) for marker, sex in zip(marker_list, sex_list) if marker != 5) / len([i for i in marker_list if i != 5])

    # Print basic statistics
    print(f'Data checker:')
    print(f'Number of fish: {data.shape[0]}')
    print(f'Ratio of males/females: {data[0].value_counts()[0]}/{data[0].value_counts()[1]}')

    # Calculate error and missing rates
    tab_data = {'Marker': list(range(1, 16)), 'Error rate': [], 'Missing rate': []}
    for i in range(1, 16):
        error_rate = round(mean_absolute_error(data[i], data[0]), 3)
        missing_rate = round(len(data[data[i] == 5]) / len(data[i]), 3)
        tab_data['Error rate'].append(error_rate)
        tab_data['Missing rate'].append(missing_rate)

    # Print tabulated data
    print(tabulate(tab_data, headers='keys', tablefmt='pretty'))
    return None
