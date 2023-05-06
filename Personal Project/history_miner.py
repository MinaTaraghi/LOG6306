import pandas as pd
from data_preprocess import data_preprocessor
import requests
from urllib.parse import parse_qs, urlparse
import re
from dateutil import parser, relativedelta
import datetime

headers = {
        'Authorization': 'token Your Token Here'
    }


def get_commit_date(name, commit):

    url = f"https://api.github.com/repos/{name}/commits/{commit}"
    r = requests.get(url, headers=headers)
    commit = r.json()
    return commit["commit"]["committer"]["date"]


def time_diff(first, last):
    # returns the time difference in months between two commit dates
    diff = relativedelta.relativedelta(last, first)
    return diff.months + 12 * diff.years + 1


def parse_date(date):
    # returns the timedate object of a commit (in a json response)
    p = parser.parse(date)
    return p


def get_bugs(rf_date, bugs):
    bef_bugs , aft_bugs = len(bugs), 0
    index = -1
    print("total number of bugs: ", len(bugs))
    print("refactoring date ", rf_date)
    for bug in bugs:
        index += 1
        bug_date = parse_date(bug["commit"]["committer"]["date"])
        print(f"bug {index} date ", bug_date)
        if rf_date >= bug_date:
            aft_bugs = index
            bef_bugs = len(bugs) - index
            print("rf is here")
            break


    print("before bugs ", bef_bugs)
    print("after bugs ", aft_bugs)
    return bef_bugs, aft_bugs

def get_timeframe_commits(name, first, last, RF):
    before_rf_all = get_commit_counts(name, first, RF)
    after_rf_all  = get_commit_counts(name, RF, last)
    return before_rf_all, after_rf_all


def get_commit_counts(name, begin, end):
    url = f"https://api.github.com/repos/{name}/commits?since={begin}&until={end}&per_page=1"
    print(url)
    r = requests.get(url, headers=headers)
    links = r.links
    try:
        rel_last_link_url = urlparse(links["last"]["url"])
        rel_last_link_url_args = parse_qs(rel_last_link_url.query)
        rel_last_link_url_page_arg = rel_last_link_url_args['page'][0]
        commits_count = int(rel_last_link_url_page_arg)

    except:
        commits_count = 0.0000001
        print("no commits found for ", name)
    return commits_count


def get_commits(name, path):
    commits = []
    kw_commits = []
    regex = r"\bbug"
    f = re.IGNORECASE
    counter = 0
    page = 1
    while True:
        try:
            url = f"https://api.github.com/repos/{name}/commits?path=/{path}&per_page=100&page={page}"
            r = requests.get(url, headers=headers)
            for commit in r.json():
                if re.search(regex, commit["commit"]["message"], flags=f):
                    kw_commits.append(commit)
                    counter += 1
            commits = commits+ r.json()
            links = r.links
            try:
                rel_last_link_url = urlparse(links["next"]["url"])
                page += 1
            except:
                break
        except:
            print(name, path)
            break
    return commits, kw_commits


def commit_miner(name, path):
    url = f"https://api.github.com/repos/{name}/commits?path=/{path}&page=1"
    r = requests.get(url, headers=headers)
    history = r.json()
    return history


if __name__ == '__main__':

    # checking the GitHub API rate limit
    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    print(response.text)
    print(response)

    df = data_preprocessor()

    list_output = []

    for index, row in df.iterrows():
        his, bugs = get_commits(row["Subject"], row['affected_class'])

        rf_index = 0
        for commit in his:
            long_sha = commit["sha"]
            if long_sha.startswith(row["CommitId"]):
                break
            rf_index += 1

        class_after = rf_index
        class_before = len(his) - rf_index-1

        row['cls_before'] = class_before
        row['cls_after'] = class_after

        first_commit_date = his[-1]['commit']['committer']['date']
        last_commit_date = his[0]['commit']['committer']['date']

        row['first_commit'] = first_commit_date
        row['last_commit'] = last_commit_date

        RF_date = get_commit_date(row["Subject"], row["CommitId"])
        RF_date = parse_date(RF_date)
        RF_date_str = RF_date.isoformat()[:19] + "Z"

        row['RF_date'] = RF_date_str

        all_before, all_after = get_timeframe_commits(row['Subject'], first_commit_date, last_commit_date, RF_date_str)
        '''print(all_before+all_after)
        print(get_commit_counts(row["Subject"], first_commit_date, last_commit_date))'''

        row['all_before'] = all_before
        row['all_after'] = all_after

        change_before = round(class_before/max(all_before, 1), 4)
        change_after  = round(class_after/max(all_after, 1), 4)
        row['change_ratio_before'] = change_before
        row['change_ratoi_after'] = change_after

        ratio_change = len(his)/(all_after+all_before)

        ratio_change_before = round((class_before / max(all_before, 1)) / ratio_change, 4)
        ratio_change_afetr =  round((class_after / max(all_after, 1)) / ratio_change, 4)

        row['2nd_ratio_before'] = ratio_change_before
        row['2nd_ratio_after'] = ratio_change_afetr


        bugs_before, bugs_after = get_bugs(RF_date, bugs)

        row['bugs_before'] = bugs_before
        row['bugs_after'] = bugs_after
        bug_ratio_before = round(bugs_before / max(class_before, 1), 4)
        bug_ratio_after = round(bugs_after / max(class_after, 1), 4)

        row['bugs_ratio_before'] = bug_ratio_before
        row['bugs_ratio_after'] = bug_ratio_after
        list_output.append(row)

    df_out = pd.DataFrame(list_output)
    df_out.to_csv("RF_stats.csv")
