import pickle
import pandas as pd
import numpy as np
from typing import Dict, List
from statsmodels.regression.linear_model import RegressionResultsWrapper

_ols_model = pickle.load(open('models/lasso/lasso.pkl', 'rb'))
_encoder = pickle.load(open('models/lasso/encoder.pkl', 'rb'))
test_data = None
preprocessed = None
prep_names = None
_hard_coded_sigmay = 807.8974922409773
_hard_coded_muy = 66.6701413333333

def get_test_data():
    global test_data

    if (test_data is None):
        test_data = pd.read_csv('data/repositories-1.4.0-2018-12-22-rating.csv')
        test_data = test_data.to_dict(orient='record')

    return test_data

  
def get_prep_data():
    global preprocessed

    if preprocessed is None:
        preprocessed = pd.read_csv('data/pre-processed_datax.csv', usecols=_FEATURES)

    return preprocessed


def get_prep_names():
    global prep_names

    if prep_names is None:
        prep_names = pd.read_csv('data/pre-processed_names.csv')

    return prep_names


# Hard-coded list of features our model deems are most important
_FEATURES = [
    'Language_0', 'Language_1', 'Language_2', 'Language_3', 'Language_4',
    'Language_5', 'Language_6', 'Language_7', 'Language_8', 'License_0',
    'License_1', 'License_2', 'License_3', 'License_4', 'License_5',
    'License_6', 'Fork', 'Size', 'Issues enabled', 'Wiki enabled',
    'Pages enabled', 'Forks Count', 'Open Issues Count', 'Default branch',
    'Watchers Count', 'Contributors Count', 'Display Name',
    'Pull requests enabled', 'Deprecated', 'Help Wanted', 'GitHub'
    ]


def predict_stars(repo_name: str) -> np.float64:
    """
    Predicts future stars of a Github projects. Regarding input: When using 
    dataframes to call this function, turn them to dictionaries as follows:
    `df.to_dict(orient='records')`. Depending on context it might return an 
    array, when additional call is required as follows: `array[0]`.
    Can throw OSError, if model-file is missing.
    """
    names = get_prep_names()['Name with Owner']
    id = names[names == repo_name].index[0]

    df = np.array(get_prep_data().iloc[[id]])
    
    df = df.reshape(1, -1)
    prediction = _ols_model.predict(df)[0]
    denormalized = round((prediction * _hard_coded_sigmay) + _hard_coded_muy)

    if denormalized <= 0:
        return 0

    return int(denormalized)
