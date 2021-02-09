"""

    scrape_tweets_daily.py

    This tweet performs daily scrapes of the hydrated tweets at 
    https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset

    It loads the tweets and saves both the tweets the tweet IDs to an AWS bucket

"""
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import time
import boto3


def get_links_from_website(website, driver_path, username, password):
    """

        Uses web scraping to get the .csv links for the COVID19 tweets from
        https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset

        Args:
            website (str): path to the IEEE website
            driver_path (str): path to one's Chromedriver installation
            username: IEEE username
            password: IEEE password

        Returns:
            filename_list: a list of names (str) which are labels for each link (e.g., "march25_march26.csv")
            link_list: a list of links (str) which are paths to the individual .csv files

    """

    # initialize driver
    driver = webdriver.Chrome(driver_path)
    driver.get(website)

    # click on button to log in
    login_button = driver.find_element(
        By.XPATH, "/html/body/div[3]/div/div[2]/nav/div/ul/li[2]/a")
    login_button.click()

    time.sleep(1)

    # enter login info
    username_field = driver.find_element(By.ID, "username")
    username_field.clear()
    password_field = driver.find_element(By.ID, "password")
    password_field.clear()

    username_field.send_keys(username)
    password_field.send_keys(password)

    driver.find_element(By.ID, "modalWindowRegisterSignInBtn").click()

    # get links for datasets
    has_link = True
    idx = 1
    filename_list = []
    links_list = []

    while has_link:

        try:
            row = driver.find_element(
                By.XPATH, f"/html/body/div[5]/div/div/main/div/div[2]/div[1]/div/div/div/table[2]/tbody/tr[{idx}]/td[1]/span/a")
            filename = row.text
            link = row.get_attribute("href")

            filename_list.append(filename)
            links_list.append(link)
            idx += 1

        except Exception as e:
            print("No more .csv links could be loaded")
            print(e)
            has_link = False

    driver.close()

    return (filename_list, links_list)


def get_tweetIDs_to_hydrate(link):
    """

        Takes a link to a .csv file and returns both the original .csv file (with tweet ID + sentiment score) and list of tweet IDs

        Args:
            link (str): path to .csv file
        Returns:
            df: pandas df, with cols = ["tweet_id", "sentiment_score"] (sentiment score calculated by paper referenced in the 
            IEEE link)
            tweet_IDs: list (str), with the IDs for each tweet
    """

    df = pd.read_csv(link, names=["tweet_id", "sentiment_score"])

    df.drop_duplicates(inplace=True)

    tweet_IDs = list(df["tweet_id"])

    return (df, tweet_IDs)


def save_to_AWS(local_file, s3_file, AWS_bucket, AWS_access, AWS_secret):
    """

    Saves a local file to AWS

    Args:
        local_file: path (str) to a local file to export to AWS
        s3_file: path (str) of file within the S3 bucket
        AWS_bucket: name of S3 bucket
        AWS_access: AWS access key
        AWS_secret: AWS secret key

    """

    # connect boto3 wih AWS
    try:
        s3 = boto3.client("s3",
                          aws_access_key_id=AWS_access,
                          aws_secret_access_key=AWS_secret)
    except Exception as e:
        print("Connection with AWS unsuccessful")
        print(e)
        raise ValueError("Please fix connection error to AWS S3 bucket")

    # upload data to AWS
    try:
        s3.upload_file(local_file, AWS_bucket, s3_file)
    except Exception as e:
        print("Error in uploading data to AWS")
        print(e)
        raise ValueError("Please fix error in uploading data to AWS")
    finally:
        return None


if __name__ == "__main__":

    # get credentials, as env vars

    # IEEE_USERNAME
    # IEEE_PASSWORD
    # AWS_ACCESS
    # AWS_SECRET

    IEEE_USERNAME = os.environ["IEEE_USERNAME"]
    IEEE_PASSWORD = os.environ["IEEE_PASSWORD"]

    DRIVER_PATH = "/Users/mark/Documents/research/gersteinLab/TextMining-master/chromedriver"

    AWS_TWEET_DIR = "tweet_scrapes/"
    get_links_from_website()
    # load tweets from website
    print("This part of the script loads the tweets from the website")

    #
