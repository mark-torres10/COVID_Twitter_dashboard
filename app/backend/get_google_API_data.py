"""

    get_google_API_data.py

    Gets google API data, for a certain set of keywords, for a given date 

    Takes the following args:

    DATE: date to scrape for (format: yyyy-mm-dd) (e.g., 2020-02-16)

"""
import os
import sys
import re
import boto3
import pytrends
from pytrends.request import TrendReq
import pandas as pd
import datetime

if __name__ == "__main__":

    # get consts, creds, args
    KEYWORDS = ["covid", "coronavirus", "lockdown", "quarantine", "vaccine"]

    AWS_BUCKET = os.environ["AWS_BUCKET"]
    AWS_ACCESS = os.environ["AWS_ACCESS"]
    AWS_SECRET = os.environ["AWS_SECRET"]

    FRESH_SCRAPES_FILENAME = ""
    INTEREST_OVER_TIME_FILENAME = "interest_over_time_"
    INTEREST_BY_REGION_FILENAME = "interest_by_region_"

    LOCAL_SCRAPES_DIR = "../../tweets/google_API_scrapes/"
    AWS_SCRAPES_DIR = "google_API_scrapes/"

    LOCAL_TIME_FILENAME = LOCAL_SCRAPES_DIR + INTEREST_OVER_TIME_FILENAME
    LOCAL_REGION_FILENAME = LOCAL_SCRAPES_DIR + INTEREST_BY_REGION_FILENAME

    AWS_TIME_FILENAME = AWS_SCRAPES_DIR + INTEREST_OVER_TIME_FILENAME
    AWS_REGION_FILENAME = AWS_SCRAPES_DIR + INTEREST_BY_REGION_FILENAME

    DATE = sys.argv[1]

    # check DATE format
    REGEX = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

    if not REGEX.match(DATE):
        raise ValueError(
            "DATE has incorrect format (must be in yyyy-mm-dd format)")

    # log into S3
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS,
                      aws_secret_access_key=AWS_SECRET)

    print(f"Getting Google API trends data for {DATE}")

    try:
        # start API call
        pytrends_API = TrendReq()

        pytrends_API.build_payload(
            kw_list=KEYWORDS, geo="US", timeframe=f"{DATE} {DATE}")

        # get trends over time and by region, and export locally:
        pytrends_API.interest_over_time().to_csv(LOCAL_TIME_FILENAME + DATE + ".csv")
        pytrends_API.interest_by_region().to_csv(LOCAL_REGION_FILENAME + DATE + ".csv")

        # upload to AWS
        s3.upload_file(LOCAL_TIME_FILENAME + DATE + ".csv",
                       AWS_BUCKET, AWS_TIME_FILENAME + DATE + ".csv")
        s3.upload_file(LOCAL_REGION_FILENAME + DATE + ".csv",
                       AWS_BUCKET, AWS_REGION_FILENAME + DATE + ".csv")

        # delete local versions of the file
        os.remove(LOCAL_TIME_FILENAME + DATE + ".csv")
        os.remove(LOCAL_REGION_FILENAME + DATE + ".csv")

        print(f"Finished getting Google API trends data for {DATE}")

    except Exception as e:
        print("Error in getting Google API trends data")
        print(e)
        print(f"Error occurred for the following date: {DATE}")

    finally:
        print(
            f"Finished running get_google_API_data.py on (in UTC time): {datetime.datetime.utcnow()}")
