""" This module is a part of HoneySpot project.
The module can be used to uncover GasPot honeypot.
This is a work in progress and might give false results.
"""

#TODO: Add more fingerprinting methods

import socket

__name__ = "GasPot"
# __proto__ = [] # Not sure
default_port = 10001

# Terminal print codes
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

ctrl_a = chr(1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def run(target, port):
    port = port if port != 0 else default_port
    print "[+] Now running GasPot module against - %s" % target

    s.connect((target, port))
    default_stations_list(target, port)
    s.close()

def default_stations_list(target, port):
    print "[+] Inside default_stations_list method."
    print "[+] Trying to fingerprint by checking for default station names."

     # Fetching default stations list, that comes with GasPot
    with open("modules/gaspot_default_stations_list.txt") as f:
        default_stations = [l.strip().lower() for l in f.readlines()]
    
    cmd = ctrl_a + "I20200\r\n"
    s.send(cmd)
    recvd = s.recv(1024)
    # Removing empty lines from response
    data = filter(None, recvd.split("\n"))

    # Now we know that station name comes in as 3rd element in data
    for station in default_stations:
        if data[2].lower().find(station) >= 0:
            print WARNING + "\t[+] Station name found in GasPot default list." + ENDC
            print FAIL + "\t[+] This is a possible GasPot instance." + ENDC
            break