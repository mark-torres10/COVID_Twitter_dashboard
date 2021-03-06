"""

    scrape_tweets_daily.py

    This tweet performs daily scrapes of the hydrated tweets at 
    https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset

    It loads the tweets and saves both the original dataframes (with two cols, "tweet_id" and "sentiment_score")
    and the tweet IDs to an AWS bucket

"""
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import time
import datetime
import boto3
import aws_helpers
from aws_helpers import save_to_AWS


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


def save_tweet_IDs(tweet_IDs, filepath):
    """
    Save a list of tweet IDs as a file (.csv)
    Args:
        tweet_IDs: list (str) of tweet IDs
        filepath: path (str) to save IDs

    Returns: 
        None
    """

    last_line = len(tweet_IDs) - 1

    with open(filepath, "w") as f:
        for idx, tweet in enumerate(tweet_IDs):
            if idx != last_line:
                f.write(f"{tweet}, \n")
            else:
                f.write(f"{tweet}")

    return None


if __name__ == "__main__":

    # change dir to this file's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # get env vars
    IEEE_USERNAME = os.environ["IEEE_USERNAME"]
    IEEE_PASSWORD = os.environ["IEEE_PASSWORD"]
    AWS_ACCESS = os.environ["AWS_ACCESS"]
    AWS_SECRET = os.environ["AWS_SECRET"]
    AWS_BUCKET = os.environ["AWS_BUCKET"]

    # initialize paths
    AWS_TWEET_DIR = "tweet_scrapes/"
    ID_PATH = "./../../tweets/tweet_IDs/"
    LOCAL_TWEET_PATH = "./../../tweets/"
    DRIVER_PATH = "/Users/mark/Documents/research/gersteinLab/TextMining-master/chromedriver"
    WEBSITE = "https://ieee-dataport.org/open-access/coronavirus-covid-19-geo-tagged-tweets-dataset"

    # local filenames of exports
    ID_FILENAME = "scraped_tweet_IDs_2020-03-20_2021-02-09.csv"
    DF_FILENAME = "scraped_tweet_IDs_and_scores_2020-03-20_2021-02-09.csv"
    LOCAL_EXPORT_ID_PATH = ID_PATH + ID_FILENAME
    LOCAL_EXPORT_DF_PATH = LOCAL_TWEET_PATH + DF_FILENAME
    AWS_EXPORT_ID_PATH = AWS_TWEET_DIR + "tweet_IDs/" + ID_FILENAME
    AWS_EXPORT_DF_PATH = AWS_TWEET_DIR + "raw_IEEE_tweet_scrapes/" + DF_FILENAME

    # scrape filenames and links to .csv files
    try:
        filename_list, links_list = get_links_from_website(WEBSITE,
                                                           DRIVER_PATH,
                                                           IEEE_USERNAME,
                                                           IEEE_PASSWORD)
    except Exception as e:
        print("Something wrong with scraping filenames and links on IEEE website.")
        print(e)

    # load tweets from list of links
    tweet_df_list = []
    tweet_IDs_list = []

    for link in links_list:
        tweet_df, tweet_IDs = get_tweetIDs_to_hydrate(link)
        tweet_df_list.append(tweet_df)
        tweet_IDs_list.append(tweet_IDs)

    # concatenate both the tweet IDs list and the tweet df list, each as one list or one df
    if len(tweet_IDs_list) > 1:
        merged_IDs = []
        for lst in tweet_IDs_list:
            for ID in lst:
                merged_IDs.append(ID)
    else:
        merged_IDs = tweet_IDs_list[0]

    if len(tweet_df_list) > 1:
        merged_tweet_dfs = pd.concat(tweet_df_list)
    else:
        merged_tweet_dfs = tweet_df_list[0]

    # export
    save_tweet_IDs(merged_IDs, LOCAL_EXPORT_ID_PATH)
    merged_tweet_dfs.to_csv(LOCAL_EXPORT_DF_PATH)

    # export to AWS
    try:
        # export list of IDs
        save_to_AWS(LOCAL_EXPORT_ID_PATH,
                    AWS_EXPORT_ID_PATH,
                    "s3",
                    AWS_BUCKET,
                    AWS_ACCESS,
                    AWS_SECRET)

        # export df of IDs + sentiment scores
        save_to_AWS(LOCAL_EXPORT_DF_PATH,
                    AWS_EXPORT_DF_PATH,
                    "s3",
                    AWS_BUCKET,
                    AWS_ACCESS,
                    AWS_SECRET)

        # remove local versions
        os.remove(LOCAL_EXPORT_ID_PATH)
        os.remove(LOCAL_EXPORT_DF_PATH)

    except Exception as e:
        print("Error in exporting the local files to AWS")
        print(e)
        print("------------------")
        raise ValueError(
            "Please fix the error in exporting the local files to AWS")
    finally:
        print(
            f"Finished with the execution of this 'scrape_tweets_daily.py' at (in UTC time): {datetime.datetime.utcnow()}")
