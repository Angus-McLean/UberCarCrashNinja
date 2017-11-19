#!/bin/python
from extract_mod import extract

def count_instances(file_name, column):
    """Counts the instances of the different keys in one column of a data set"""
    rows = extract(file_name, selected_columns=column)

    counter = {}

    for row in rows:
        if next(iter(row.values())) in counter:
            counter[next(iter(row.values()))] = counter[next(iter(row.values()))] + 1
        else:
            counter[next(iter(row.values()))] = 1

    for k in counter:
        print(k + ": " + str(counter[k]))
