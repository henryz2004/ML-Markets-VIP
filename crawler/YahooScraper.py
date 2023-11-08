import re
from time import sleep
from bs4 import BeautifulSoup
import requests

class YahooScraper: 
    def __init__(self, query, start_date, end_date):
        self.query = query
        self.start_date = start_date
        self.end_date = end_date
      
    def get_data(self, numpages = 5):
        base_url = 'https://news.search.yahoo.com/search?p={}'
        url = base_url.format(self.query)
        articles = []
        links = set()
        
        for i in range (0, numpages):
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', 'NewsArticle')
            
            for card in cards:
                article = extract_metadata(card)
                articles.append(article)        
                    
            try:
                url = soup.find('a', 'next').get('href')
            except AttributeError:
                break
        
        return articles
    
headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.google.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
}

def extract_metadata(card):
    headline = card.find('h4', 's-title').text
    posted = card.find('span', 's-time').text.replace('·', '').strip()
    description = card.find('p', 's-desc').text.strip()
    raw_link = card.find('a').get('href')
    unquoted_link = requests.utils.unquote(raw_link)
    pattern = re.compile(r'RU=(.+)\/RK')
    match = re.search(pattern, unquoted_link)
    if match:
        clean_link = match.group(1)
    else:
        clean_link = None
   
    metadata = {
      "title": headline,
      "description": description,
      "publish_date": posted,
      "url": clean_link
    }

  
    return metadata

query = "ford stock"
start_date = "06/06/2020"
end_date = "06/06/2022"

YScraper = YahooScraper(query, start_date, end_date)
articles = YScraper.get_data()
print(articles)