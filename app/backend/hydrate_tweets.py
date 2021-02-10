"""

    hydrate_tweets.py

    This script takes tweet IDs and returns the full tweet JSON object associated with that tweet ID. 
"""
import os
import csv
import pandas as pd
import datetime
import twarc
from twarc import Twarc
import aws_helpers
from aws_helpers import save_to_AWS, load_from_AWS


if __name__ == "__main__":

    # change dir to this file's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # get env vars
    CONSUMER_KEY = os.environ["CONSUMER_KEY"]
    CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

    AWS_BUCKET = os.environ["AWS_BUCKET"]
    AWS_ACCESS = os.environ["AWS_ACCESS"]
    AWS_SECRET = os.environ["AWS_SECRET"]

    # initialize paths
    AWS_TWEET_DIR = "tweet_scrapes/"
    ID_PATH = "./../../tweets/tweet_IDs/"
    TWEETS_PATH = "./../../tweets/hydrated_tweets/"
    LOCAL_TWEET_PATH = "./../../tweets/"

    # local filenames of exports
    ID_FILENAME = "scraped_tweet_IDs_2020-03-20_2021-02-09.csv"
    TWEETS_FILENAME = "hydrated_tweets_2020-03-20_2021-02-09.csv"
    LOCAL_EXPORT_ID_PATH = ID_PATH + ID_FILENAME
    LOCAL_EXPORT_TWEETS_PATH = TWEETS_PATH + TWEETS_FILENAME
    AWS_EXPORT_ID_PATH = AWS_TWEET_DIR + "tweet_IDs/" + ID_FILENAME
    AWS_EXPORT_TWEETS_PATH = AWS_TWEET_DIR + "hydrated_tweets/" + TWEETS_FILENAME

    try:
        # load text file from AWS
        load_from_AWS(LOCAL_EXPORT_ID_PATH,
                      AWS_EXPORT_ID_PATH,
                      "s3",
                      AWS_BUCKET,
                      AWS_ACCESS,
                      AWS_SECRET)
    except Exception as e:
        print("Error in loading tweet IDs from AWS")
        print(e)

    # create tweet ID list
    tweet_ID_list = []

    with open(LOCAL_EXPORT_ID_PATH, "r") as f:
        datareader = csv.reader(f)
        for row in datareader:
            tweet_ID_list.append(row)

    # connect twarc
    t = Twarc(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    try:
        # hydrate tweets
        JSON_list = t.hydrate(tweet_ID_list)
    except Exception as e:
        print("Error in hydrating tweets")
        print(e)
        raise ValueError("Please resolve hydration issue.")

    # transform into pandas df
    df = pd.read_json(JSON_list, lines=True)

    # save locally
    df.to_csv(LOCAL_EXPORT_TWEETS_PATH)

    try:
        # save to AWS
        save_to_AWS(LOCAL_EXPORT_TWEETS_PATH,
                    AWS_EXPORT_TWEETS_PATH,
                    "s3",
                    AWS_BUCKET,
                    AWS_ACCESS,
                    AWS_SECRET)
    except Exception as e:
        print("Error in exporting the local files to AWS")
        print(e)
        print("------------------")
        raise ValueError(
            "Please fix the error in exporting the local files to AWS")
    finally:
        print(
            f"Finished with the execution of 'hydrate_tweets.py' at (in UTC time): {datetime.datetime.utcnow()}")
