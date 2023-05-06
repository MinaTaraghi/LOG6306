from scipy.stats import shapiro, mannwhitneyu
import pandas as pd
from cliffs_delta import cliffs_delta

def shapiro_wilk_test(data):
    stat, p = shapiro(data)

    # Interpret the test result
    alpha = 0.05
    if p > alpha:
        return("Sample is likely normally distributed (fail to reject H0)")
    else:
        return("Sample is not normally distributed (reject H0)")

def mann_whitney(sample1, sample2):
    # performing Mann-Whitney U Test
    U1, p = mannwhitneyu(sample1, sample2, alternative = 'greater')
    # Interpret the test result
    alpha = 0.05
    if p < alpha:
        return("The one-tailed Mann-Whitney U test indicates that sample1 is greater than sample2. U1 and p_value: ",round(U1,4), round(p,4))
    else:
        return("The one-tailed Mann-Whitney U test does not indicate that sample1 is greater than sample2. U1 and p_value: ",round(U1,4),  round(p,4))

def cliffsdelta(sample1, sample2):
    #measuring the effect size using cliff's delta
    return cliffs_delta(df['bugs_ratio_before'], df['bugs_ratio_after'])


if __name__ == '__main__':
    df = pd.read_csv("RF_stats.csv")
    df = df[df["In ML-related code?"]==True]
    print(df)

    ####################### RQ1 #########################################
    print('####################### RQ1 #########################################')
    print("normal change before?: ")
    print(shapiro_wilk_test(df['change_ratio_before']))
    print("normal change after?: ")
    print(shapiro_wilk_test(df['change_ratoi_after']))

    print("chnage difference: ")
    print(mann_whitney(df['change_ratio_before'],df['change_ratoi_after']))

    print("change effect size:")
    cliff1= cliffs_delta(df['change_ratio_before'],df['change_ratoi_after'])
    print(round(cliff1[0],4),cliff1[1])
    ####################### RQ2 #########################################
    print('####################### RQ2 #########################################')
    print("normal bug before?: ")
    print(shapiro_wilk_test(df['bugs_ratio_before']))
    print("normal bug after?: ")
    print(shapiro_wilk_test(df['bugs_ratio_after']))

    print("bug difference: ")
    print(mann_whitney(df['bugs_ratio_before'], df['bugs_ratio_after']))

    print("bug effect size:")
    cliff = cliffsdelta(df['bugs_ratio_before'], df['bugs_ratio_after'])
    print(round(cliff[0],4),cliff[1])




    #############################################################
    df['change_ratio_after-before'] = df["change_ratoi_after"]-df["change_ratio_before"]

    df['bug_ratio_after-before'] = df["bugs_ratio_after"]-df["bugs_ratio_before"]

    ml = df[df['Is ML-specific refactoring category?']==True]

    nml = df[df['Is ML-specific refactoring category?'] == False]
    ####################### RQ3 #########################################
    print('####################### RQ3 #########################################')
    print("normal change ml?: ")
    print(shapiro_wilk_test(ml['change_ratio_after-before']))
    print("normal change nml?: ")
    print(shapiro_wilk_test(nml['change_ratio_after-before']))

    print("change ml/nml difference: ")
    print(mann_whitney(nml['change_ratio_after-before'], ml['change_ratio_after-before']))

    print("change ml/nml effect size:")
    cliff = cliffsdelta(nml['change_ratio_after-before'], ml['change_ratio_after-before'])
    print(round(cliff[0], 4), cliff[1])

    ####################### RQ4 #########################################
    print('####################### RQ4 #########################################')
    print("normal bug ml?: ")
    print(shapiro_wilk_test(ml['bug_ratio_after-before']))
    print("normal bug nml?: ")
    print(shapiro_wilk_test(nml['bug_ratio_after-before']))

    print("bug ml/nml difference: ")
    print(mann_whitney(nml['bug_ratio_after-before'], ml['bug_ratio_after-before']))

    print("bug ml/nml effect size:")
    cliff = cliffsdelta(nml['bug_ratio_after-before'], ml['bug_ratio_after-before'])
    print(round(cliff[0], 4), cliff[1])



