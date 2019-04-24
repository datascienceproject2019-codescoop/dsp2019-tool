import pickle
import pandas as pd
import numpy as np
from typing import Dict, List
from statsmodels.regression.linear_model import RegressionResultsWrapper

OLS_MODEL_PATH = 'models/lasso_pickle'
ENCODER_PATH = 'models/encoder.pickle'
_ols_model = pickle.load(open(OLS_MODEL_PATH, 'rb'))
_encoder = pickle.load(open(ENCODER_PATH, 'rb'))

def get_test_data():
    test_data = None

    if (test_data is None):
        test_data = pd.read_csv('resources/repositories-1.4.0-2018-12-22-rating.csv')
        test_data = test_data.to_dict(orient='record')

    return test_data

# Hard-coded list of features our model deems are most important
_FEATURES = [
  'Language_1',
  'Deprecated',
  'License_4',
  'License_5',
  'Language_4',
  'Language_5',
  'Language_8',
  'Wiki enabled',
  'Size',
  'Language_6',
  'Language_7',
  'License_6',
  'Pull requests enabled',
  'Default branch',
  'License_2',
  'Language_2',
  'License_3',
  'Language_3',
  'Contributors Count',
  'Fork',
  'Pages enabled',
  'Issues enabled',
  'Open Issues Count',
  'Watchers Count',
  'Forks Count'
  ]
  

def _get_proper_dict(data: Dict[str, str]) -> Dict[str, List[str]]:
    """Used to turn dictionaries to form which Pandas understands"""
    proper = {}

    for k in data.keys():
      proper[k] = [data[k]]

    return proper


def _gnumeric_func (data, columns):
    data[columns] = data[columns].apply(lambda x: pd.factorize(x)[0])
    return data


def _getDummies (data, feature):
    dummies = pd.get_dummies(data[feature])
    data = pd.concat([data, dummies], axis=1)
    data = data.drop([feature],axis=1)
    return data


def _initDatax(data: pd.DataFrame):
    droplist = ['ID','SourceRank','Description', 'Name with Owner', \
      'Created Timestamp', "Updated Timestamp", 'Last pushed Timestamp', \
        'Homepage URL', 'Mirror URL', 'UUID', 'Last Synced Timestamp',\
          'Fork Source Name with Owner', 'Changelog filename', \
            'Contributing guidelines filename', 'License filename',\
              'Code of Conduct filename', 'Security Threat Model filename', \
                'Security Audit filename', 'SCM type', 'Logo URL', 'Keywords', \
                  'Stars Count']
    factorizelist = ['Default branch', 'Display Name', 'Pull requests enabled'] 
    truefalselist = ['Fork', 'Issues enabled', 'Wiki enabled', 'Pages enabled']
    dummieslist = ['Status','Host Type']
    binaryEncodelist = ['Language', 'License']

    datax = data.drop(droplist, axis=1)
    datax = datax.drop(['Readme filename'], axis=1) #idk why I need to do it separately, needs cleaning

    datax = _gnumeric_func(datax, factorizelist)
    datax[truefalselist] = datax[truefalselist] * 1

    for item in dummieslist:
        datax = _getDummies(datax,item)
        
    return datax


def predict_stars(data_dict) -> np.float64:
    """
    Predicts future stars of a Github projects. Regarding input: When using 
    dataframes to call this function, turn them to dictionaries as follows:
    `df.to_dict(orient='records')`. Depending on context it might return an 
    array, when additional call is required as follows: `array[0]`.
    Can throw OSError, if model-file is missing.
    """
    df = pd.DataFrame.from_dict(_get_proper_dict(data_dict))
    old_keys = set(df.keys())
    df = _initDatax(df)

    print("((((((((((((((((((one))))))))))))))))))")
    print(old_keys - set(df.keys()))
    encoded_df = _encoder.transform(df)
    print("((((((((((((((((two))))))))))))))))")
    df_cut = df[_FEATURES]
    print("(((((((((((((((three)))))))))))))))")
    prediction = _ols_model.predict(df_cut)
    print("(((((((((((((((four)))))))))))))))")

    return prediction.values[0]
