#!/usr/bin/env python3
"""Get the current uplink public IP addresses from the Meraki organization MX."""

__author__ = "Aaron Davis"
__version__ = "0.0.5"
__copyright__ = "Copyright (c) 2023 Aaron Davis"
__license__ = "MIT License"

import os
import sys
import configparser
import json
import time
import logging
from logging import handlers
from requests import request
from umbrella import umb_nets, umb_token, retire_nets, deploy_nets


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(r".\logs\umb_nets_debug.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

KEY = "CI"
environ = os.getenv(KEY, default="LOCAL")

if environ == "true":
    mer_key = os.environ["mer_key"]
    mer_org = os.environ["mer_org"]
else:
    config = configparser.ConfigParser()
    config.read("./secrets/config.ini")
    mer_key = config["MERAKI"]["mer_key"]
    mer_org = config["MERAKI"]["mer_org"]

m_nets = []
u_nets = []

mer_url = "https://api.meraki.com/api/v1"
mer_uplinks = f"/organizations/{mer_org}/appliance/uplink/statuses"
# mer_payload = {}
mer_headers = {"X-Cisco-Meraki-API-Key": mer_key}

logging.info("Running merumb.py")

response = request("GET", mer_url + mer_uplinks, headers=mer_headers, timeout=2)

mer_resp = response.json()

int0_name = mer_resp[0]["uplinks"][0]["interface"]
int0_pub = mer_resp[0]["uplinks"][0]["publicIp"]
int1_name = mer_resp[0]["uplinks"][1]["interface"]
int1_pub = mer_resp[0]["uplinks"][1]["publicIp"]

m_nets = [int0_pub, int1_pub]

logging.info(f"{int0_name} is {int0_pub}")
logging.info(f"{int1_name} is {int1_pub}")

logging.info("Ending merumb.py")

brella_token = umb_token.umb_token()

deployed_nets = umb_nets.nets(brella_token)

for count, value in enumerate(deployed_nets):
    print(f"Umbrella network {count} is {value['ipAddress']}")
    u_nets.append(value["ipAddress"])

u_retired_nets = [x for x in m_nets if x not in set(u_nets)]
m_retired_nets = [x for x in u_nets if x not in set(m_nets)]

print(f"These Meraki IP's are not deployed in Umbrella: {u_retired_nets}")
print(f"These Umbrella networks need to be removed: {m_retired_nets}")

if m_retired_nets:
    print("Remove retired Umbrella networks.")
    retire_nets.del_nets(m_retired_nets, deployed_nets, brella_token)
else:
    print("No networks need to be removed.")

if u_retired_nets:
    print("Adding new networks to Umbrella.")
    deploy_nets.add_nets(u_retired_nets, brella_token)
else:
    print("No networks need to be added to Umbrella.")

logging.info("End script")
