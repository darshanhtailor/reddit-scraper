import pandas as pd

df = pd.read_csv('reddit_data.csv')

deleted_count = 0
seen_urls = {'url'}

for index, row in df.iterrows():
    url = row['url']
    if url in seen_urls:
        df.drop(index, inplace=True)
        deleted_count += 1
    else:
        seen_urls.add(url)

print("Count of deleted rows:", deleted_count)

df.to_csv('cleaned_data.csv', index=False)