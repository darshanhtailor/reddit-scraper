import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import spacy
from textblob import TextBlob


def parser():
    with open("reviews.html", "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')

    reviews = soup.find_all(class_='review-text-content')
    extracted_reviews = []
    for review in reviews:
        extracted_reviews.append(review.text)

    print(extracted_reviews)

    extracted_reviews = [extracted_review[1:-1] for extracted_review in extracted_reviews]

    with open('reviews.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # writer.writerow('reviews')
        for extracted_review in extracted_reviews:
            writer.writerow([extracted_review])


def sentiment_analysis():
    def preprocessing_text(text):
        doc = sp(text.lower())
        tokens = [token for token in doc if not token.is_stop and not token.is_digit and not token.is_punct]
        tokens = [token.lemma_ for token in tokens]
        return ' '.join(tokens)

    def get_sentiment(text):
        return TextBlob(text).sentiment.polarity


    df = pd.read_csv('reviews.csv')    
    df = df.dropna()

    sp = spacy.load('en_core_web_sm')
    df['processed_reviews'] = df['reviews'].apply(preprocessing_text)

    df['polarity'] = df['processed_reviews'].apply(get_sentiment)


    sentiment_list = []
    pos = 0
    neg = 0
    neu = 0

    for num in df['polarity']:
        if num > 0:
            pos = pos + 1
            sentiment_list.append('Positive')

        elif num < 0:
            neg = neg + 1
            sentiment_list.append('Negative')

        else:
            neu = neu + 1
            sentiment_list.append('Neutral')

    df['sentiment'] = sentiment_list

    print("Total positive opinions:", pos)
    print("Total negative opinions:", neg)
    print("Total neutral opinions:", neu)

    print("Positive Sentiments:")
    print(df[df['sentiment'] == 'Positive'].head())

    print("\nNegative Sentiments:")
    print(df[df['sentiment'] == 'Negative'].head())

    print("\nNeutral Sentiments:")
    print(df[df['sentiment'] == 'Neutral'].head())


# parser()
sentiment_analysis()

