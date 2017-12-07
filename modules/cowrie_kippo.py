""" This module is a part of HoneySpot project.
The module can be used to uncover Kippo and possibly Cowrie.
This is a work in progress and might give false results.
https://github.com/micheloosterhof/cowrie/blob/master/cowrie/commands/fs.py#L309 - Lack on -p switch
"""

# Cowrie has problem playing nice with Python SSH
# libs (paramiko and pxssh). We will use this to try to
# fingerprint.

import pxssh
import socket

global score

__name__ = "Kippo"
__proto__ = ["ssh"]
default_port = 22

# Terminal print codes
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def run(target, port):
    port = port if port != 0 else default_port
    print "[+] Now running Cowrie/Kippo module against - %s" % target
    
    # trying various tests.
    paramiko_exec_command(target, port)
    connect_pxssh(target, port)

def paramiko_exec_command(target, port):
    print "\n[+] Trying to test connection using paramiko."
    try:
        import paramiko
    except ImportError:
        print "[-] Failed to import paramiko, not running this test."
        return

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(target, port, "root", "password")
    try:
        stdin, stdout, stderr = client.exec_command("hostname")
    except paramiko.SSHException as e: 
        if str(e) == "Channel closed.":
            print "\t[-] Failed to execute command using paramiko."
            print FAIL + "\t[-] Possible honeypot instance detected." + ENDC

    finally:
        client.close()

def connect_pxssh(target, port):
    print "\n[+] Trying to connect using pxssh."
    ssh_client = None # This variable holds the successful login object

    is_prompt_found = True
    try:
        ssh_client = pxssh.pxssh()
        print "[+] Trying to SSH with `auto_prompt_reset=True`. Might take few seconds."
        ssh_client.login(server=target, 
                     port=port, 
                     username="root", 
                     password="password")

        ssh_client.sendline("id")
        ssh_client.prompt(timeout=5)
        if "uid=0(root)" in client.before:
            print "[+] Log-in successful."
            print "[+] Test command executed successfully!"
    except Exception as e:
        ssh_client.close()
        if "could not set shell prompt" in str(e):
            is_prompt_found = False
            print "\t[-] Problem setting prompt."
            print FAIL + "\t[-] Possible honeypot instance detected." + ENDC
        
    if not is_prompt_found:
        try:
            ssh_client = pxssh.pxssh()
            print "[+] Trying to SSH with `auto_prompt_reset=False`"
            ssh_client.login(server=target, 
                         port=port, 
                         username="root", 
                         password="password",
                         auto_prompt_reset=False)

            prompt_pattern = "root@\w+\:~#"
            ssh_client.PROMPT = prompt_pattern
            ssh_client.sendline("id")
            ssh_client.prompt(timeout=5)
            if "uid=0(root)" in ssh_client.before:
                print "\t[+] Log-in successful using pxssh."
        except Exception as e:
            print FAIL + "\t[-] Problem logging in using pxssh. Cannot continue." + ENDC
            ssh_client.close()
            return

    if ssh_client:
        or_operator_check(ssh_client)
        cd_old_directory(ssh_client)
        curl_ftp_download(ssh_client)
        ssh_client.close()

def or_operator_check(client):
    # https://github.com/micheloosterhof/cowrie/issues/512
    print "\n[+] Testing using || operator."
    issue_url = "https://github.com/micheloosterhof/cowrie/issues/512"
    command = "echo definitely || echo  _honeypot"
    client.sendline(command)
    client.prompt(timeout=2)

    stdout = client.before.strip()
    if "_honeypot" in stdout:
        print "\t[-] OR operator (||) check failed."
        print FAIL + "\t[-] Possible honeypot instance detected." + ENDC
        print "\t[+] Update when this issue is fixed: {}.".format(issue_url)

def cd_old_directory(client):
    """https://github.com/micheloosterhof/cowrie/blob/master/cowrie/commands/fs.py#L135
    This code checks if we can run 'cd -' command on target or not.
    First checks by doing cd to some directory and then doing "cd -".
    Secondly it checks by setting OLDPWD variable which is used by "cd -".
    """
    print "\n[+] Now testing changing to $OLDPWD directory."
    command = "cd /"
    client.sendline(command)
    client.prompt(timeout=2)
    command = "cd -"
    client.sendline(command)
    client.prompt(timeout=2)
    if "bash: cd: OLDPWD not set" in client.before:
        print "\t[-] First pass failed."
        print FAIL + "\t[-] Possible honeypot instance detected." + ENDC

    print "\n\t[+] Setting $OLDPWD variable and checking again."
    command = "OLDPWD='/root/'"
    client.sendline(command)
    client.prompt(timeout=2)
    command = "cd -"
    client.sendline(command)
    client.prompt(timeout=2)
    if  "bash: cd: OLDPWD not set" in client.before:
        print "\t[-] Second pass failed."
        print FAIL + "\t[-] Possible honeypot instance detected." + ENDC

def curl_ftp_download(client):
    """https://github.com/micheloosterhof/cowrie/issues/6
    """
    print "\n[+] Trying to download other protocol with curl."

    command = "curl ftp://ftp.au.debian.org/debian/README"
    error_msg = "Unsupported scheme."
    client.sendline(command)
    client.prompt()
    if error_msg in client.before:
        print "\t[-] Failed to download via curl."
        print FAIL + "\t[-] Possible honeypot instance detected." + ENDC