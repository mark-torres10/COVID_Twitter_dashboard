"""

    hydrate_tweets.py

    This script takes tweet IDs and returns the full tweet JSON object associated with that tweet ID. 
"""
import os
import twarc
from twarc import Twarc


if __name__ == "__main__":

    # get env vars
    CONSUMER_KEY = os.environ["CONSUMER_KEY"]
    CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

    # connect twarc
    t = Twarc(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    dir(t)

    print(t)
