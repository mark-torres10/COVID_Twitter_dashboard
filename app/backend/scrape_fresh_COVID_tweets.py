"""

    scrape_fresh_COVID_tweets.py

    This script uses the Twitter API (via twarc) to scrape a fresh sample
    batch of COVID tweets. These tweets won't be preprocessed in any way, they're 
    just meant to be displayed on the dashboard's frontend. 

    This script is meant to be run hourly as a cron job
"""
import os
import time
import datetime
import boto3
import pandas as pd
from twarc import Twarc
from aws_helpers import save_to_AWS

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
    # year-month-day hour (military time, in UTC time)
    FRESH_TWEETS_FILENAME = f"fresh_hourly_tweets_{datetime.datetime.utcnow().strftime('%Y-%m-%d %H')}.csv"

    LOCAL_FRESH_TWEETS_DIR = "./../../tweets/hourly_tweets/"
    LOCAL_FRESH_TWEETS_PATH = LOCAL_FRESH_TWEETS_DIR + FRESH_TWEETS_FILENAME

    AWS_TWEET_DIR = "tweet_scrapes/"
    AWS_FRESH_TWEETS_PATH = AWS_TWEET_DIR + \
        "hourly_tweets/" + FRESH_TWEETS_FILENAME

    # connect to Twitter API
    num_login_attempts = 1

    while True:
        try:
            t = Twarc(CONSUMER_KEY, CONSUMER_SECRET,
                      ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            break
        except Exception as e:
            print("Problem with connecting to Twitter API")
            print(e)
            sleep_time_seconds = 60 * num_login_attempts
            num_login_attempts += 1
            time.sleep(sleep_time_seconds)
            if num_login_attempts > 5:
                break

    # scrape fresh tweets (filter allows you to get tweets as they happen)
    JSON_list = []
    search_terms = ["covid", "covid19", "vaccine", "coronavirus"]
    search_query = ','.join(search_terms)
    num_tweets = 10

    for i in range(num_tweets):
        try:
            tweet = next(
                t.filter(track=search_query))

            JSON_list.append(tweet)
        except Exception as e:
            print("Error in scraping fresh tweets")
            print(e)
            raise ValueError("Please resolve scraping issue.")

    # transform into pandas df
    df = pd.DataFrame(JSON_list)

    # save locally
    df.to_csv(LOCAL_FRESH_TWEETS_PATH)

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
