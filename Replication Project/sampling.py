import pandas as pd

###script for stratified sampling with a 0.33 sampling probability given a file of
### refactorings called "all_refactorings.csv" in the same directory
### in ehich the refactorings have column named "project" that determines the
### project on GitHub that they belong to


df = pd.read_csv("all_refactorings.csv")
#print((df['project'].value_counts()) / len(df) * 100)
print((df['project'].value_counts()))

sample = df.groupby('project', group_keys=False).apply(lambda x: x.sample(frac=0.33))
print(sample)
print((sample['project'].value_counts()))
#print((sample['project'].value_counts()) / len(sample) * 100)
sample.to_csv("sample.csv")
