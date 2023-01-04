import sys
import logging
from requests import request


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(r".\logs\debug.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def main_mod():
    print("This module cannot be run directly.")


def add_nets(mer_add, b_token):
    logging.info("Start deploy_nets.py")
    a_url = "https://api.umbrella.com/deployments/v2/networks"
    a_tok = f"Bearer {b_token}"
    a_headers = {
        "Authorization": a_tok,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    for net in mer_add:
        net_name = str(net)
        a_payload = {
            "name": net_name,
            "ipAddress": net,
            "prefixLength": 32,
            "isDynamic": True,
            "status": "CLOSED",
        }
        print(a_payload)
        a_resp = request("POST", a_url, headers=a_headers, data=a_payload, timeout=2)
        print(a_resp.text)
        if a_resp.ok:
            print(f"Umbrella network {net} added.")
        else:
            print(f"Umbrella network {net} was not added.")
    logging.info("End deploy_nets.py")
