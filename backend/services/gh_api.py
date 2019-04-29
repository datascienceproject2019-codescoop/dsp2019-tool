import pandas as pd
import requests
import json
import os
from pandas.core.frame import DataFrame
from typing import List, Dict
from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile

_test500 = None
_api_address = 'https://api.github.com'
_github = None

def get_github() -> Github:
    import os
    from github.GithubException import BadCredentialsException

    global _github

    if _github is None:
        try:
            _github = Github(os.environ.get('GITHUB_API_KEY'))
            # Just to test validity of credentials
            _github.get_repo('ArktinenSieni/discotetris')
        except BadCredentialsException as e:
            print(e)
            print('Invalid Github-credentials: initializing without API-key')
            _github = Github()

    return _github


def get_test_data() -> DataFrame:
    global _test500

    if (_test500 is None):
        _test500 = pd.read_csv('resources/data500.csv')

    return _test500


def _get_repo_langs(repo: Repository) -> Dict[str, int]:
    langs = repo.get_languages()

    for k, v in langs.items():
        langs[k] = 1

    return langs


def _get_pages_enabled(repo: Repository) -> int:
    """
    GET /repos/:owner/:repo/pages
    """
    address = _api_address + '/repos/' + repo.full_name + '/pages'
    response = json.loads(requests.get(address).content)
    
    try:
        if response['message'] == 'Not Found':
            return 0
    except:
        print('Error occured')
        return 0

    return 1


def _get_has_pulls(repo: Repository) -> int:
    pulls = repo.get_pulls()

    return 1 if (pulls.totalCount > 0) else 0


def _has_only_minor_lang(langs: Dict[str, int]) -> int:
    important_prog_lang = [
        'Java', 'HTML', 'Scala', 'PHP', 'Python', 'JavaScript', 'CSS', 'Go', 
        'Shell', 'Objective-C', 'Emacs Lisp'
        ]

    has_major = False

    for l in langs.keys():
        if l in important_prog_lang:
            has_major = True

    return 0 if has_major else 1


def _get_default_branch_index(repo: Repository) -> int:
    branch_name = repo.default_branch
    branches = repo.get_branches()

    branch_i = 0

    for i, b in enumerate(branches):
        if b.name == branch_name:
            branch_i = i
            break

    return branch_i


def _get_license(repo):
    from github.GithubException import UnknownObjectException
    license = None

    try:
        license = repo.get_license()
    except UnknownObjectException as e:
        # print('No licenses on repo ' + repo.full_name)
        pass

    return license


def _license_equals(license: ContentFile, license_key: str) -> int:
    if license is None:
        return 0

    return license.license.key == license_key


def find_repo_by_fullname_as_dict(f_name: str) -> Dict[str, int]:
    """
    Built on _featureList presented in star_predict.py-file.
    """

    if os.environ.get('GITHUB_API_KEY') == None:
        test_df = get_test_data()
        return test_df.to_dict(orient='records')[0]

    repo_as_dict = {}
    gh = get_github()

    repo = gh.get_repo(f_name)
    langs = _get_repo_langs(repo)
    license = _get_license(repo)

    repo_as_dict = {**repo_as_dict, **langs}
    repo_as_dict['Pages enabled'] = _get_pages_enabled(repo)
    repo_as_dict['Issues enabled'] = 1 if repo.has_issues else 0
    repo_as_dict['Forks Count'] = repo.forks_count
    repo_as_dict['Open Issues Count'] = repo.open_issues
    repo_as_dict['Watchers Count'] = repo.watchers
    repo_as_dict['BSD-2-Clause'] = _license_equals(license, 'bsd-2-clause')
    repo_as_dict['Wiki enabled'] = 1 if repo.has_wiki else 0
    repo_as_dict['MIT'] = _license_equals(license, 'mit')
    repo_as_dict['Pull requests enabled'] = _get_has_pulls(repo)
    repo_as_dict['Fork'] =  1 if (repo.fork) else 0
    repo_as_dict['Size'] = repo.size
    repo_as_dict['Contributors Count'] = repo.get_contributors().totalCount
    repo_as_dict['Other'] = _has_only_minor_lang(langs)
    repo_as_dict['Default branch'] = _get_default_branch_index(repo)
    repo_as_dict['Stars Count'] = repo.stargazers_count
    repo_as_dict['Language'] = repo.language

    return repo_as_dict
