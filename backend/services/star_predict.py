import pickle
import pandas as pd
from numpy import float64
from typing import Dict, List
from statsmodels.regression.linear_model import RegressionResultsWrapper

_lasso_model = pickle.load(open('models/lasso/lasso-old.pkl', 'rb'))

def _get_proper_dict(data: Dict[str, str]) -> Dict[str, List[str]]:
    """Used to turn dictionaries to form which Pandas understands"""
    proper = {}
    features = _lasso_model.params.keys().tolist()
    for k in features:
        if k in data.keys():
            proper[k] = [data[k]]
        else:
            print('Key ' + k + ' was not in data. Setting default value 0')
            proper[k] = [0]

    return proper

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

    # model = _get_lasso_model()
    prediction = _lasso_model.predict(df)

    return prediction[0]
