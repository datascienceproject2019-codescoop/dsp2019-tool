import pandas as pd
import requests
from pandas.core.frame import DataFrame
from typing import List

_test500 = None
_api_address = 'https://api.github.com'

def _get_test_data() -> DataFrame:
    global _test500

    if (_test500 is None):
        _test500 = pd.read_csv('resources/data500.csv')

    return _test500


def get_projects() -> DataFrame:
    return _get_test_data()


def find_repos_by_name(name: str) -> List[DataFrame]:
    t_data = _get_test_data()

    found = t_data.loc[t_data['Name with Owner'] == name]

    if (len(found) <= 1):
        found = [found]

    return found

def find_repositories_by_name(name: str) -> List[DataFrame]:
    address = _api_address + '/repositories?q=' + name

    df = pd.read_json(requests.get(address).content)

    if (len(df) <= 1):
        df = [df]

    return df