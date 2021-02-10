"""

    scrape_fresh_COVID_tweets.py

    This script uses the Twitter API (via twarc) to scrape a fresh sample
    batch of COVID tweets. These tweets won't be preprocessed in any way, they're 
    just meant to be displayed on the dashboard's frontend. 

    This script is meant to be run hourly as a cron job
"""
import os
import time
import boto3
from aws_helpers import save_to_AWS

if __name__ == "__main__":
    pass

    # change dir to this file's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # get env vars
    AWS_BUCKET = os.environ["AWS_BUCKET"]
    AWS_ACCESS = os.environ["AWS_ACCESS"]
    AWS_SECRET = os.environ["AWS_SECRET"]

    # initialize paths
    FRESH_TWEETS_FILENAME = ""  # year-month-day hour:00:00 (military time)

    LOCAL_FRESH_TWEETS_DIR = "./../../tweets/hourly_tweets/"
    LOCAL_FRESH_TWEETS_PATH = LOCAL_FRESH_TWEETS_DIR + FRESH_TWEETS_FILENAME

    AWS_TWEET_DIR = "tweet_scrapes/"
    AWS_FRESH_TWEETS_PATH = AWS_TWEET_DIR + \
        "hourly_tweets/" + FRESH_TWEETS_FILENAME

    # scrape fresh tweets

    # export to AWS bucket
    try:
        # save to AWS
        save_to_AWS(LOCAL_FRESH_TWEETS_PATH,
                    AWS_FRESH_TWEETS_PATH,
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
            f"Finished with the execution of 'scrape_fresh_COVID_tweets.py' at (in UTC time): {datetime.datetime.utcnow()}")
