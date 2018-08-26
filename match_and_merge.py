__author__ = "Ahmed Elsers"
__Email__ = "ahmed.elsersi@gmail.com"

####################
# Search and Match #
####################
# This is a script that accepts 3 files as input, IP/MAC/VLAN, IP/DNS-NAME, and MAC/PORT.
# The output is one single csv file contains IP/MAC/VLAN/DNS-NAME/PORT.

####################
# Concept - Design #
####################
# 1- Make a list of the files which are going to be used, and convert them if they are in xlsx to csv format if needed.
# 2- Wrangling and clean Data: IP, MAC, DNS-NAME, and PORT
# 3- Save Data

import os
import sys
import argparse
import fileinput
import pandas as pd
from textwrap import dedent

from regex_check import *

parser = argparse.ArgumentParser(description=dedent("""Search & Match three csv/excel FILEs containing
                                                       IP/MAC, IP/DNS and MAC/PORT, and save the output to
                                                       a csv/excel FILE contains IP/MAC/PORT/DNS."""),
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--version", help="print version", action="version", version="%(prog)s v1.0")
parser.add_argument("FILE", nargs="*")
args = parser.parse_args()



# Make a list of the files which are going to be used, and convert them if they are in xlsx to csv format if needed
def get_csv_xlsx_files_list():
    csv_list = []
    xlsx_list = []
    for file in args.FILE:
        if os.path.splitext(file)[1] == '.csv':
            csv_list.append(file)
        elif os.path.splitext(file)[1] == '.xlsx':
            xlsx_list.append(file)
        else:
            print(file, 'is not in csv or xlsx format.')
            sys.exit(0)
    if xlsx_list:
        return csv_list + convert_to_csv(xlsx_list)
    else:
        return csv_list


# convert xlsx file to csv format
def convert_to_csv(args):
    files_list = []
    for file in args:
        file_dir_name = os.path.dirname(file)
        file_name_extension_csv = os.path.splitext(os.path.basename(file))[0] + '.csv'
        new_csv_path = os.path.join(file_dir_name, file_name_extension_csv)
        xlsx_file = pd.ExcelFile(file)
        df = pd.read_excel(xlsx_file)
        df.to_csv(new_csv_path, index=False)
        files_list.append(new_csv_path)
    return files_list


def wrangling_clean_data():
    files_list = get_csv_xlsx_files_list()
    for file in files_list:
        load_file = pd.read_csv(file, dtype=str)
        file_columns = [col for col in load_file.columns]
        for column in file_columns:
            if column.upper() == 'IP':
                load_file[column] = load_file[column].apply(regex_check_ip)
            elif column.upper() == 'MAC':
                load_file[column] = load_file[column].apply(regex_check_mac)
        load_file.to_csv(file, index=False)
    return files_list



def merge_save_data():
    files_list = wrangling_clean_data()
    frames = [pd.read_csv(file, dtype=str) for file in files_list]
    first_frame = frames[0]
    for frame in frames[1:]:
        first_frame = first_frame.merge(frame)
    first_frame.to_csv('final.csv', index=False)




if __name__ == '__main__':
    try:
        merge_save_data()

    except FileNotFoundError:
        print(fileinput.filename(),":", "No such file or directory")
    except IsADirectoryError:
        print(fileinput.filename(),":", "Is a directory")
    except KeyboardInterrupt:
        print()
        sys.exit(0)
