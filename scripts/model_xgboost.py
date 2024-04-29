# Code for XGB model. Train, GridSerchCV, validation.
# No parser option implemented, usage: python3 model_xgboost.py your_data_name trained_model_file_name
# Coded by @ndre! RATM!
# Should you have any questions: andeeri@protonmail.com / https://github.com/andeeri-k


############## Import packages ######################
import numpy as np
import pandas as pd
import sys
import xgboost as xgb
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from statistics import mean
# Custom module
try:
    from data_checker import data_checker
    checker = True
except ImportError:
    checker = False
    pass
#####################################################

data_file = sys.argv[1] # your data
out_model_filename = sys.argv[2] # file name for the trained model
# data_file = 'sim_random.dat'
# out_model_filename = 'sim_random_xgboost_model.bin'

# Load work data, make target vector y and feature matrix X, re-code missing SNPs (5) in X to nan
dat = pd.read_csv(data_file, header=None, sep=',')
if checker:
    data_checker(dat)  # check the data
y = dat[0].copy(deep=True)  # target vector
X = dat[list(range(1, 16))].copy(deep=True)  # feature matrix
X.replace(5, np.nan, inplace=True)  # set missing SNPs (5) to 'not a number'


# Initiate Extreme Gradient Boost Binary Logistics Classifier with default parameters
clf = xgb.XGBClassifier(objective='binary:logistic', min_child_weight=0)


# Run GridSearchCV to find the best suitable parameters for the model
param_grid = {
    'learning_rate': [0.05, 0.1, 0.15, 0.2, 0.25, 0.3],
    'max_depth': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    'subsample': [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    'colsample_bytree': [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
}

gscv = GridSearchCV(estimator=clf, param_grid=param_grid, scoring='accuracy', cv=5, verbose=1) # initiate GridSerchCV
gscv.fit(X, y) # run GridSerchCV
best_params = gscv.best_params_ # store the best params
print("Best Parameters:", best_params) # print the best params
best_model = gscv.best_estimator_ # store the best model
best_model.save_model(out_model_filename) # save trained model


# Function to perform n-fold cross validation
def n_fold_validation(X: pd.DataFrame, y: pd.Series, model_params: dict, n_folds: int, iterations: int) -> None:
    """"Function to perform n-fold validation (n_folds) n times (iterations)
    Args:
        X (pd.DataFrame): Input DataFrame containing marker data
        y (pd.DataFrame): Input DataFrame containing sex data
        model_params (dict): Input dictionary with model parameters
        n_folds (int): number of data splits
        interations (int): number of repeated rounds
    
    Returns:
        Always returns None
    
    """
    print(f'\nPerforming {n_folds}-f cross validation')
    aggregator_of_means = [] # list of accuracy means
    clf_cv = xgb.XGBClassifier(objective='binary:logistic', min_child_weight=0, **model_params) # initiate model
    for i in range(iterations):
      folds = KFold(n_splits=n_folds, shuffle=True, random_state=802)
      cv_accuracy = cross_val_score(clf_cv, X, y, cv=folds, scoring='accuracy')
      aggregator_of_means.append(cv_accuracy.mean())
    mean_ag = mean(aggregator_of_means) # mean accuracy in n-folds
    test_group = len(y)//n_folds # size of the test group
    miscls = int(test_group * (1 - mean_ag)) # number of misclassified samples
    perc_miscls = int(miscls / test_group * 100) # percent of misclassified samples
    print(f'Mean 5-f cross validation replicated {iterations} times was {mean(aggregator_of_means):.5f}')
    print(f'Average number misclassified samples: {miscls}')
    print(f'Average percentage misclassified samples: {perc_miscls}%')
    return None

# Perform n-fold cross validation
# 5-fold CV replicated 20 times (100 rounds in total)
n_fold_validation(X, y, best_params, 5, 20)
# 3-fold CV replicated 20 times (60 rounds in total)
n_fold_validation(X, y, best_params, 3, 20)
# 2-fold CV replicated 20 times (40 rounds in total)
n_fold_validation(X, y, best_params, 2, 20)