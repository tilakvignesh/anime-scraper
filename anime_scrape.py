from googlesearch import search
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_valid_url(url):

    """Check if a given URL is valid and contains the keywords for streaming anime

    :param url: URL to check
    :return: URL if valid, None otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout= 5)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.find('title')
            if any(keyword in title.text.lower() for keyword in ['free', 'stream', 'online', 'tv', 'series']):
                return url
        return None
    except:
        return None

def search_anime(anime_name, num):
    """
    Given an anime name, search for websites that could be used to stream that anime online for free.
    :param anime_name: Name of the anime to search for
    :param num: Number of results to search for
    :return: List of valid URLs that could be used to stream the anime
    """
    urls = search(f'{anime_name} free online stream', stop = num)
    op = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for url in urls:
            base = urlparse(url)
            base_url = base.scheme + '://' + base.netloc
            futures.append(executor.submit(check_valid_url, base_url))

        for future in as_completed(futures):
            result = future.result()
            if result and result not in op:
                op.append(result)

    return op


if __name__ == '__main__':
    anime = input('Enter the name of the anime: ')
    num = int(input('Enter the number of results you want to parse: '))
    potential_urls = search_anime(anime, num)
    for url in potential_urls:
        print(url)
    
    print(f'Total URLs found: {len(potential_urls)} out of {num} searches')
