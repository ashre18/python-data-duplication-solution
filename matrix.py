

# import pandas as pd
# from fuzzywuzzy import fuzz

# # Sample data
# data = {
#     'full_name': ['John Doe', 'John Doe', 'Jane Smith', 'Jane Smith', 'Jane Smith', 'Bob Johnson'],
#     'DOB': ['01/01/1990', '01/01/1995', '02/02/1985', '02/02/1986', '02/02/1987', '03/03/2000'],
#     'sales': [100, 200, 150, 50, 100, 300]
# }
# df = pd.DataFrame(data)

# # Group by full name
# grouped = df.groupby('full_name')

# # Merge rows with similar dates of birth
# for name, group in grouped:
#     dob_scores = [fuzz.token_sort_ratio(group.iloc[i]['DOB'], group.iloc[j]['DOB']) for i in range(len(group)) for j in range(i+1, len(group))]
#     for i, score in enumerate(dob_scores):
#         if score >= 90:
#             # Merge rows with similar dates of birth
#             row1 = group.iloc[i // (len(group)-1)]
#             row2 = group.iloc[i % (len(group)-1) + 1]
#             merged_row = row1.copy()
#             merged_row['DOB'] = row1['DOB'] if len(row1['DOB']) == 10 else row2['DOB']
#             merged_row['sales'] = row1['sales'] + row2['sales']
#             group = group.drop([row1.name, row2.name])
#             group = group.append(merged_row)
#             group = group.reset_index(drop=True)
#     grouped.groups[name] = group.index

# # Combine all groups back into a single dataframe
# df_new = pd.concat([grouped.get_group(name) for name in grouped.groups], ignore_index=True)

from fuzzywuzzy import fuzz
import pandas as pd

# Load data from CSV file
df = pd.read_csv('test.csv', delimiter='\t')

# Define a function to calculate the similarity between two records
def calculate_similarity(row1, row2):
    fields = ["LAST_NAME", "FIRST_NAME", "DOB", "SEX"]
    score = 0
    for field in fields:
        score += fuzz.token_sort_ratio(str(row1[field]), str(row2[field]))
    return score

# Identify fuzzy duplicates and remove them
threshold = 80 # set the minimum similarity threshold
duplicates = set()
for i, row1 in df.iterrows():
    for j, row2 in df.iterrows():
        if i != j and calculate_similarity(row1, row2) >= threshold:
            duplicates.add((i, j))

df.drop(index=[j for i, j in duplicates], inplace=True)

# Save the result to a new CSV file
df.to_csv('data_without_duplicates.csv', sep='\t', index=False)
