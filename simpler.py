import pandas as pd
from fuzzywuzzy import fuzz

df = pd.read_csv('test.csv')
print(df)
groups = df.groupby(['LAST_NAME', 'FIRST_NAME'])
def merge_similar_dates(group):
    threshold = 80
    rows_to_drop = []
    for i, row in group.iterrows():
        for j, other_row in group.iterrows():
            if i != j and j not in rows_to_drop and i not in rows_to_drop:
                ratio = fuzz.token_sort_ratio(row['DOB'], other_row['DOB'])
                print(ratio)
                if ratio >= threshold:
                    group.at[i, 'ACCESSIONS'] += other_row['ACCESSIONS']
                    rows_to_drop.append(j)
    group = group.drop(rows_to_drop)
    return group

merged_df = groups.apply(merge_similar_dates).reset_index(drop=True)
print(merged_df)