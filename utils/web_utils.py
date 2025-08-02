import requests
import time
import random


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    #'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def fetch_page(url):
    time.sleep(random.uniform(1, 3)) 

    try:
        page = requests.get(url, headers=headers, timeout=10)
        page.raise_for_status()  # Raise an error for bad responses
        return page
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    