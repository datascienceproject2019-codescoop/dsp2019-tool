import pandas as pd
from pandas.core.frame import DataFrame

_test500 = None

def _get_test_data() -> DataFrame:
    global _test500

    if (_test500 is None):
        _test500 = pd.read_csv('resources/data500.csv')

    return _test500


def get_projects() -> DataFrame:
    return _get_test_data()


def find_repos_by_name(name: str) -> DataFrame:
    t_data = _get_test_data()

    found = t_data.loc[t_data['Name with Owner'] == name]

    if (len(found) <= 1):
        found = [found]

    return found
