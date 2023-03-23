import os
import pandas as pd
import numpy as np
from itertools import combinations
from fuzzywuzzy import fuzz

from scipy import stats

# define a function to compute the fuzzy matching score
def fuzzy_match(first, second):
    return fuzz.token_sort_ratio(first, second)

#define function to get PID
def getPID(first_name, last_name, dob):
    return first_name.str[:3] + last_name.str[:1] + pd.to_datetime(dob).dt.strftime('%m%d%y')

# define a custom function to aggregate each group and create a new PID column
def aggregate_by_name(group):
    mode_DOB = group['dob'].mean()
    mode_SEX = group['sex'].sum()
    pid = group['first_name'].iloc[0] + group['last_name'].iloc[0] + mode_DOB
    return pd.DataFrame({'DOB': [id], 'DOB': [mode_DOB], 'SEX': [mode_SEX]})

def remove_for_each(group):
    # create a new column with the fuzzy matching score against each row
    # grouped_scores  = grouped['DOB'].apply(lambda x: [fuzzy_match(x, y) for y in grouped['DOB']])
    # compute pairwise fuzzy scores between dates of birth
    scores = [[fuzzy_match(df['DOB'][i], df['DOB'][j]) for j in range(len(df))] for i in range(len(df))]
    print(scores)

    # compute confidence matrix from fuzzy scores
    confidences = [[max(scores[i][j], scores[j][i]) if i != j else 100 for j in range(len(group))] for i in range(len(group))]    
    for row in confidences:
        for element in row:
            print(element, end=' ')
        print()

    # remove duplicates using confidence matrix
    duplicates = set()
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            if confidences[i][j] >= 90:
                duplicates.add(min(i, j))

    # create new DataFrame without duplicates
    df_no_duplicates = df.drop(duplicates)

    # print new DataFrame
    print(df_no_duplicates)


    # print the result
    return df_no_duplicates



df = pd.read_csv('test.csv', header=0, na_values="0",encoding='windows-1254')

# Remove extra spaces and capitalize FIRST_NAME
df['LAST_NAME'] = df['LAST_NAME'].str.strip().str.title()
df['FIRST_NAME'] = df['FIRST_NAME'].str.strip().str.title()

# group by name
grouped = df.groupby(['LAST_NAME', 'FIRST_NAME'])
removed = pd.concat([remove_for_each(g) for _, g in grouped], axis=0)


print(removed)


df.to_csv('removed.csv')