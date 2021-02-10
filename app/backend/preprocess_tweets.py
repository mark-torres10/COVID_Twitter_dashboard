"""

    preprocess_tweets.py

    Cleans and preprocesses hydrated tweets (from AWS S3 bucket), uploads back to AWS.

"""
import pandas as pd
import emoji
import re
import nltk
from nltk.corpus import stopwords

import aws_helpers
from aws_helpers import save_to_AWS, load_from_AWS


def parse_location(location_dict):
    """
    Looks at location information and determines (1) if the location is in the USA or not and (2) if it
    is in the USA, what state is it in?

    Arg:
        location_dict: value from "place" field from tweet data (dict)
    Returns:   
        is_USA: is the location in the USA? (bool)
        country_location: country (str)
        state: if it is in the USA, which state is it in? (str)

    """

    if location_dict is None:
        return ("N/A", "N/A", "N/A")
    elif location_dict["country_code"] != "US":
        return (False, location_dict["country_code"], "N/A")
    else:
        # e.g., "Los Angeles, CA" --> "CA"
        state = location_dict["full_name"].split(",")[1].strip()
        return (True, "US", state)


def parse_dates(timestamp):
    """
    Processes the date information and extracts date and time information
    Arg:
        timestamp: timestamp of date + time (str)
    Returns:
        date: human-readable date (str) (e.g., "2021-02-09")
        year: calendar year (int)
        month: calendar month (str, "00" to "12")
        day: calendar day (int)
        hour: hour of day (int)

    """
    hour = pd.to_datetime(timestamp).hour
    dt_obj = pd.to_datetime(timestamp).date()
    year = dt_obj.year
    month = dt_obj.month
    day = dt_obj.day

    if month < 10:
        month = f"0{month}"

    month = str(month)

    date = f"{year}-{month}-{day}"

    return (date, year, month, day, hour)


def remove_emoji(text):
    """
    Removes emojis from a text

    Args:
        text: tweet/text to clean (str)
    Returns:
        clean_text: tweet/text without emojis (str)
    """

    text = text.encode("utf-8")
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode(
        'utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text


def clean_text(text):
    """
    Removes punctuation, does string split (tokenization) and removes links
    Args:
        text: tweet/text to clean (str)
    Returns:
        tokenized_text_arr: tokenized and cleaned text (list of strings)
    """

    PUNCTUATION = '''!()-[]{};:'"\,<>./?@$%^&*_~'''  # keep hashtags
    STOPWORDS = stopwords.words("english")

    # remove punctuation
    text_no_punctuation = ""

    for char in text:
        if char not in PUNCTUATION:
            text_no_punctuation = text_no_punctuation + char

    # remove emojis
    text_no_punctuation = remove_emoji(text_no_punctuation)

    # remove \n and \t
    text_no_punctuation = re.sub(r'\n', '', text_no_punctuation)
    text_no_punctuation = re.sub(r'\t', '', text_no_punctuation)

    # remove escape sequences
    text_no_escape = ""

    for char in text_no_punctuation:
        try:
            char.encode('ascii')
            # this'll catch chars that don't have an ascii equivalent (e.g., emojis)
            text_no_escape = text_no_escape + char
        except:
            pass

    # add space between # and another char before it (e.g., split yes#baseball into yes #baseball)
    text_no_escape = re.sub(r"([a-zA-Z0-9]){1}#", r"\1 #", text_no_escape)

    # string split
    text_arr = text_no_escape.split(' ')

    tokenized_text_arr = []

    for word in text_arr:

        word = word.lower()

        if "http" not in word and word.strip() != '' and word not in STOPWORDS:
            tokenized_text_arr.append(word)

    return tokenized_text_arr


def parse_hashtags(text):
    """
    Extracts both (1) the hashtags in a piece of text as well as 
    (2) the parts of the text that don't have a hashtag

    Args:
        text: tweet/piece of text (str)
    Return:
        hashtag_arr: array of hashtags (list of strings)
        non_hashtag_arr: array of non-hashtag words (list of strings)
    """
    hashtag_arr = []
    non_hashtag_arr = []

    tokenized_text_arr = text.split(' ')

    for word in tokenized_text_arr:
        if '#' in word:
            # how many hashtags are in the word?
            num_hashtags = 0
            for char in word:
                if char == '#':
                    num_hashtags += 1

            # if multiple hashtag words are squished together, split them on '#' and return the resulting words
            if num_hashtags > 1:
                word_arr = word.split('#')
                for inner_word in word_arr:
                    if inner_word != '#':
                        hashtag_arr.append("#" + inner_word)
            # else, if only one hashtag, add as is
            else:
                hashtag_arr.append(word)

        else:
            non_hashtag_arr.append(word)

    return (hashtag_arr, non_hashtag_arr)


def count_hashtags(text):
    """
    Counts the number of hashtags in a piece of text
    Args:
        text: tweet/piece of text (str)
    Return:
        count: number of hashtags (#s) in text
    """
    text_arr = text.split(' ')
    count = 0

    for word in text_arr:
        if '#' in word:
            count += 1

    return count


if __name__ == "__main__":

    # load tweets from AWS, use subset of cols
    tweets_df = ""
    tweets_df = tweets_df[["user", "created_at", "id",
                           "full_text", "geo", "coordinates",
                           "place", "retweet_count", "favorite_count"]]

    # initialize lists to hold information

    # loop through all rows, append information to corresponding list
