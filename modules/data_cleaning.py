### all of the imports go into requirements!!!

import pandas as pd
import numpy as np
import string
from datetime import timedelta
from nltk.corpus import stopwords
from nltk import word_tokenize



def data_preprocessing():
    # Load your existing database into a DataFrame
    data = pd.read_csv('/home/yannik/ticket-control-bvg/data/telegram_data.csv')  # Replace with the path to your database file
    # Notice the .copy() to copy the values
    data = data.copy()

    # replace sender type with str type
    data['sender'] = data['sender'].astype(str)

    # convert date to datetime format
    data["date"] = pd.to_datetime(data["date"])

    # first round of cleaning na/empty strings/...
    data = data[data['text'].notna()]
    data['text'] = data['text'].str.strip()
    data['text'].replace('', np.nan, inplace=True)
    data.dropna(subset=['text'], inplace=True)

    # sorting values by sender & date
    df = data.sort_values(by=['sender', 'date'])

    # creating a time difference
    df['time_diff'] = df.groupby('sender')['date'].diff()

    #
    data_clean = df.groupby(['sender', (df['time_diff'] > timedelta(minutes=10)).cumsum()]).agg({'text': ' '.join,
                                                                                            'date': 'first'}).reset_index()


    data_clean['sender'] = data_clean['sender'].astype(str)

    import re
    def remove_emojis(data):
        emoj = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
                        "]+", re.UNICODE)
        return re.sub(emoj, '', data)

    data_clean['text']= data_clean['text'].apply(lambda x: remove_emojis(str(x)))

    # second round of cleaning na/empty strings/...
    data_clean = data_clean[data_clean['text'].notna()]
    data_clean['text'] = data_clean['text'].str.strip()
    data_clean['text'].replace('', np.nan, inplace=True)
    data_clean.dropna(subset=['text'], inplace=True)


    data_clean = data_clean.drop_duplicates()

    # lowercasing all strings
    data_clean['text']= data_clean['text'].apply(lambda x: x.lower())

    # generating list of default stop words
    stop_words = set(stopwords.words('german'))

    # Customizing a list of stopwords
    my_stopwords = stop_words.copy()  # Create a copy of the stop_words list

    # Add other stopwords
    my_stopwords.add('männlich')
    my_stopwords.add('weiblich')
    my_stopwords.add('gelesen')
    my_stopwords.add('weste')
    my_stopwords.add('shirt')
    my_stopwords.add('pulli')
    my_stopwords.add('jacke')
    my_stopwords.add('jacken')
    my_stopwords.add('westen')
    my_stopwords.add('ticket')
    my_stopwords.add('tickets')
    my_stopwords.add('eingestiegen')

    # Remove unwanted stopwords
    my_wanted_words = ['nach', 'bei', 'von', 'vom' 'zum', 'über', 'bis']
    final_stopwords = my_stopwords - set(my_wanted_words)

    def stopword(text):
        word_tokens = word_tokenize(text)
        text = [w for w in word_tokens if not w in final_stopwords]  ## if w isn't in final_stopwords, return w
        return ' '.join(text)  ##transforming list into string again

    data_clean['text'] = data_clean['text'].apply(stopword)

    # removing punctuation
    for element in string.punctuation:
        data_clean['text'] = data_clean['text'].str.replace(element, '')

    # third round of cleaning na/empty strings/...
    data_clean['text'] = data_clean['text'].replace('', np.nan)
    data_clean['text'] = data_clean['text'].str.strip()
    data_clean.dropna(subset='text', inplace=True)
    data_clean = data_clean.drop_duplicates(subset='text')
    data_clean = data_clean[data_clean['text'] != '']
    data_clean.dropna(subset='text', inplace=True)

    # replacing unwanted characters and words
    data_clean['text'] = data_clean['text'].str.replace('ß', 'ss')
    data_clean['text'] = data_clean['text'].str.replace('ä', 'ae')
    data_clean['text'] = data_clean['text'].str.replace('ö', 'oe')
    data_clean['text'] = data_clean['text'].str.replace('ü', 'ue')
    data_clean['text'] = data_clean['text'].str.replace('strasse', 'str')
    data_clean['text'] = data_clean['text'].str.replace('alexanderplatz', 'alex')
    data_clean['text'] = data_clean['text'].str.replace('zoologischer garten', 'zoo')
    data_clean['text'] = data_clean['text'].str.replace('kottbusser', 'kotti')
    data_clean['text'] = data_clean['text'].str.replace('goerlitzer', 'goerli')


    #final sorting
    data_clean = data_clean.sort_values(by=['date', 'sender'])

    # converting into "handover" file
    data_handover = data_clean.drop('time_diff', axis=1)

    return data_handover