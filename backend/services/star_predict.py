import pickle
import pandas as pd
from numpy import float64
from typing import Dict, List
from statsmodels.regression.linear_model import RegressionResultsWrapper

# Don't call this one, call _get_ols_model() instead
_ols_model = None

# Hard-coded list of features our model deems are most important
_featureList = {
    'Java'                  : (lambda data: _extract_boolean_key(data, 'Java')), 
    'Pages enabled'         : (lambda data: _boolean_to_binary(data, 'has_pages')), 
    'Issues enabled'        : (lambda data: _boolean_to_binary(data, 'has_issues')), 
    'Scala'                 : (lambda data: _extract_boolean_key(data, 'Scala')), 
    'PHP'                   : (lambda data: _extract_boolean_key(data, 'PHP')),
    'Python'                : (lambda data: _extract_boolean_key(data, 'Python')), 
    'Default branch'        : (lambda data: _extract_value(data, 'Default branch')), 
    'Size'                  : (lambda data: _extract_value(data, 'size')), 
    'Contributors Count'    : (lambda data: _extract_value(data, 'forks')),
    'Forks Count'           : (lambda data: _extract_value(data, 'Contributors Count')), 
    'Open Issues Count'     : (lambda data: _extract_value(data, 'Open Issues Count')), 
    'Watchers Count'        : (lambda data: _extract_value(data, 'watchers')), 
    'Emacs Lisp'            : (lambda data: _extract_boolean_key(data, 'Emacs Lisp')),
    'BSD-2-Clause'          : (lambda data: _license_equals(data, 'bsd-2-clause')), 
    'JavaScript'            : (lambda data: _extract_boolean_key(data, 'JavaScript')), 
    'Wiki enabled'          : (lambda data: _boolean_to_binary(data, 'has_wiki')),
    'MIT'                   : (lambda data: _license_equals(data, 'mit')),
    'Pull requests enabled' : (lambda data: -1), 
    'Fork'                  : (lambda data: 0), 
    'HTML'                  : (lambda data: _extract_boolean_key(data, 'HTML')), 
    'Other'                 : (lambda data: _other_prog_lang(data)), 
    'CSS'                   : (lambda data: _extract_boolean_key(data, 'CSS')), 
    'Go'                    : (lambda data: _extract_boolean_key(data, 'Go')),
    'Shell'                 : (lambda data: _extract_boolean_key(data, 'Shell')), 
    'Objective-C'           : (lambda data: _extract_boolean_key(data, 'Objective-C'))
}


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
    Predicts future stars of a Github projects. Regarding input: When using 
    dataframes to call this function, turn them to dictionaries as follows:
    `df.to_dict(orient='records')`. Depending on context it might return an 
    array, when additional call is required as follows: `array[0]`.
    Can throw OSError, if model-file is missing.
    """
    formatted = _get_proper_dict(data)
    
    frame = pd.DataFrame.from_dict(formatted, dtype=float64)
    # filter the dataframe
    frame = frame[_featureList.keys()]

    model = _get_ols_model()

    prediction = model.predict(frame)

    return prediction[0]

def _extract_boolean_key(data: Dict[str, str], key: str) -> int:
    if key in data.keys():
        return 1
    
    return 0


def _extract_value(data, key: str):
    if key in data.keys():
        return data[key]
    
    return ''


def predict_gh_data(data) -> float64:
    """
    Following the _featureList
    """
    dict_to_predict = {}

    for key, fun in _featureList.items():
        dict_to_predict[key] = fun(data)

    dict_to_predict = _get_proper_dict(dict_to_predict)

    frame = pd.DataFrame.from_dict(dict_to_predict, dtype=float64)

    model = _get_ols_model()
    
    return model.predict(frame)[0]


def _license_equals(data, license_key: str) -> int:
    try:
        if (data['license']['key'] == license_key):
            return 1
        else:
            return 0
    except TypeError:
        return 0


def _other_prog_lang(data) -> int:
    has_major_langs = False
    important_prog_lang = [
        'Java', 'HTML', 'Scala', 'PHP', 'Python', 'JavaScript', 'CSS', 'Go', 
        'Shell', 'Objective-C'
        ]

    keys = data.keys()

    for lang in important_prog_lang:
        if lang in keys:
            has_major_langs = True

    if (has_major_langs):
        return 0
    else:
        return 1


def _boolean_to_binary(data, column: str) -> int:
    if (data[column]):
        return 1
    else:
        return 0
    