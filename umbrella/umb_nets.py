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


def nets(brella_toke):
    logging.info("Start umb_nets.py")
    umb_net_url = "https://api.umbrella.com/deployments/v2/networks"
    umb_hdr = f"Bearer {brella_toke}"
    umb_head = {"Authorization": umb_hdr}

    umb_nets = (request("GET", umb_net_url, headers=umb_head, timeout=2)).json()

    # deployed_nets = umb_nets.json()
    logging.info("End umb_token.py")
    return umb_nets
