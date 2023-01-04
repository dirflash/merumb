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


def del_nets(mer_retired, d_nets, b_token):
    logging.info("Start retire_nets.py")
    for count, val in enumerate(d_nets):
        for entry in mer_retired:
            origin_id = val["originId"]
            if entry == val["ipAddress"]:
                print(f'ID {"origin_id"} is {val["ipAddress"]} needs to be deleted.')
                umbrella_delete_net(origin_id, b_token)
    logging.info("Ending retire_nets.py")


def umbrella_delete_net(o_id, token):
    d_url = f"https://api.umbrella.com/deployments/v2/networks/{o_id}"
    d_tok = f"Bearer {token}"
    d_payload = "{}"
    d_headers = {"Authorization": d_tok, "Accept": "application/json"}
    d_resp = request("DELETE", d_url, headers=d_headers, data=d_payload, timeout=2)
    print(d_resp.text)
    if d_resp.ok:
        print(f"Umbrella origin ID {o_id} deleted.")
    else:
        print(f"Umbrella network ID {o_id} was not deleted.")


if __name__ == "__main__":
    main_mod()
