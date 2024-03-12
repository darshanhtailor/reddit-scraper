import requests
from bs4 import BeautifulSoup
import csv
import time

def scraper(url):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'}
    page = requests.get(url, headers=headers)

    return page.text


def parser(html, parsed_data, itr):
    soup = BeautifulSoup(html, 'html.parser')
    curr = []

    ignore_subreddit_searches = 0
    titles = soup.find_all(class_='search-title')
    for title in titles:
        if itr == 1 and ignore_subreddit_searches < 3:
            ignore_subreddit_searches += 1
        else:
            curr.append({
                'title': title.text,
                'url': title.get('href')
            })

    i = 0
    scores = soup.find_all(class_='search-score')
    for score in scores:
        curr[i]['points'] = score.text
        i += 1

    i = 0
    comments = soup.find_all(class_='search-comments')
    for comment in comments:
        curr[i]['comments'] = comment.text
        i += 1

    ignore_subreddit_searches = 0
    i = 0
    times = soup.find_all(class_='search-time')
    for time in times:
        if itr == 1 and ignore_subreddit_searches < 3:
            ignore_subreddit_searches += 1
        else:
            tags = time.find_all() 
            curr[i]['time'] = tags[0].get('datetime')
            i += 1

    ignore_subreddit_searches = 0
    i = 0
    mediaLinks = soup.find_all(class_='search-link')
    for mediaLink in mediaLinks:
        if itr == 1 and ignore_subreddit_searches < 3:
            ignore_subreddit_searches += 1
        else:
            curr[i]['media_url'] = mediaLink.text
            i += 1
    

    parsed_data += curr


def next_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    nextLinks = soup.find_all(class_='nextprev')
    nextLinks.reverse()

    tags = nextLinks[0].find_all()
    tags.reverse()

    return tags[0].get('href')


site = 'https://old.reddit.com'
q = 'ipl'
sort = 'top'
t = 'month'
url = f'{site}/search/?q={q}&sort={sort}&t={t}'

parsed_data = []

for i in range(5):
    html = scraper(url)
    parser(html, parsed_data, i+1)
    url = next_url(html)
    print(f'Page {i+1} scraped and parsed')
    time.sleep(2)


field_names = ['title', 'url', 'points', 'comments', 'time', 'media_url']
file_name = 'reddit_data.csv'

with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(parsed_data)

print('CSV file saved')