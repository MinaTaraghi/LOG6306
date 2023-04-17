import requests
import math
import pandas as pd
from urllib.parse import parse_qs, urlparse
import re


### main script that mines the commits of the 26 projects listed in the list projects
###  parses the commits and stores all the commits that have the word "refactor"
### in them as the refactorings in a file "all_refactorings.csv"
### The statistics (#commits, #refactorig commits ) for the 26 projects
### is also stored in a file "stats.csv"

def get_commit_counts(project, headers):
    url = f"https://api.github.com/repos/{project}/commits?per_page=1"
    r = requests.get(url, headers=headers)
    links = r.links
    try:
        rel_last_link_url = urlparse(links["last"]["url"])
        rel_last_link_url_args = parse_qs(rel_last_link_url.query)
        rel_last_link_url_page_arg = rel_last_link_url_args["page"][0]
        commits_count = int(rel_last_link_url_page_arg)

    except:
        commits_count = 0
    return commits_count

def get_commits(project, headers):
    commit_count = get_commit_counts(project, headers)
    commits = []
    kw_commits = []
    print(commit_count)
    regex = r"\brefactor"
    f = re.IGNORECASE
    counter = 0
    for page in range(1, math.ceil(commit_count/100)+1):
        url = f"https://api.github.com/repos/{project}/commits?per_page=100&page={page}"
        r = requests.get(url, headers=headers)
        for commit in r.json():
            if re.search(regex, commit["commit"]["message"], flags=f):
                kw_commits.append(commit)
                counter += 1
                print(counter)
        commits= commits+ r.json()
    return commits, kw_commits

if __name__ == '__main__':
    headers = {
        'Authorization': 'Your Token here'
    }
    # checking the GitHub API rate limit
    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    print(response.text)
    print(response)


    projects = ["felipebravom/AffectiveTweets",
                "stanfordnlp/CoreNLP",
                "datacleaner/DataCleaner",
                "deeplearning4j/deeplearning4j",
                "elki-project/elki",
                "algorithmfoundry/foundry",
                "kermitt2/grobid",
                "jenetics/jenetics",
                "knime/knime-core",
                "universal-automata/liblevenshtein-java",
                "apache/mahout",
                "mimno/Mallet",
                "Waikato/moa",
                "modernmt/modernmt",
                "rabidgremlin/Mutters",
                "graphaware/neo4j-nlp",
                "CElabls/neuronix",
                "haifengl/smile",
                "apache/submarine",
                "jtablesaw/tablesaw",
                "fiji/Trainable_Segmentation",
                "Waikato/weka-trunk",
                "vespa-engine/vespa",
                "elastic/elasticsearch",
                "klevis/DigitRecognizer",
                "numenta/htm.java"
                ]
    #print(len(projects))
    stats = []
    all_refactorings =[]
    for project in projects:
        project_stats = {}
        commits, kw_commits = get_commits(project, headers)
        for commit in kw_commits:
            refactoring = {}
            refactoring["project"] = project
            refactoring["sha"] = commit["sha"]
            refactoring["message"] = commit["commit"]["message"]
            refactoring["link"] = f"https://github.com/{project}/commit/{commit['sha']}"
            all_refactorings.append(refactoring)
        print(project)
        project_stats["project_name"] = project
        print("#Commits:\t", len(commits))
        print("#keywords:\t", len(kw_commits))
        project_stats["#commits"] = len(commits)
        project_stats["#kwds"] = len(kw_commits)
        stats.append(project_stats)
        print("************************************")
    df = pd.DataFrame(stats)
    df.to_csv("stats.csv")

    df_refactorings = pd.DataFrame(all_refactorings)
    df_refactorings.to_csv("all_refactorings.csv")

