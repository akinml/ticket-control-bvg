### all of the imports go into requirements!!!

import pandas as pd
import numpy as np
import string
from datetime import timedelta
from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk
import datetime as dt

nltk.download("punkt")
nltk.download("stopwords")
from ticket_control.params import path_to_data

# Load your existing database into a DataFrame
# Use flexible path so that it works on everyone's environment

# Chris Notes: Functions are applied on data. Not good practice to load the data inside of functions.
data = pd.read_csv(str(path_to_data) + "/database_telegram.csv", low_memory=False)

##Chris Notes: Define the input of functions and declare their datatype.
def data_preprocessing(data: pd.DataFrame):
    # Provide a Doc String why we have this function and what it does in simple terms.
    """This function is the first step in our Datapreprocessing pipeline. It takes the Telegram Database with the columns...."""

    # Notice the .copy() to copy the values
    data = data.copy()

    # replace sender type with str type
    data["sender"] = data["sender"].astype(str)
    data["date"] = data["date"].astype(str).str.strip("+00:00").str[0:16]
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    print(data.iloc[-1:, :])

    # Only consider most recent values, cut time in the beginning of the group
    start_date = dt.date(2019, 11, 1)
    data = data.loc[start_date:]

    # first round of cleaning na/empty strings/...
    data = data[data["text"].notna()]
    data["text"] = data["text"].str.strip()
    data["text"].replace("", np.nan, inplace=True)
    data.dropna(subset=["text"], inplace=True)

    # sorting values by sender & date
    df = data.sort_values(by=["sender", "date"])

    # creating a time difference
    df["time_diff"] = df.groupby("sender")["date"].diff()

    #
    data_clean = (
        df.groupby(["sender", (df["time_diff"] > timedelta(minutes=10)).cumsum()])
        .agg({"text": " ".join, "date": "first"})
        .reset_index()
    )

    data_clean["sender"] = data_clean["sender"].astype(str)
    # Chris Notes: Always import at the start of the Module.
    import re

    def remove_emojis(data):
        emoj = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002500-\U00002BEF"  # chinese char
            "\U00002702-\U000027B0"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u200d"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\ufe0f"  # dingbats
            "\u3030"
            "]+",
            re.UNICODE,
        )
        return re.sub(emoj, "", data)

    data_clean["text"] = data_clean["text"].apply(lambda x: remove_emojis(str(x)))

    # second round of cleaning na/empty strings/...
    data_clean = data_clean[data_clean["text"].notna()]
    data_clean["text"] = data_clean["text"].str.strip()
    data_clean["text"].replace("", np.nan, inplace=True)
    data_clean.dropna(subset=["text"], inplace=True)

    data_clean = data_clean.drop_duplicates()

    # lowercasing all strings
    data_clean["text"] = data_clean["text"].apply(lambda x: x.lower())

    # generating list of default stop words
    stop_words = set(stopwords.words("german"))

    # add multiple words using 'update'
    new_words_to_add = [
        "männlich",
        "weiblich",
        "gelesen",
        "weste",
        "westen",
        "shirt",
        "pulli",
        "jacke",
        "jacken",
        "ticket",
        "tickets",
        "eingestiegen",
        "ausgestiegen",
        "steigen",
        "schwarze",
        "schwarz",
        "männer",
        "haare",
        "the",
        "stehen",
        "gelesene",
        "blaue",
        "with",
        "wertend",
        "fahrgaesten",
        "fahrgaeste",
        "fahrgästen",
        "fahrgästen",
        "westlichen",
        "warnwesten",
        "gelbwesten",
        "abwertend",
        "blauwesten",
        "fahrgaesten",
        "wertende",
        "besten",
        "nichtwertende",
        "wuetend",
        "wütend",
        "wuetend",
        "wuetenden",
        "genau",
        "sicher",
        "ungenau",
        "sicherheitswesten",
        "westentraeger",
    ]
    stop_words.update(new_words_to_add)

    # Remove unwanted stopwords
    my_wanted_words = ["nach", "bei", "von", "vom" "zum", "über", "bis"]
    final_stopwords = stop_words - set(my_wanted_words)

    # Chris Notes: Not best practice to define functions inside of funcitons. Better to keep the definition separate and call the function within other functions.
    def stopword(text):
        word_tokens = word_tokenize(text)
        text = [
            w for w in word_tokens if not w in final_stopwords
        ]  ## if w isn't in final_stopwords, return w
        return " ".join(text)  ##transforming list into string again

    data_clean["text"] = data_clean["text"].apply(stopword)

    # removing punctuation
    for element in string.punctuation:
        data_clean["text"] = data_clean["text"].str.replace(element, "")

    # third round of cleaning na/empty strings/...
    data_clean["text"] = data_clean["text"].replace("", np.nan)
    data_clean["text"] = data_clean["text"].str.strip()
    data_clean.dropna(subset="text", inplace=True)
    data_clean = data_clean.drop_duplicates(subset="text")
    data_clean = data_clean[data_clean["text"] != ""]
    data_clean.dropna(subset="text", inplace=True)

    # replacing unwanted characters and words
    data_clean["text"] = data_clean["text"].str.replace("ß", "ss")
    data_clean["text"] = data_clean["text"].str.replace("ä", "ae")
    data_clean["text"] = data_clean["text"].str.replace("ö", "oe")
    data_clean["text"] = data_clean["text"].str.replace("ü", "ue")
    data_clean["text"] = data_clean["text"].str.replace("strasse", "str")
    data_clean["text"] = data_clean["text"].str.replace("alexanderplatz", "alex")
    data_clean["text"] = data_clean["text"].str.replace("zoologischer garten", "zoo")
    data_clean["text"] = data_clean["text"].str.replace("kottbusser", "kotti")
    data_clean["text"] = data_clean["text"].str.replace("goerlitzer", "goerli")

    # final sorting
    data_clean = data_clean.sort_values(by=["date", "sender"])

    # converting into "handover" file
    ##Chris Notes: Assign you objects names that indicate their type and state in the process.
    df_for_fuzzy_matching = data_clean.drop("time_diff", axis=1)

    return df_for_fuzzy_matching
