import logging
import os
import subprocess
import shlex
import psutil
from enum import Enum

"""
Allows blocking a set of URLs using hosts redirection.
The list of URLs that will be blocked is set below.
"""

# Configure these
ADDRESSES_TO_BLOCK = ["mywealth.bnpparibas.ch", "ebanking-ch2.ubs.com", "online.bankaustria.at"]
REDIRECT_IP = "93.184.216.34"
HOSTS_FILE = "/private/etc/hosts"
# Configuration ends

def __exec_command(command):
    """Execute a command and wait for it to finish."""
    p = subprocess.Popen(shlex.split(command))
    p.wait()

def addDomainsToHosts():
    """Adds the configured hosts redirection logic to hosts file"""
    __exec_command("cp original_hosts " + HOSTS_FILE)
    logging.info("Copied original hosts to location (activating block)")

    lines = ["\n\n"]
    for address in ADDRESSES_TO_BLOCK:
        lines.append(REDIRECT_IP + " " + address + " #SHOW ONLY WHEN CONNECTED TO UN-TRUSTED IP\n")
    with open(HOSTS_FILE, "a+") as f:
        f.writelines(lines)
    logging.info("hosts file updated")

def removeDomainsFromHosts():
    __exec_command("cp original_hosts " + HOSTS_FILE)
    logging.info("Copied original hosts to location (deactivating block)")

class Status(Enum):
    """Possible statuses of the blockade."""
    UNDEFINED = 0
    OPEN = 1
    BLOCKED = 2

status = Status.UNDEFINED # the current status of the blockade

def stop():
    """Stop blocking. (requires admin priviledges)"""
    logging.info("Action Trigger: Stop")
    global status
    if status is Status.OPEN:
        return

    removeDomainsFromHosts()
    status = Status.OPEN

def start():
    """Start blocking. (requires admin priviledges)"""
    logging.info("Action Trigger: Start")
    global status
    if status is Status.BLOCKED:
        return

    addDomainsToHosts()
    status = Status.BLOCKED
