#!/bin/python

import random
import csv

def extract(input_file, output_file="", selected_columns = []):
    """Function that extracts wanted data from a csv file. Can output to another csv file or return a list of the selected data"""
    with open(input_file) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        
        # We prompt user for columns if none are provided
        if len(selected_columns) == 0:
            # We print the header row with the associated indices
            for i in range(0,len(header_row)):
                print(str(i) + ": " + header_row[i])

            # The user is prompted to select the columsn he wants to extract
            selection = input("Enter the index of a column you wish to extract, enter anything that is not a number when done: ")
    
            # We keep asking as long as the input is valid
            while selection.isdigit():
                if int(selection) >= len(header_row):
                    print("This index is out of bounds, make a valid selection")

                else:
                    selected_columns.append(int(selection))
                    selection = input("Enter the index of a column you wish to extract, enter anything that is not a number when done: ")

        # If an output file is provided, we write the selected columns to it (only supports csv)
        if output_file != "":
            with open(output_file, 'w') as outfile:
                writer = csv.writer(outfile)
            
                new_row = []
                for i in selected_columns:
                    new_row.append(header_row[i])
                writer.writerow(new_row)

                for row in reader:
                    new_row.clear()
                    for i in selected_columns:
                        new_row.append(row[i])
                    writer.writerow(new_row)

        # If no file is specified, we return the output in a dictionary
        else:
            result = []
            
            # We build a dictionary for each row that we put into a list
            row_dict = {}
            for row in reader:
                for i in selected_columns:
                    row_dict[header_row[i]] = row[i]
                result.append(row_dict.copy())
                row_dict.clear()

            return result

# Splits a list of data into two lists in a ratio of (fraction):(1-fraction) randomly
def data_split(data, fraction):
    """Splits a list of data into two lists (returned within a single list) in a ratio of (fraction):(1-fraction) and popoulates each list randomly"""
    # Since shuffle affects the list and we want to keep the original list intact, we copy the list
    shf_data = data.copy()
    shuffle(shf_data)
    
    # We will return a list containing 2 lists
    result = []

    # This is the first list of the result, containing the training data
    train_data = []
    train_size = fraction * len(shf_data)
    for row in shf_data[:train_size]:
        train_data.append(row.copy())
    result.append(train_data.copy())

    # This is the second list of the result, containing the testing data
    test_data = []
    for row in shf_data[train_size:]:
        test_data.append(row.copy())
    result.append(test_data.copy())

    return result
