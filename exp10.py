import spacy
from textblob import TextBlob

def sentiment_analysis(review):
    def preprocessing_text(text):
        doc = sp(text.lower())
        tokens = [token for token in doc if not token.is_stop and not token.is_digit and not token.is_punct]
        tokens = [token.lemma_ for token in tokens]
        return ' '.join(tokens)

    def get_sentiment(text):
        return TextBlob(text).sentiment.polarity

    def find_solution(text):
        for keyword, solution in keyword_solutions.items():
            # print(keyword, solution)
            if keyword.lower() in text.lower():
                return solution
        return 'Contact customer care.'

    sp = spacy.load('en_core_web_sm')

    processed_review = preprocessing_text(review)
    # print(processed_review)
    polarity = get_sentiment(processed_review)

    # print(polarity)

    if polarity > 0:
        print('positive review')
        return
    else:
        keyword_solutions = {
            'oil': 'It is the natural oil present in peanut. There is no extra oil added. Place the container upside down for sometime for the oil to mix.',
            'oily': 'It is the natural oil present in peanut. There is no extra oil added. Place the container upside down for sometime for the oil to mix.',
            'leak': 'Send images with proof to customer support for further assistance.',
            'flavour': 'Try our flavoured peanut butter range next time. This one does not have any additives.',
            'consistent': 'Mix well with a spoon.',
            'package': 'Send images with proof to customer support for further assistance.',
            'flavor': 'Try our flavoured peanut butter range next time. This one does not have any additives.',
            'consistency': 'Mix well with a spoon.',
            'expire': 'Refrigerate for long lasting freshness.'
        }

        print(f'Solution: {find_solution(processed_review)}')

review = input('Enter a review: ')
sentiment_analysis(review)