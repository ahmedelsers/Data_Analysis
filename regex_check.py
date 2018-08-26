__author__: Ahmed Elsers
__Email__: ahmed.elsersi@gmail.com


import re

## Regular Expresions to extract IPs, MACs, DNSs and PORTs
def regex_check_ip(ip):
    ip = str(ip).strip()
    try:
        ip_regex_check_result = [0<=int(x)<256 for x in re.split('\.',re.match(r'^\d+\.\d+\.\d+\.\d+$',str(ip)).group(0))].count(True)==4
        if ip_regex_check_result:
            return ip
    except AttributeError:
        return 'None_' + ip

def regex_check_mac(mac):
    mac = str(mac).strip()
    try:
        mac_regex_check_result = re.match('([a-fA-F0-9]{4}[:|\-|\.]?){3}$', mac).group(0) == mac
        if mac_regex_check_result:
            return mac
    except AttributeError:
        return 'None_' + mac
