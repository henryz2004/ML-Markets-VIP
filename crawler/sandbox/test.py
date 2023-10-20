import requests
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import concurrent.futures

class GoogleScraper:
    def __init__(self, query, start_date, end_date):
        self.query = query
        self.start_date = start_date
        self.end_date = end_date

    def url_generator(self, first_url, num_pages=10, results_per_page=10):
        parsed_url = urlparse(first_url)
        query_params = parse_qs(parsed_url.query)
        start_param = query_params.get('start', ['0'])[0]
        start_value = int(start_param)
        generated_urls = []
        generated_urls.append(first_url)
        for _ in range(num_pages):
            start_value += results_per_page
            query_params['start'] = str(start_value)
            updated_url = urlunparse(parsed_url._replace(query=urlencode(query_params, doseq=True)))
            generated_urls.append(updated_url)
        return generated_urls

    def extract_links(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        links = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = soup.select('.tF2Cxc')  # Use a more specific selector
            for result in search_results:
                link = result.a.get('href')
                if link and link.startswith("http") and "google" not in link:
                    links.append(link)
        return links

    def get_data(self):
        base_url = "https://www.google.com/search"
        params = {
            "q": self.query,
            "tbs": f"cdr:1,cd_min:{self.start_date},cd_max:{self.end_date}",
            "tbm": "nws"
        }
        url = f"{base_url}?{urlencode(params)}"
        urls = self.url_generator(url)
        news_links = []

        # Use concurrent processing to fetch links efficiently
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            link_lists = list(executor.map(self.extract_links, urls))
            for links in link_lists:
                news_links.extend(links)

        metadata_list = []
        for url in news_links:
            try:
                article = Article(url)
                article.download()
                article.parse()
                title = article.title
                description = article.meta_description
                publish_date = article.publish_date
                article_url = article.source_url
                metadata = {
                    "title": title,
                    "description": description,
                    "publish_date": publish_date,
                    "url": article_url
                }
                metadata_list.append(metadata)
            except Exception as e:
                continue
        return metadata_list
    

query = "ford stock"
start_date = "06/06/2020"
end_date = "06/06/2022"

newspaper = GoogleScraper(query, start_date, end_date)
data = newspaper.get_data()
print(data)
