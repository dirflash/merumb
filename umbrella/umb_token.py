#!/usr/bin/env python3
"""Get the Umbrella API access token."""

__author__ = "Aaron Davis"
__version__ = "0.0.5"
__copyright__ = "Copyright (c) 2023 Aaron Davis"
__license__ = "MIT License"

import os
import sys
import configparser
import logging
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(r".\logs\umb_token_debug.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

KEY = "CI"
environ = os.getenv(KEY, default="LOCAL")

if environ == "true":
    umb_key = os.environ["umb_key"]
    umb_secr = os.environ["umb_secr"]
else:
    config = configparser.ConfigParser()
    config.read("./secrets/config.ini")
    umb_key = config["UMBRELLA"]["umb_key"]
    umb_secr = config["UMBRELLA"]["umb_secr"]
    # logger.addHandler(logHandler)


def umb_token():
    logging.info("Start umb_token.py")
    token_url = "https://api.umbrella.com/auth/v2/token"

    auth = HTTPBasicAuth(umb_key, umb_secr)
    client = BackendApplicationClient(client_id=umb_key)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url, auth=auth)
    umb_auth = str(token["access_token"])
    logging.info("End umb_token.py")
    return umb_auth


if __name__ == "__main__":
    umb_token()
