from flask import Flask, render_template, request, redirect, url_for
from joblib import load
from tweets import TwitterClient
import re
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from get_tweets import get_related_tweets
import pandas as pd


pipeline = load("text_classification (3).joblib")

def remove_pattern(text, pattern_regex):
        r = re.findall(pattern_regex, text)
        for i in r:
            text = re.sub(i, '', text)
    
        return text

def requestResults1(name):
    selenium_client = TwitterClient()
    tweets_df = selenium_client.get_tweets(name)
    print("tweest rsult ",tweets_df)

    tweets_df['tidy_tweets'] = np.vectorize(remove_pattern)(tweets_df['tweets'], "@[\w]*: | *RT*")
    cleaned_tweets = []

    for index, row in tweets_df.iterrows():
     # Here we are filtering out all the words that contains link
        words_without_links = [word for word in row.tidy_tweets.split()        if 'http' not in word]
        cleaned_tweets.append(' '.join(words_without_links))

    tweets_df['tidy_tweets'] = cleaned_tweets
    tweets_df.drop_duplicates(subset=['tidy_tweets'], keep=False)
    tweets_df['absolute_tidy_tweets'] = tweets_df['tidy_tweets'].str.replace("[^a-zA-Z# ]", "")
    # nltk.download('all')

    # Tokenization
    tokenized_tweet = tweets_df['absolute_tidy_tweets'].apply(lambda x: x.split())
    # Finding Lemma for each word
    word_lemmatizer = WordNetLemmatizer()
    tokenized_tweet = tokenized_tweet.apply(lambda x: [word_lemmatizer.lemmatize(i) for i in x])
    #joining words into sentences (from where they came from)
    for i, tokens in enumerate(tokenized_tweet):
        tokenized_tweet[i] = ' '.join(tokens)

    tweets_df['absolute_tidy_tweets'] = tokenized_tweet

    bow_word_vectorizer = CountVectorizer(max_df=0.90, min_df=2, stop_words='english', max_features=50)
    # bag-of-words feature matrix
    bow_word_feature = bow_word_vectorizer.fit_transform(tweets_df['absolute_tidy_tweets'])

    tweets_df['prediction'] = pipeline.predict(bow_word_feature.toarray())
    #data = str(tweets_df.prediction.value_counts()) + '\n\n'
    tweets_df.drop(['tidy_tweets','absolute_tidy_tweets'],axis=1,inplace=True)
    tweets_df['prediction'] = tweets_df['prediction'].replace({'0':'Negative', 0:'Negative','1':'positive',1:'positive','-1':'neutral',-1:'neutral'})
    return tweets_df

def requestResults(name):
    tweets = get_related_tweets(name)
    tweets['prediction'] = pipeline.predict(tweets['tweet_text'])
    data = str(tweets.prediction.value_counts()) + '\n\n'
    return data + str(tweets)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        print(request)
        user = request.form['search']
        return redirect(url_for('success', name=user))


@app.route('/success/<name>')
def success(name):
    data=requestResults1(name)
    # datadf=pd.DataFrame(data=data)
    # print(type(data))
    # return render_template('home.html', data="<xmp>" + str(requestResults1(name)) + " </xmp> ")
    return render_template('home.html',  tables=[data.to_html(classes='data')], titles=data.columns.values)
    # return "<xmp>" + requestResults1(name) + " </xmp> "


if __name__ == '__main__' :
    app.run(debug=True)