import os
import time
import pandas as pd
import numpy as np
from datetime import datetime
from github import Github
from github import GithubException


LOWER_BOUND           = 1.791759469228055
UPPER_BOUND           = 42.40071186221785
TIMESTAMP_LOWER_BOUND = "2012-12-12 17:51:25"


'''
Create some plots that contains chronological data for a repository:
    - stars count
    - forks count
    - watchers count
    - contributors count
    - rating

The intended dataframe is the one stored in: resources/repositories-timeseries.csv

The np arrays can be composed of either four or five elements:
    - the first four are the historical data points of the repository
    - the fifth point is fetched via the github api; this can most likely fail due to:
            - error 404: the repository does not exist anymore
            - error 502: temporary github api problem
            - exceeded the api call limit

Also fetches some recent commits, closed issues and open issues and plots them.

Note: it is assumed that the repository name that is given as a input to the fuctions
      does actually exist in the dataframe
      (there is no problem if it does not exist on github)
'''


def _get_stars_count(github_client, repository_name):
    '''
    Get the Stars Count for a given repository
    '''

    try:
        repo  = github_client.get_repo(repository_name)
        count = repo.stargazers_count

        return count

    except GithubException as error:

        if error.status == 404:
            return None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo  = github_client.get_repo(repository_name)
                count = repo.stargazers_count

                return count

            except GithubException as error:
                return None


def _get_forks_count(github_client, repository_name):
    '''
    Get the Forks Count for a given repository
    '''

    try:
        repo  = github_client.get_repo(repository_name)
        count = repo.forks_count

        return count

    except GithubException as error:

        if error.status == 404:
            return None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo  = github_client.get_repo(repository_name)
                count = repo.forks_count

                return count

            except GithubException as error:
                return None


def _get_watchers_count(github_client, repository_name):
    '''
    Get the Watchers Count for a given repository
    '''

    try:
        repo  = github_client.get_repo(repository_name)
        count = repo.subscribers_count

        return count

    except GithubException as error:

        if error.status == 404:
            return None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo  = github_client.get_repo(repository_name)
                count = repo.subscribers_count

                return count

            except GithubException as error:
                return None


def _get_contributors_count(github_client, repository_name):
    '''
    Get the Contributors Count for a given repository
    '''

    try:
        repo  = github_client.get_repo(repository_name)
        count = repo.get_contributors().totalCount

        return count

    except GithubException as error:

        if error.status == 404:
            return None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo  = github_client.get_repo(repository_name)
                count = repo.get_contributors().totalCount

                return count

            except GithubException as error:
                return None


def _get_rating(github_client, repository_name):
    '''
    Determine the Rating for a given repository
    '''

    try:
        repo  = github_client.get_repo(repository_name)

        star_count        = repo.stargazers_count
        fork_count        = repo.forks_count
        contributor_count = repo.get_contributors().totalCount
        watchers_count    = repo.subscribers_count
        open_issues       = repo.get_issues(state = 'open').totalCount

        updated_timestamp = repo.updated_at
        upd_timestamp = (updated_timestamp - datetime.strptime(TIMESTAMP_LOWER_BOUND, '%Y-%m-%d %H:%M:%S')).days

        has_pages = 0
        for branch in repo.get_branches():
            if branch.name == "gh-pages":
                has_pages = 1

                break

        rating = has_pages + int(repo.has_issues) + int(repo.has_wiki) - int(repo.fork) +\
                 np.log(star_count + 1) + np.log(fork_count + 1) + np.log(contributor_count + 1) +\
                 np.log(watchers_count + 1) - np.log(open_issues + 1) + np.log(upd_timestamp + 1)
        rating = (rating - LOWER_BOUND) / (UPPER_BOUND - LOWER_BOUND)
        rating = round(rating * 5, 2)

        if rating > 5:
            rating = 5
        elif rating < 0:
            rating = 0

        return rating

    except GithubException as error:

        if error.status == 404:
            return None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo  = github_client.get_repo(repository_name)

                star_count        = repo.stargazers_count
                fork_count        = repo.forks_count
                contributor_count = repo.get_contributors().totalCount
                watchers_count    = repo.subscribers_count
                open_issues       = repo.get_issues(state = 'open').totalCount

                updated_timestamp = repo.updated_at
                upd_timestamp = (updated_timestamp - datetime.strptime(TIMESTAMP_LOWER_BOUND, '%Y-%m-%d %H:%M:%S')).days

                has_pages = 0
                for branch in repo.get_branches():
                    if branch.name == "gh-pages":
                        has_pages = 1

                        break

                rating = has_pages + int(repo.has_issues) + int(repo.has_wiki) - int(repo.fork) +\
                         np.log(star_count + 1) + np.log(fork_count + 1) + np.log(contributor_count + 1) +\
                         np.log(watchers_count + 1) - np.log(open_issues + 1) + np.log(upd_timestamp + 1)
                rating = (rating - LOWER_BOUND) / (UPPER_BOUND - LOWER_BOUND)
                rating = round(rating * 5, 2)

                if rating > 5:
                    rating = 5
                elif rating < 0:
                    rating = 0

                return rating

            except GithubException as error:
                return None


def get_stars_count_timeseries(dataframe, github_client, repository_name):
    '''
    Returns the Stars Count Timeseries for a given repository
    '''

    # get the historical data
    timeseries = dataframe[dataframe["Name with Owner"] == repository_name]["Stars Count_1"].values
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Stars Count_2"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Stars Count_3"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Stars Count_4"].values)

    try:
        # try to get the latest value from the repository via the github api
        stars_count = _get_stars_count(github_client, repository_name)

        if stars_count is not None:
            timeseries = np.append(timeseries, stars_count)

    # most likely due to a socket timeout caused by running out of github api calls
    except: pass

    return timeseries


def get_forks_count_timeseries(dataframe, github_client, repository_name):
    '''
    Returns the Forks Count Timeseries for a given repository
    '''

    # get the historical data
    timeseries = dataframe[dataframe["Name with Owner"] == repository_name]["Forks Count_1"].values
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Forks Count_2"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Forks Count_3"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Forks Count_4"].values)

    try:
        # try to get the latest value from the repository via the github api
        forks_count = _get_forks_count(github_client, repository_name)

        if forks_count is not None:
            timeseries = np.append(timeseries, forks_count)

    # most likely due to a socket timeout caused by running out of github api calls
    except: pass

    return timeseries


def get_watchers_count_timeseries(dataframe, github_client, repository_name):
    '''
    Returns the Watchers Count Timeseries for a given repository
    '''

    # get the historical data
    timeseries = dataframe[dataframe["Name with Owner"] == repository_name]["Watchers Count_1"].values
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Watchers Count_2"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Watchers Count_3"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Watchers Count_4"].values)

    try:
        # try to get the latest value from the repository via the github api
        watchers_count = _get_watchers_count(github_client, repository_name)

        if watchers_count is not None:
            timeseries = np.append(timeseries, watchers_count)

    # most likely due to a socket timeout caused by running out of github api calls
    except: pass

    return timeseries


def get_contributors_count_timeseries(dataframe, github_client, repository_name):
    '''
    Returns the Contributors Count Timeseries for a given repository
    '''

    # get the historical data
    timeseries = dataframe[dataframe["Name with Owner"] == repository_name]["Contributors Count_1"].values
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Contributors Count_2"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Contributors Count_3"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Contributors Count_4"].values)

    try:
        # try to get the latest value from the repository via the github api
        contributors_count = _get_contributors_count(github_client, repository_name)

        if contributors_count is not None:
            timeseries = np.append(timeseries, contributors_count)

    # most likely due to a socket timeout caused by running out of github api calls
    except: pass

    return timeseries


def get_rating_timeseries(dataframe, github_client, repository_name):
    '''
    Returns the Rating Timeseries for a given repository
    '''

    # get the historical data
    timeseries = dataframe[dataframe["Name with Owner"] == repository_name]["Rating_1"].values
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Rating_2"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Rating_3"].values)
    timeseries = np.append(timeseries,
                           dataframe[dataframe["Name with Owner"] == repository_name]["Rating_4"].values)

    try:
        # try to get the latest value from the repository via the github api
        rating = _get_rating(github_client, repository_name)

        if rating is not None:
            timeseries = np.append(timeseries, rating)

    # most likely due to a socket timeout caused by running out of github api calls
    except: pass

    return timeseries


def get_issues_timestamps(github_client, repository_name, max_open_issues = 200, max_closed_issues = 200):
    '''
    Returns:
        - open issue create timestamps for the specified repository
        - lower bound of number of open issues to be plotted
        - total number of open issues for that repository(higher bound of number of open issues to be plotted)
        - average daily number of open issues

        - closed issue closed timestamps for the specified repository
        - lower bound of number of closed issues to be plotted
        - total number of closed issues for the repository
        - average daily number of closed issues

    max_open_issues: maximum number of entries that shall be returned(if the repository has fewer
                     open issues than all the available ones will be returned)
    max_closed_issues: maximum number of entries that shall be returned(if the repository has fewer
                       closed issues than all the available ones will be returned)
    '''

    try:
        repo = github_client.get_repo(repository_name)

        open_issues           = repo.get_issues(state = 'open')
        number_of_open_issues = open_issues.totalCount

        closed_issues           = repo.get_issues(state = 'closed')
        number_of_closed_issues = closed_issues.totalCount

        # get the open issues timestamps (creation time)
        counter_open = 0
        open_issues_timestamps = []

        for issue in open_issues:
            open_issues_timestamps.append(issue.created_at)
            counter_open += 1

            if counter_open == max_open_issues:
                break

        # the open issues are given from newer to older so we invert them to make chronological plotting more facile
        open_issues_timestamps = open_issues_timestamps[::-1]
        open_issues_timestamps = np.array(open_issues_timestamps)
        open_issues_timestamps.sort()

        lower_open = number_of_open_issues - len(open_issues_timestamps) + 1

        # get the average number of issues opened per day
        try:
            average_open = len(open_issues_timestamps) / ((open_issues_timestamps[-1] - open_issues_timestamps[0]).days)
        except:
            average_open = len(open_issues_timestamps)

        # get the closed issues timestamps (closure time)
        counter_closed = 0
        closed_issues_timestamps = []

        for issue in closed_issues:
            closed_issues_timestamps.append(issue.created_at)
            counter_closed += 1

            if counter_closed == max_closed_issues:
                break

        # the closed issues are given from newer to older so we invert them to make chronological plotting more facile
        closed_issues_timestamps = closed_issues_timestamps[::-1]
        closed_issues_timestamps = np.array(closed_issues_timestamps)
        closed_issues_timestamps.sort()

        lower_closed = number_of_closed_issues - len(closed_issues_timestamps) + 1

        # get the average number of closed issues per day
        try:
            average_closed = len(closed_issues_timestamps) / ((closed_issues_timestamps[-1] - closed_issues_timestamps[0]).days)
        except:
            average_closed = len(closed_issues_timestamps)

        return open_issues_timestamps, lower_open, number_of_open_issues, average_open, closed_issues_timestamps, lower_closed, number_of_closed_issues, average_closed

    except GithubException as error:

        if error.status == 404:
            return None, None, None, None, None, None, None, None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo = github_client.get_repo(repository_name)

                open_issues           = repo.get_issues(state = 'open')
                number_of_open_issues = open_issues.totalCount

                closed_issues           = repo.get_issues(state = 'closed')
                number_of_closed_issues = closed_issues.totalCount

                # get the open issues timestamps (creation time)
                counter_open = 0
                open_issues_timestamps = []

                for issue in open_issues:
                    open_issues_timestamps.append(issue.created_at)
                    counter_open += 1

                    if counter_open == max_open_issues:
                        break

                # the open issues are given from newer to older so we invert them to make chronological plotting more facile
                open_issues_timestamps = open_issues_timestamps[::-1]
                open_issues_timestamps = np.array(open_issues_timestamps)
                open_issues_timestamps.sort()

                lower_open = number_of_open_issues - len(open_issues_timestamps) + 1

                # get the average number of issues opened per day
                try:
                    average_open = len(open_issues_timestamps) / ((open_issues_timestamps[-1] - open_issues_timestamps[0]).days)
                except:
                    average_open = len(open_issues_timestamps)

                # get the closed issues timestamps (closure time)
                counter_closed = 0
                closed_issues_timestamps = []

                for issue in closed_issues:
                    closed_issues_timestamps.append(issue.created_at)
                    counter_closed += 1

                    if counter_closed == max_closed_issues:
                        break

                # the closed issues are given from newer to older so we invert them to make chronological plotting more facile
                closed_issues_timestamps = closed_issues_timestamps[::-1]
                closed_issues_timestamps = np.array(closed_issues_timestamps)
                closed_issues_timestamps.sort()

                lower_closed = number_of_closed_issues - len(closed_issues_timestamps) + 1

                # get the average number of closed issues per day
                try:
                    average_closed = len(closed_issues_timestamps) / ((closed_issues_timestamps[-1] - closed_issues_timestamps[0]).days)
                except:
                    average_closed = len(closed_issues_timestamps)

                return open_issues_timestamps, lower_open, number_of_open_issues, average_open, closed_issues_timestamps, lower_closed, number_of_closed_issues, average_closed


            # for when the api server didn't recover, or for when a socket timeout occurs
            # or for 409: 'Git Repository is empty'
            except:
                return None, None, None, None, None, None, None, None


def get_commits_timestamps(github_client, repository_name, max_commit_number = 200):
    '''
    Returns:
        - commit timestamps for the specified repository
        - lower bound of number of commits to be plotted
        - total number of commits for that repository(higher bound of number of commits to be plotted)
    max_commit_number: maximum number of entries that shall be returned(if the repository has fewer
                       commits than all the available ones will be returned)
    '''

    try:
        repo = github_client.get_repo(repository_name)

        commits           = repo.get_commits()
        number_of_commits = commits.totalCount

        # get the commit timestamps
        counter = 0
        commits_timestamps = []

        for commit in commits:
            if commit.commit is not None:
                commits_timestamps.append(commit.commit.author.date)
                counter += 1

                if counter == max_commit_number:
                    break

        # the commits are given from newer to older so we invert them to make chronological plotting more facile
        commits_timestamps = commits_timestamps[::-1]
        commits_timestamps = np.array(commits_timestamps)
        commits_timestamps.sort()

        lower_bound = number_of_commits - len(commits_timestamps) + 1

        return commits_timestamps, lower_bound, number_of_commits

    except GithubException as error:

        if error.status == 404:
            return None, None, None

        # most likely a 502
        else:
            time.sleep(1)

            try:
                repo = github_client.get_repo(repository_name)

                commits           = repo.get_commits()
                number_of_commits = commits.totalCount

                # get the commit timestamps
                counter = 0
                commits_timestamps = []

                for commit in commits:
                    if commit.commit is not None:
                        commits_timestamps.append(commit.commit.author.date)
                        counter += 1

                        if counter == max_commit_number:
                            break

                # the commits are given from newer to older so we invert them
                # to make chronological plotting more facile
                commits_timestamps = commits_timestamps[::-1]
                commits_timestamps = np.array(commits_timestamps)
                commits_timestamps.sort()

                lower_bound = number_of_commits - len(commits_timestamps) + 1

                return commits_timestamps, lower_bound, number_of_commits

            # for when the api server didn't recover, or for when a socket timeout occurs
            # or for 409: 'Git Repository is empty'
            except:
                return None, None, None
