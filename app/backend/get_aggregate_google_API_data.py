"""

    get_aggregate_google_API_data.py

    This data aggregates the Google API data stored in AWS. It assumes the existence of an existing aggregate datasets

    It loads the most recent aggregate dataset, the most recent daily scrapes of data, and appends the most recent scrape
    to the most recent aggregate dataset

    Args:
        - Date: a date, in the format of %Y-%m-%d (e.g., 2020-03-20)

    Assumes that there is an existing aggregate dataset and that the most recent version has already been scraped
    (via 'get_google_API_data.py')

"""
import os
import sys
import re
import boto3
import pytrends
from pytrends.request import TrendReq
import pandas as pd
import datetime
import re

if __name__ == "__main__":

    # get consts, creds, args

    AWS_BUCKET = os.environ["AWS_BUCKET"]
    AWS_ACCESS = os.environ["AWS_ACCESS"]
    AWS_SECRET = os.environ["AWS_SECRET"]

    INTEREST_OVER_TIME_FILENAME = "interest_over_time_"
    INTEREST_BY_REGION_FILENAME = "interest_by_region_"

    LOCAL_SCRAPES_DIR = "../../tweets/google_API_scrapes/"
    AGGREGATE_GOOGLE_DIR = "aggregate_google_API_data/"
    AWS_SCRAPES_DIR = "google_API_scrapes/"

    LOCAL_AGGREGATE_TIME_PATH = LOCAL_SCRAPES_DIR + "aggregate_interest_over_time_"
    LOCAL_AGGREGATE_REGION_PATH = LOCAL_SCRAPES_DIR + "aggregate_interest_by_region_"

    AWS_AGGREGATE_TIME_PATH = AGGREGATE_GOOGLE_DIR + "aggregate_interest_over_time_"
    AWS_AGGREGATE_REGION_PATH = AGGREGATE_GOOGLE_DIR + "aggregate_interest_by_region_"

    LOCAL_TIME_FILENAME = LOCAL_SCRAPES_DIR + INTEREST_OVER_TIME_FILENAME
    LOCAL_REGION_FILENAME = LOCAL_SCRAPES_DIR + INTEREST_BY_REGION_FILENAME

    AWS_TIME_FILENAME = AWS_SCRAPES_DIR + INTEREST_OVER_TIME_FILENAME
    AWS_REGION_FILENAME = AWS_SCRAPES_DIR + INTEREST_BY_REGION_FILENAME

    # get date provided, date of most recent aggregate file

    START_DATE = "2020-03-01"
    DATE = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")
    DATE_FORMATTED = DATE.strftime("%Y-%m-%d")

    PREV_DATE_FORMATTED = (
        DATE - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    print(
        f"The provided date is: {DATE_FORMATTED} and the previous date is {PREV_DATE_FORMATTED}")

    # get filenames, of preexisting file, the most recent data scrape, and the next aggregate file
    PREV_AGG_DATA_FILENAME = f"{START_DATE}_{PREV_DATE_FORMATTED}.csv"

    NEW_FILE_SCRAPE_TIME = AWS_TIME_FILENAME + DATE_FORMATTED
    NEW_FILE_SCRAPE_REGION = AWS_REGION_FILENAME + DATE_FORMATTED

    NEW_AGG_DATA_FILENAME = f"{START_DATE}_{DATE_FORMATTED}.csv"

    # connect with AWS S3
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS,
                      aws_secret_access_key=AWS_SECRET)

    # load pre-existing data:

    # load previous aggregate data
    s3.download_file(Bucket=AWS_BUCKET,
                     Key=AWS_AGGREGATE_TIME_PATH + PREV_AGG_DATA_FILENAME,
                     Filename=LOCAL_AGGREGATE_TIME_PATH + PREV_AGG_DATA_FILENAME)

    s3.download_file(Bucket=AWS_BUCKET,
                     Key=AWS_AGGREGATE_REGION_PATH + PREV_AGG_DATA_FILENAME,
                     Filename=AWS_AGGREGATE_REGION_PATH + PREV_AGG_DATA_FILENAME)

    # load today's time and region data
    s3.download_file(Bucket=AWS_BUCKET,
                     Key=NEW_FILE_SCRAPE_TIME,
                     Filename=LOCAL_TIME_FILENAME + DATE_FORMATTED + ".csv")

    s3.download_file(Bucket=AWS_BUCKET,
                     Key=NEW_FILE_SCRAPE_REGION,
                     Filename=LOCAL_REGION_FILENAME + DATE_FORMATTED + ".csv")

    # load as dfs
    prev_agg_time_df = pd.read_csv(
        LOCAL_AGGREGATE_TIME_PATH + PREV_AGG_DATA_FILENAME)
    prev_agg_region_df = pd.read_csv(
        AWS_AGGREGATE_REGION_PATH + PREV_AGG_DATA_FILENAME)

    new_time_df = pd.read_csv(LOCAL_TIME_FILENAME + DATE_FORMATTED + ".csv")
    new_region_df = pd.read_csv(
        LOCAL_REGION_FILENAME + DATE_FORMATTED + ".csv")

    # remove local copies
    os.remove(LOCAL_AGGREGATE_TIME_PATH + PREV_AGG_DATA_FILENAME)
    os.remove(AWS_AGGREGATE_REGION_PATH + PREV_AGG_DATA_FILENAME)
    os.remove(LOCAL_TIME_FILENAME + DATE_FORMATTED + ".csv")
    os.remove(LOCAL_REGION_FILENAME + DATE_FORMATTED + ".csv")

    # add 'date' col to region df
    new_region_df['date'] = DATE_FORMATTED

    # append new dfs to running aggregate dfs
    new_agg_time_df = prev_agg_time_df.append(new_time_df)
    new_agg_region_df = prev_agg_region_df.append(new_region_df)

    # save new dfs, locally
    new_agg_time_df.to_csv(LOCAL_AGGREGATE_TIME_PATH +
                           f"{START_DATE}_{DATE_FORMATTED}.csv")
    new_agg_region_df.to_csv(
        LOCAL_AGGREGATE_REGION_PATH + f"{START_DATE}_{DATE_FORMATTED}.csv")

    # export to AWS
    s3.upload_file(LOCAL_AGGREGATE_TIME_PATH +
                   f"{START_DATE}_{DATE_FORMATTED}.csv",
                   AWS_BUCKET, AWS_AGGREGATE_TIME_PATH + f"{START_DATE}_{DATE_FORMATTED}.csv")
    s3.upload_file(LOCAL_AGGREGATE_REGION_PATH + f"{START_DATE}_{DATE_FORMATTED}.csv",
                   AWS_BUCKET, AWS_AGGREGATE_REGION_PATH + f"{START_DATE}_{DATE_FORMATTED}.csv")

    print(
        f"Finished running 'get_aggregate_google_API_data.py' at (in UTC time): {datetime.datetime.utcnow()}")
