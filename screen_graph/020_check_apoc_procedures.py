import os

import pandas as pd

print(os.getcwd())


# load data from csv 'data/granular_relationships.txt'
df = pd.read_csv("data/granular_relationships.txt")

# get Source labels from df and convert to list
source_labels = df["Source"].tolist()
# split each label into list of words using '|' as separator
source_labels = [x.split("|") for x in source_labels]
# flatten list of lists into list of words
source_labels = [item for sublist in source_labels for item in sublist]
# remove duplicates from list and sort
source_labels = sorted(list(set(source_labels)))

# get Target labels from df and convert to list
target_labels = df["Target"].tolist()
# split each label into list of words using '|' as separator
target_labels = [x.split("|") for x in target_labels]
# flatten list of lists into list of words
target_labels = [item for sublist in target_labels for item in sublist]
# remove duplicates from list and sort
target_labels = sorted(list(set(target_labels)))

# get Relationship labels from df and convert to list
relationship_labels = df["Relationship"].tolist()
# split each label into list of words using '|' as separator
relationship_labels = [x.split("|") for x in relationship_labels]
# flatten list of lists into list of words
relationship_labels = [item for sublist in relationship_labels for item in sublist]
# remove duplicates from list and sort
relationship_labels = sorted(list(set(relationship_labels)))

# find Source labels that are in any line of 'data/ot_files/apoc_procedures_ot_data.txt'
used_source_labels = []
with open("data/ot_files/apoc_procedures_ot_data.txt") as f:
    for line in f:
        for word in source_labels:
            if str(":" + word) in line:
                used_source_labels.append(word)
# remove duplicates from list and sort
used_source_labels = sorted(list(set(used_source_labels)))
print(
    f"Of {len(source_labels)} source labels, {len(used_source_labels)} are used in the OT query."
)
# subtract used labels from all labels to find unused labels
unused_source_labels = [x for x in source_labels if x not in used_source_labels]
print(f"Used source labels: {used_source_labels}")
print(f"Unused source labels: {unused_source_labels}")

# find Target labels that are in any line of 'data/ot_files/apoc_procedures_ot_data.txt'
used_target_labels = []
with open("data/ot_files/apoc_procedures_ot_data.txt") as f:
    for line in f:
        for word in target_labels:
            if str(":" + word) in line:
                used_target_labels.append(word)
# remove duplicates from list and sort
used_target_labels = sorted(list(set(used_target_labels)))
print(
    f"Of {len(target_labels)} target labels, {len(used_target_labels)} are used in the OT query."
)
# subtract used labels from all labels to find unused labels
unused_target_labels = [x for x in target_labels if x not in used_target_labels]
print(f"Used target labels: {used_target_labels}")
print(f"Unused target labels: {unused_target_labels}")

# find Relationship labels that are in any line of 'data/ot_files/apoc_procedures_ot_data.txt'
used_relationship_labels = []
with open("data/ot_files/apoc_procedures_ot_data.txt") as f:
    for line in f:
        for word in relationship_labels:
            if str(":" + word) in line:
                used_relationship_labels.append(word)
# remove duplicates from list and sort
used_relationship_labels = sorted(list(set(used_relationship_labels)))
print(
    f"Of {len(relationship_labels)} relationship labels, {len(used_relationship_labels)} are used in the OT query."
)
# subtract used labels from all labels to find unused labels
unused_relationship_labels = [
    x for x in relationship_labels if x not in used_relationship_labels
]
print(f"Used relationship labels: {used_relationship_labels}")
print(f"Unused relationship labels: {unused_relationship_labels}")
