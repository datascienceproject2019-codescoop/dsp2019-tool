import pickle
import pandas as pd
from numpy import float64
from typing import Dict, List
from statsmodels.regression.linear_model import RegressionResultsWrapper

# Don't call this one, call _get_ols_model() instead
_ols_model = None

# Hard-coded list of features our model deems are most important
_featureList = [
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


def _get_proper_dict(data: Dict[str, str]) -> Dict[str, List[str]]:
    """Used to turn dictionaries to form which python understands"""
    for k, v in data.items():
        data[k] = [v]

    return data


def _get_ols_model() -> RegressionResultsWrapper:
    """Retrieves the saved model. The model should be downloaded by hand, since 
    it is quite big. Location is the inside backend/models/"""
    global _ols_model

    if (_ols_model is None):
        with open('models/pickle_model', 'rb') as pmodel:  
            _ols_model = pickle.load(pmodel)

    return _ols_model


def predict_stars(data: Dict[str, str]) -> float64:
    """
    Predicts future stars of a Github projects
    Can throw OSError, if model is missing.
    """
    formatted = _get_proper_dict(data)
    
    frame = pd.DataFrame.from_dict(formatted, dtype=float64)
    # filter the dataframe
    frame = frame[_featureList]

    model = _get_ols_model()

    prediction = model.predict(frame)

    return prediction[0]