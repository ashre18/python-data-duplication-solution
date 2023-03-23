import pandas as pd
from itertools import combinations
from fuzzywuzzy import fuzz

# define function to compute fuzzy scores between dates of birth
def compute_fuzzy_scores(dob_pairs):
    fuzzy_scores = []
    for dob_pair in dob_pairs:
        fuzzy_score = fuzz.token_set_ratio(dob_pair[0], dob_pair[1])
        fuzzy_scores.append(fuzzy_score)
    print(fuzzy_scores)
    return fuzzy_scores

df = pd.read_csv('test.csv', header=0, na_values="0",encoding='windows-1254')


# extract pairs of dates of birth for each first and last name, compute fuzzy scores, and remove duplicates based on threshold
df_duplicates_removed = pd.concat([g.drop_duplicates(subset=['DOB'], keep=False) for _, g in df.groupby(['FIRST_NAME', 'LAST_NAME'])], axis=0)
dob_pairs = list(combinations(df_duplicates_removed['DOB'], 2))
fuzzy_scores = compute_fuzzy_scores(dob_pairs)
duplicates_to_remove = set()
for i, dob_pair in enumerate(dob_pairs):
    if fuzzy_scores[i] > 90:
        duplicates_to_remove.add(dob_pair[1])
df_final = df_duplicates_removed[~df_duplicates_removed['DOB'].isin(duplicates_to_remove)]

# print the resulting DataFrame
print(df_final)
