import subprocess
import pandas as pd
import json

### code for mining refactorings using the RefactoringMiner tool
### nneds to have the latest RefactoringMiner (v2.4) extracted in the same directory
### a valid GitHub aoken must be provided in the same directory in the form of
    ### OAuthToken= ''Your token''
    ### in a file named github-oauth.properties
### the links to commits stored in the file gh_links_60.csv must also be in the same directory

###outputs all the refactorings in a csv file format named "refactorings.csv"


def mine_refactorings():
    refactoring_miner_path = "./bin/RefactoringMiner"

    df = pd.read_csv("gh_links_60.csv")
    df["repo"] = df["links"].apply(lambda s: s[19:s.find("/commit")])
    df["sha"] = df["links"].apply(lambda s: s[s.find("/commit")+8:])


    print(df[["repo", "sha"]])
    commits = df[["repo", "sha"]]


    for index, commit in commits.iterrows():
        print(commit)
        command = [refactoring_miner_path, "-gc", commit["repo"], commit["sha"], "360", "-json",  "out_"+str(index)+".json"]
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True)
        output = subprocess.check_output(command)
        # Print the output
        print(output.decode('utf-8'))
        return

def parse_refactorings():

    refactorings = []
    for i in range (0,60):
        f = open("out_"+str(i)+".json")
        data = json.load(f)
        print(type(data))

        refactoring = {}
        refactoring["repo"] = data["commits"][0]["repository"]
        refactoring["sha"] = data["commits"][0]["sha1"]
        for r in data["commits"][0]["refactorings"]:
            if r["type"] in refactoring:
                refactoring[r["type"]] = refactoring[r["type"]]+1
            else:
                refactoring[r["type"]] = 1
        refactorings.append(refactoring)
        df = pd.DataFrame(refactorings)
        df.to_csv("refactorings.csv")
    return

if __name__ == '__main__':
    mine_refactorings()
    parse_refactorings()
