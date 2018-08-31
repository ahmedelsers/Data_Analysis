#!/usr/bin/env python
__author__ = 'Ahmed Elsers'
__Email__ = 'ahmed.elsersi@gmail.com'


#####################
# Scan Network #
####################
# This is a script to scan a Network range given by the user, to do nslookup/reverse nslookup.
# and generate a file contains two column, IP and FQDN.

import os
import sys
import platform
import socket
import argparse
import ipaddress
from textwrap import dedent
try:
    import pandas as pd
except ModuleNotFoundError:
    os.system('pip install pandas')
    import pandas as pd


parser = argparse.ArgumentParser(description=dedent("""Scan Network IP range, and get the FQDN for each IP,
                                                       and save the output to a file."""),
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--version", help="print version",
                   action="version", version="%(prog)s v4.0")
parser.add_argument("-ip", "--ip-range", dest='IP', help="Enter the Network IP range, ex. 10.6.1.0/24",
                    default='10.6.1.0/24', type=str, nargs='+')
parser.add_argument("-o", "--output", help="the output file name",
                    dest='file_name', default='scan_output.csv')
args = parser.parse_args()


def check_input_file():
    if os.path.splitext(args.file_name)[1] == '.csv':
        file_name = args.file_name
    else:
        file_name = args.file_name + '.csv'
    if os.path.isfile(file_name):
        print(file_name, end=': ')
        raise FileExistsError
    elif os.path.isdir(file_name):
        print(file_name, end=': ')
        raise IsADirectoryError
    else:
        return file_name


def scan_network():
    IP_FQDN = []
    IP_NETWORKS_LIST = [ipaddress.ip_network(ip_network) for ip_network in args.IP ]
    try:
        for ip_network in IP_NETWORKS_LIST:
            ip_list = [ip.compressed for ip in ip_network]
            ip_list.pop(0)
            ip_list.pop()
            if platform.system() == 'Windows':
                command = "ping -n 1 -l 1 -s 1 -w 1 "
            else:
                command = "ping -c 1 -l 1 -s 1 -W 1 "
            for ip in ip_list:
                test = True if os.system(command + ip) is 0 else False
                if test:
                    IP_FQDN.append((ip, socket.getfqdn(ip)))
                else:
                    IP_FQDN.append(
                        (ip, socket.getfqdn(ip), "Server is not reachable."))
    except ValueError:
        print("Please enter a valid network IP/prefix_len, ex. 10.6.1.0/24, 10.6.0.0/16")
    return IP_FQDN


def save_data():
    file_name = check_input_file()
    IP_FQDN = scan_network()
    data = pd.DataFrame(data=IP_FQDN, columns=['IP', 'FQDN', 'Status'])
    data.to_csv(file_name, index=False)


def main():
    save_data()


if __name__ == '__main__':
    try:
        main()
    except FileExistsError:
        print("file exists, choose another name.")
    except IsADirectoryError:
        print("Is a directory, choose another name.")
    except KeyboardInterrupt:
        print()
        sys.exit(0)
