import pickle
import pandas as pd
from numpy import float64
from typing import Dict, List
from statsmodels.regression.linear_model import RegressionResultsWrapper

OLS_MODEL_PATH = 'models/ols.pickle'
_ols_model = None

def _get_featurelist():
    model = _get_ols_model()

    return model.params.keys().tolist()


def _get_proper_dict(data: Dict[str, str]) -> Dict[str, List[str]]:
    """Used to turn dictionaries to form which Pandas understands"""
    proper = {}

    for k in _get_featurelist():
        if k in data.keys():
            proper[k] = [data[k]]
        else:
            print('Key ' + k + ' was not in data. Setting default value 0')
            proper[k] = [0]

    return proper


def _get_ols_model() -> RegressionResultsWrapper:
    """Retrieves the saved model. The model should be downloaded by hand, since 
    it is quite big. Location is the inside OLD_MODEL_PATH"""
    global _ols_model

    if (_ols_model is None):
        with open(OLS_MODEL_PATH, 'rb') as pmodel:  
            _ols_model = pickle.load(pmodel)

    return _ols_model


def predict_dict(data: Dict[str, int]) -> float64:
    """
    Predicts future stars of a Github projects. Regarding input: When using 
    dataframes to call this function, turn them to dictionaries as follows:
    `df.to_dict(orient='records')`. Depending on context it might return an 
    array, when additional call is required as follows: `array[0]`.
    Can throw OSError, if model-file is missing.
    """
    formatted = _get_proper_dict(data)

    df = pd.DataFrame.from_dict(formatted, dtype=float64)
    #df = df[_get_featurelist()]

    model = _get_ols_model()
    prediction = model.predict(df)

    return prediction[0]
