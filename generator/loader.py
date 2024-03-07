from urllib.parse import urljoin, urlparse
import requests
import os
import json
from bs4 import BeautifulSoup


with open('config.json', 'r') as file:
    config_data = json.load(file)


start_url = config_data["start_url"]
urls_to_visit = [start_url]
visited_urls = set()

while urls_to_visit:
    url = urls_to_visit.pop(0)
    
    if url in visited_urls:
        continue
        
    visited_urls.add(url)
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            response.raise_for_status()
  
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        for link in soup.find_all('a'):
            next_link = link.get('href')
            if next_link:
                next_link = urljoin(url, next_link)
                if urlparse(next_link).netloc == urlparse(url).netloc:
                    urls_to_visit.append(next_link)
                
        file_path = os.path.join("../resource/search", f"{url.replace('/', '_').replace(':', '')}")
        with open(file_path, "w") as file:
            file.write(content)
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")