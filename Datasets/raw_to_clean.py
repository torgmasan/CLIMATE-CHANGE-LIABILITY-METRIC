from typing import List


def remove_unwanted_columns(file_name: str, remove_columns: List[int]) -> None:
    raw = open(file_name, 'r')
    raw_lines = raw.readlines()

    clean_lines = []
    for raw_line in raw_lines:
        temp_list = raw_line.split(',')
        newline_adjusted = temp_list.pop(-1).split('\n')
        temp_list.append(newline_adjusted[0])
        temp_list.append('\n')

        for column in remove_columns:
            temp_list.pop(column)

        while '' in temp_list:
            temp_list.remove('')

        junc = ','
        clean_lines.append(junc.join(temp_list))

    clean = open(file_name, 'w')
    clean.writelines(clean_lines)
    clean.close()
