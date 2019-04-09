import pickle
import pandas as pd
import numpy as np
from typing import Dict, List
from statsmodels.regression.linear_model import RegressionResultsWrapper

OLS_MODEL_PATH = 'models/ols.pickle'
_ols_model = pickle.load(open(OLS_MODEL_PATH, 'rb'))

# Hard-coded list of features our model deems are most important
_FEATURES = [
    'Java', 
    'Pages enabled', 
    'Issues enabled', 
    'Scala', 
    'PHP',
    'Python', 
    'Default branch', 
    'Size', 
    'Contributors Count',
    'Forks Count', 
    'Open Issues Count', 
    'Watchers Count', 
    'Emacs Lisp',
    'BSD-2-Clause', 
    'JavaScript', 
    'Wiki enabled', 
    'MIT',
    'Pull requests enabled', 
    'Fork', 
    'HTML', 
    'Other', 
    'CSS', 
    'Go',
    'Shell', 
    'Objective-C'
  ]

def predict_stars(df) -> np.float64:
    """
    Predicts future stars of a Github projects. Regarding input: When using 
    dataframes to call this function, turn them to dictionaries as follows:
    `df.to_dict(orient='records')`. Depending on context it might return an 
    array, when additional call is required as follows: `array[0]`.
    Can throw OSError, if model-file is missing.
    """
    df_cut = df[_FEATURES]

    prediction = _ols_model.predict(df_cut)

    return prediction.values[0]
