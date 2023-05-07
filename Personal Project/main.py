import pandas as pd
import requests
repos = {"AffectiveTweets":"felipebravom",
                "CoreNLP":"stanfordnlp",
                "DataCleaner":"datacleaner",
                "deeplearning4j":"deeplearning4j",
                "elki":"elki-project",
                "Foundry":"algorithmfoundry",
                "grobid":"kermitt2",
                "jenetics":"jenetics",
                "knime-core":"knime",
                "liblevenshtein-java":"universal-automata",
                "mahout":"apache",
                "Mallet":"mimno",
                "moa":"Waikato",
                "modernmt":"modernmt",
                "Mutters":"rabidgremlin",
                "neo4j-nlp":"graphaware",
                "neuronix":"CElabls",
                "smile":"haifengl",
                "submarine":"apache",
                "tablesaw":"jtablesaw",
                "Trainable_Segmentation":"fiji",
                "weka-trunk":"Waikato",
                "vespa":"vespa-engine",
                "elasticsearch":"elastic",
                "DigitRecognizer":"klevis",
                "htm.java":"numenta"
}

def get_affected_file_number(row):
    headers = {
        'Authorization' : 'token Your Token Here'
    }
    url = f"https://api.github.com/repos/{repos[row['Subject']] + '/' + row['Subject']}/commits/{row['CommitId']}"
    r = requests.get(url, headers=headers)
    commit = r.json()
    try:
        files = len(commit["files"])
    except:
        files = 0
        print(r.json())
        print(url)
    return files


if __name__ == '__main__':




    headers = {
        'Authorization': 'token Your Token Here'
    }
    # checking the GitHub API rate limit
    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    print(response.text)
    print(response)

    df = pd.read_csv("commits - unique_refactoring_commits.csv")
    #print(df["Subject"])
    links = []
    names = []
    number_of_files = []
    for index, row in df.iterrows():
        link = "https://github.com/" + repos[row["Subject"]] + "/" + row["Subject"] + "/commit/" + row["CommitId"]
        links.append(link)
        names.append(repos[row["Subject"]] + "/" + row["Subject"])
        number_of_files.append(get_affected_file_number(row))


    df['link'] = links
    df['Subject'] = names
    df['#affected_files'] = number_of_files
    print(df)
    df.to_csv("commits_affected_files.csv")
