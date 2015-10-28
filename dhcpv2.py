#!/usr/bin/env python

### This script add dhcp static host/mac entry to dhcpd.conf

## argparse 
## read dhcpd.conf file
## read line and find regex pattern of host/mac entry
## add each host to dictionary, line # key
## if input hostname not match and mac is the same, change to new hostname
## add each mac to dictionary as key and line # key
## if input hostname match and mac is different, change to new mac
## if no match write exact line to new file

"""
add a host's mac_address and hostname to DHCP server.
example: addclient --name host1 --mac 00:00:00:00:00:01 
"""

import argparse
import re
import shutil
import os

def backupConfigFile(src, dst):
    print("backup dhcpd.conf file")
    shutil.copy(src, dst)

def copyConfigFile(src, dst):
    print("Copy dhcp temp file to dhcpd.conf")
    shutil.copy(src, dst)

def makeConfigFile():
    pass

def main():
    dhcpd_conf = 'dhcpd.conf'
    dhcpd_conf_bak = 'dhcpd.conf.bak'
    dhcpd_temp_conf = 'dhcpd_temp.conf'
    store_data = {}  ## Store match data
    match_line = []  ## Store match data

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--hostname", required=True, help="hostname")
    parser.add_argument("-m", "--hostmac", required=True, help="host mac address")
    parser.add_argument("-f", "--force", action="store_true", help="force overwrite existing duplicate")
    args = parser.parse_args()

    new_dhcp_entry = '{} {{ hardware ethernet {}; fixed-address {}; option host-name "{}"; }}\n'.format(args.hostname, args.hostmac, args.hostname, args.hostname)

    ## backup file
    backupConfigFile(dhcpd_conf, dhcpd_conf_bak)

    print("input hostname: {}, hostmac: {}".format(args.hostname, args.hostmac))

#   Add all entries in dictionary store_data: key = line #, value = list of words of an entry
    with open(dhcpd_conf, 'r') as dhcp_file:
        ## enumerate line number similar to file_line_num += 1
        for file_line_num, line in enumerate(dhcp_file, start=1):
            store_data[file_line_num] = line

#   store match data in match_data  
    for key, value in store_data.iteritems():
        if args.hostname in value or args.hostmac in value:
           #print('host match line {}. Use -f to overwrite.'.format(key))
           match_line.append(key)
          
# if entry exists use force to overwrite
    if match_line:
        print("entry exists line {} use -f to overwrite".format(match_line))
        if args.force:
            for i in match_line:
                del store_data[i]

            with open(dhcpd_temp_conf, 'w') as temp_dhcp_file:
                for key, value in store_data.iteritems():
                    temp_dhcp_file.write(value)
                temp_dhcp_file.write(new_dhcp_entry)
                
            ## make temp file as dhcpd.conf
            copyConfigFile(dhcpd_temp_conf, dhcpd_conf)

# if entry does not exist append entry to original dhcpd.conf file
    else:
        print("Entry not exist adding new entry {}".format(new_dhcp_entry))
        with open(dhcpd_conf, 'a+') as main_dhcp_file: 
            main_dhcp_file.write(new_dhcp_entry)
            
## main
if __name__ == '__main__':
    main()
