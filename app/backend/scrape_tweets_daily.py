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


if __name__ == "__main__":

    # get credentials, as env vars

    # IEEE_USERNAME
    # IEEE_PASSWORD

    # load tweets from website
    print("This part of the script loads the tweets from the website")

    #
