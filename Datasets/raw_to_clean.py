from typing import List
import csv


def extract_wanted_column(file_name: str, first_column_name: str, second_column_name) -> List[List[str]]:
    """Return two lists owhich contain the essential columns from the input csv files for further processing.

    Precondition:
        - filepath refers to a csv file with 2 or more columns
        - first and second column strings are present in the csv header
    """
    each_row_req_1 = []
    each_row_req_2 = []

    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        req_i = req_j = 0

        for i in range(len(header)):
            for j in range(len(header)):
                if header[i] == first_column_name and header[j] == second_column_name:
                    req_i = i
                    req_j = j

        for row in reader:
            each_row_req_1.append(row[req_i])
            each_row_req_2.append(row[req_j])

    return [each_row_req_1, each_row_req_2]
