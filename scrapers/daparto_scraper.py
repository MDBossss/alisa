from bs4 import BeautifulSoup
import logging

from utils.cloudscraper_utils import fetch_cloudflare_page
from utils.clean_price import clean_price


def scrape_daparto(part_number, cookie=None):
    print(f"[Daparto] Scraping products for part number: {part_number}...")

    url = f"https://www.daparto.de/Teilenummernsuche/Teile/Alle-Hersteller/{part_number}?ref=fulltext&sort=price"

    cookies = {
    "cf_clearance": cookie,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.6',
        'Referer': 'https://www.daparto.de/',
        'Sec-CH-UA': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        'Sec-CH-UA-Arch': '"x86"',
        'Sec-CH-UA-Bitness': '"64"',
        'Sec-CH-UA-Full-Version-List': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.0.0", "Brave";v="138.0.0.0"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Model': '""',
        'Sec-CH-UA-Platform': '"Windows"',
        'Sec-CH-UA-Platform-Version': '"10.0.0"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
    }


    page = fetch_cloudflare_page(url, cookies=cookies, headers=headers)
    if not page:
        raise ValueError("Daparto fetch failed (possible 403 or bad cookie)")

    soup = BeautifulSoup(page.content, "html.parser")

    products_data = []
    products = soup.find_all("div", class_="spare-part")

    if not products:
        print("[Daparto] No products found for the given part number.")
        return []

    print(f"[Daparto] Found {len(products)} products for part number: {part_number}")

    for product in products:
        try:
            link_element = product.find("span", class_="link")
            title = link_element.text.strip().replace("  ","")
            product_link = link_element.get("data-href", "")
            price = clean_price(product.find("div", class_="price").text.strip())

            products_data.append({
                "source": "daparto",
                "price": price,
                "title": title,
                "link": f"https://www.daparto.de{product_link}",
            })
        except AttributeError as e:
            print(f"[Daparto] Error parsing product data: {e}")
            continue

    return products_data
