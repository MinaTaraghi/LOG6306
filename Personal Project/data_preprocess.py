import pandas as pd

def data_preprocessor():
    df = pd.read_csv("commits-Final-edited.csv")
    df.drop(["og_idx"], axis = "columns", inplace= True)
    #print(df)

    return df

if __name__ == '__main__':
    df = data_preprocessor()