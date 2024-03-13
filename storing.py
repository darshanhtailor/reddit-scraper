import csv
from pymongo import MongoClient

client = MongoClient('mongodb+srv://darshan:12345@cluster0.potuzln.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client['sma']

collection = db['reddit_data']

collection.delete_many({})

with open('cleaned_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        collection.insert_one(row)

print('CSV data has been stored in MongoDB')