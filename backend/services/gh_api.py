import pandas as pd
import requests
import json
from pandas.core.frame import DataFrame
from typing import List, Dict

_test500 = None
_api_address = 'https://api.github.com'

def _get_test_data() -> DataFrame:
    global _test500

    if (_test500 is None):
        _test500 = pd.read_csv('resources/data500.csv')

    return _test500



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
def get_projects() -> DataFrame:
    return _get_test_data()


def find_repos_by_name(name: str) -> List[DataFrame]:
    t_data = _get_test_data()

    found = t_data.loc[t_data['Name with Owner'] == name]

    if (len(found) <= 1):
        found = [found]

    return found

def find_repositories_by_fullname(name: str) -> List[Dict[str, str]]:
    address = _api_address + '/search/repositories?q=' + name
    response = requests.get(address).content
    loaded = json.loads(response)

    return loaded['items']


def find_langs_by_fullname(name: str) -> Dict[str, str]:
    address = _api_address + '/repos/' + name + '/languages'

    response = requests.get(address).content

    return json.loads(response)


def count_items_by_link(address: str) -> int:
    response = requests.get(address).content

    json_list = json.loads(response)

    return len(json_list)


def get_open_issues_by_fullname(name: str):
    """
    Returns dict as {'total_count': 0, 'incomplete_results': False, 'items': []}
    """
    address = _api_address + '/search/issues?q=' + name + '+state:open'
    response = requests.get(address).content

    return json.loads(response)


def get_branch_index(branches_url: str, branch_name: str) -> int:
    branch_url = branches_url.split('{')[0]

    response = requests.get(branch_url).content
    branches = json.loads(response)

    branch_index = 0

    for i, branch in enumerate(branches):
        if branch['name'] == branch_name:
            branch_index = i

    return branch_index
