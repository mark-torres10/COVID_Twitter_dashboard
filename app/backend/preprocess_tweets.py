"""

    preprocess_tweets.py

    Cleans and preprocesses hydrated tweets (from AWS S3 bucket), uploads back to AWS.

"""
import os
import ast
import pandas as pd
import emoji
import re
import nltk
import datetime
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
        try:
            # e.g., "Los Angeles, CA" --> "CA"
            state = location_dict["full_name"].split(",")[1].strip()
        except Exception as e:
            # sometimes it just denotes the full name as "United States"
            state = location_dict["full_name"].strip()
        finally:
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


def try_literal_eval(text):
    """
    Tries to use ast's literal_eval function to 
    evaluate a string into its literal representation (e.g., 'dict')

    Arg:
        text: string representation
    Returns:
        eval: literal representation of parsed string
    """
    try:
        eval = ast.literal_eval(text)
    except Exception as e:
        eval = None

    return eval


if __name__ == "__main__":

    # change dir to this file's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # get env vars
    AWS_BUCKET = os.environ["AWS_BUCKET"]
    AWS_ACCESS = os.environ["AWS_ACCESS"]
    AWS_SECRET = os.environ["AWS_SECRET"]

    # initialize paths
    AWS_TWEET_DIR = "tweet_scrapes/"
    HYDRATED_TWEETS_PATH = "./../../tweets/hydrated_tweets/"
    PREPROCESSED_TWEETS_PATH = "./../../tweets/preprocessed_tweets/"

    # full paths of files
    HYDRATED_TWEETS_FILENAME = "hydrated_tweets_2020-03-20_2021-02-09.csv"
    PREPROCESSED_TWEETS_FILENAME = "preprocessed_tweets_2020-03-20_2021-02-09.csv"
    LOCAL_HYDRATED_TWEETS_PATH = HYDRATED_TWEETS_PATH + HYDRATED_TWEETS_FILENAME
    LOCAL_PREPROCESSED_TWEETS_PATH = PREPROCESSED_TWEETS_PATH + \
        PREPROCESSED_TWEETS_FILENAME

    AWS_HYDRATED_TWEETS_PATH = AWS_TWEET_DIR + \
        "hydrated_tweets/" + HYDRATED_TWEETS_FILENAME
    AWS_PREPROCESSED_TWEETS_PATH = AWS_TWEET_DIR + \
        "preprocessed_tweets/" + PREPROCESSED_TWEETS_FILENAME

    # load tweets from AWS, use subset of cols
    # for now, can choose to use local version of file, rather than manually load it

    use_local = True
    if use_local:
        tweets_df = pd.read_csv(LOCAL_HYDRATED_TWEETS_PATH)
    else:
        tweets_df = pd.read_csv(AWS_HYDRATED_TWEETS_PATH)

    tweets_df = tweets_df[["user", "created_at", "id",
                           "full_text", "geo", "coordinates",
                           "place", "retweet_count", "favorite_count"]]

    print(f"Parsing {tweets_df.shape[0]} tweets today...")

    # change place col to be read as dict, not str
    tweets_df["place"] = tweets_df["place"].apply(
        lambda x: try_literal_eval(x))

    # initialize lists to hold information
    is_USA_list = []
    country_location_list = []
    state_location_list = []
    dates_list = []
    year_list = []
    month_list = []
    day_list = []
    hour_list = []
    tokenized_text_list = []
    hashtags_list = []
    non_hashtags_list = []
    hashtag_counts_list = []

    # loop through the location column, get location information
    for idx, location_dict in enumerate(tweets_df["place"]):

        try:
            is_USA, country, state = parse_location(location_dict)

            is_USA_list.append(is_USA)
            country_location_list.append(country)
            state_location_list.append(state)
        except Exception as e:
            print("Error in looping through locations column and getting locations")
            print(f"Error happened at index {idx}\n")
            print(f"The location was: {location_dict}\n")
            print(f"The error was: {e}\n")
            if type(location_dict) == int:
                is_USA_list.append("N/A")
                country_location_list.append("N/A")
                state_location_list.append("N/A")
                continue
            else:
                raise ValueError(
                    "Please address error in looping through locations column")

    # loop through the dates column, get date info
    for idx, timestamp in enumerate(tweets_df["created_at"]):

        try:
            date, year, month, day, hour = parse_dates(timestamp)

            dates_list.append(date)
            year_list.append(year)
            month_list.append(month)
            day_list.append(day)
            hour_list.append(hour)
        except Exception as e:
            print("Error in looping through dates column and getting dates")
            print(f"Error happened at index {idx}\n")
            print(f"The timestamp was: {timestamp}\n")
            print(f"The error was: {e}\n")

            dates_list.append("N/A")
            year_list.append("N/A")
            month_list.append("N/A")
            day_list.append("N/A")
            hour_list.append("N/A")

    # loop through the text column, get parsed text
    for idx, text in enumerate(tweets_df["full_text"]):

        try:
            # cleaned, tokenized text
            tokenized_text_arr = clean_text(text)
            tokenized_text_list.append(tokenized_text_arr)

            # get hashtags
            hashtag_arr, non_hashtag_arr = parse_hashtags(text)
            hashtags_list.append(hashtag_arr)
            non_hashtags_list.append(non_hashtag_arr)

            # get hashtag counts
            hashtag_count = count_hashtags(text)
            hashtag_counts_list.append(hashtag_count)

        except Exception as e:
            print("Error in looping through text column and getting parsed text")
            print(f"Error happened at index {idx}\n")
            print(f"The text was: {text}\n")
            print(f"The error was: {e}\n")
            raise ValueError(
                "Please address error in looping through text column")

    # add lists as columns to our df
    tweets_df["is_USA"] = is_USA_list
    tweets_df["country"] = country_location_list
    tweets_df["state"] = state_location_list
    tweets_df["date"] = dates_list
    tweets_df["year"] = year_list
    tweets_df["month"] = month_list
    tweets_df["day"] = day_list
    tweets_df["hour"] = hour_list
    tweets_df["tokenized_text"] = tokenized_text_list
    tweets_df["hashtags_list"] = hashtags_list
    tweets_df["non_hashtags_list"] = non_hashtags_list
    tweets_df["hashtag_count"] = hashtag_counts_list

    # export df as local .csv file
    try:
        tweets_df.to_csv(LOCAL_PREPROCESSED_TWEETS_PATH)
    except Exception as e:
        print("Problem with exporting tweets df as local file")
        print(e)
        raise ValueError(
            "Please address issue with exporting tweets df as local file")

    # export df to AWS bucket
    try:
        # save to AWS
        save_to_AWS(LOCAL_PREPROCESSED_TWEETS_PATH,
                    AWS_PREPROCESSED_TWEETS_PATH,
                    "s3",
                    AWS_BUCKET,
                    AWS_ACCESS,
                    AWS_SECRET)

        # remove local version
        os.remove(LOCAL_PREPROCESSED_TWEETS_PATH)
    except Exception as e:
        print("Error in exporting the local files to AWS")
        print(e)
        print("------------------")
        raise ValueError(
            "Please fix the error in exporting the local files to AWS")
    finally:
        print(
            f"Finished with the execution of 'preprocess_tweets.py' at (in UTC time): {datetime.datetime.utcnow()}")
