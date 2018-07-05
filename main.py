# Author: Alexander Hack
# Website: https://www.anhack.xyz
# Date: July 5, 2018
#
# Purpose: Figures out how commonly words appear
# in buzzfeed articles; to see if there is a trend


from collections import Counter
from bs4 import BeautifulSoup
import urllib2

target = "https://www.buzzfeed.com/"
words_printed = 15


def find_strings(soup):
    text_dump=""
    # Remove javascript
    [s.extract() for s in soup('script')]
    # Remove css
    [s.extract() for s in soup('style')]

    for text in soup.stripped_strings:
        text_dump += text + " "

    return text_dump.lower().replace('\\', '').replace('/', ' ').replace('-', ' ').replace('"', '').replace('\\u', ' \\u').split()

def load_article(link):
    try:
        html = urllib2.urlopen(link).read()
    except urllib2.URLError:
        print 'Failed to fetch ' + link

    try:
        soup = BeautifulSoup(html, 'lxml')
    except HTMLParser.HTMLParseError:
        print 'Failed to parse ' + link

    return soup

def parse_article(link):
    soup = load_article(link)
    stream = find_strings(soup)

    return stream

def find_articles():
    articles=[]
    soup = load_article(target)
    for article in soup.find_all('div', class_='js-card__content'):
        articles.append(article.div.a.get('href'))

    return articles

pool = []

# Get text from homepage
# And add it to the text pool
pool += parse_article(target)
# Find articles that are linked on the homepage
articles = find_articles()

# Populate word pool
for page_url in articles:
    pool += parse_article(target[:-1] + page_url)

# Clean up and print results
for word in Counter(pool).most_common(words_printed):
    print(': '.join(map(str, word)))


