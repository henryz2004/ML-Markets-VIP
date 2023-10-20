import requests
from newspaper import Article
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def url_generator(first_url, num_pages=10, results_per_page=10):
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


def link_scraper(query, start_date, end_date):
    base_url = "https://www.google.com/search"
    params = {
        "q": query,
        "tbs": f"cdr:1,cd_min:{start_date},cd_max:{end_date}",
        "tbm": "nws"
    }

    
    url = f"{base_url}?{urlencode(params)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }

    urls = url_generator(url)
    news_links = []
    for link in urls:
        response = requests.get(link, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = soup.find_all("a")
            for result in search_results:
                link = result.get("href")
                if link and link.startswith("http") and "google" not in link:
                    news_links.append(link)

    return news_links

def get_data():
    urls = link_scraper(query, start_date, end_date)
    metadata_list = []

    for url in urls:
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

        except (Exception) as e:
            continue

    return metadata_list

if __name__ == "__main__":
    query = "dogs"
    start_date = "8/8/2022"  # Format: MM/DD/YYYY
    end_date = "11/4/2022"   # Format: MM/DD/YYYY
    print(get_data())
