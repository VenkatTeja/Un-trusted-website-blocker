#!/usr/bin/env python3

import ipaddress
import time
import json
import blockade
import logging
from datetime import datetime
from requests import get

# Set loop wait time between each check (in seconds)
WAIT_TIME = 30

"""Logging setup to ./logs folder"""
now = datetime.now()
stringDate = now.strftime("%Y_%m_%d")
logging.basicConfig(filename="logs/" + stringDate + ".log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y%I:%M:%S %p',
                            level=logging.DEBUG)

"""
Closes blockade when one's IP is not as expected.
(requires admin priviledges)
"""

logging.info("Application initialised")
while True:
    try:
        public_ip = ipaddress.ip_address(get('https://api.ipify.org', verify=False).text)
    except Exception as e:
        # Probably because system is not connected to the internet.
        logging.error("Exception while checking public ip")
        time.sleep(WAIT_TIME)
        continue

    logging.info("My Public IP: %s" % public_ip)
    logging.info("Blockade status: %d" % blockade.status.value)

    with open("trusted_ips.json", "r") as f:
        data = json.load(f)
        trusted_ips = data['TRUSTED_IPS']
        logging.debug("TRUSTED_IPs: " + str(trusted_ips))

        for ip in trusted_ips:
            logging.debug("Expected IP: %s" % ip)
            EXPECTED_IP = ipaddress.ip_address(ip)
            if public_ip != EXPECTED_IP and blockade.status!=blockade.Status.BLOCKED:
                blockade.start()
            elif public_ip==EXPECTED_IP and blockade.status!=blockade.Status.OPEN:
                blockade.stop()
    time.sleep(WAIT_TIME)
