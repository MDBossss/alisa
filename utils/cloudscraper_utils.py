import cloudscraper
import time
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    #'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.autodoc.de/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}

# Create a single scraper instance that can be reused across requests.
# This makes it more efficient than creating a new one for every request.
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

def fetch_cloudflare_page(url):
    """
    Fetches a URL using cloudscraper to bypass Cloudflare protection.
    """
    time.sleep(random.uniform(1, 3)) 

    try:
        # Use the global scraper instance to make the request
        page = scraper.get(url, headers=HEADERS, timeout=15)
        page.raise_for_status() # Raise an exception for bad status codes
        return page
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
