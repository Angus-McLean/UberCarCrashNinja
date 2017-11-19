#!/bin/python

import csv
import sys

if len(sys.argv) < 2:
    print("Usage: extract.py /path/to/input_file.csv [/path/to/output_file.csv]")
    print("       If no output file is specified, the output is sent to stdout")

# Put in the path to the file you want in the arguments
filepath = sys.argv[1]

with open(filepath) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    
    # We print the header row with the associated indices
    for i in range(0,len(header_row)):
        print(str(i) + ": " + header_row[i])

    # The user is prompted to select the columsn he wants to extract
    selected_columns = []
    selection = input("Enter the index of a column you wish to extract, enter anything that is not a number when done: ")
    
    # We keep asking as long as the input is valid
    while selection.isdigit():
        if int(selection) >= len(header_row):
            print("This index is out of bounds, make a valid selection")

        else:
            selected_columns.append(int(selection))
            selection = input("Enter the index of a column you wish to extract, enter anything that is not a number when done: ")

    # If an output file is provided, we write the selected columns to it (only supports csv)
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w') as outfile:
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

    # If no file is specified, we send the output to stdout
    else:
        # We print all the selected headers
        for i in selected_columns:
            print(header_row[i], end=' ')
        print('')

        # And all the data associated with these rows
        for row in reader:
            for i in selected_columns:
                print(row[i], end=' ')
            print('')

