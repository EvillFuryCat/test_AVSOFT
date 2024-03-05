from urllib.parse import urljoin, urlparse
import requests
import os
from bs4 import BeautifulSoup


visited_urls = set()
start_url = "https://fly-z-one.ru/"


def download_page(url: str):
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return
        
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        for link in soup.find_all('a'):
            next_link = link.get('href')
            if next_link:
                next_link = urljoin(url, next_link)
                if urlparse(next_link).netloc == urlparse(url).netloc:
                        download_page(next_link)
                
        file_path = os.path.join("../resource/search", f"{url.replace('/', '_').replace(':', '')}")
        with open(file_path, "w") as file:
            file.write(content)
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        

download_page(start_url)