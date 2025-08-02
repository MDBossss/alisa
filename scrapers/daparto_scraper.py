from bs4 import BeautifulSoup

from utils.cloudscraper_utils import fetch_cloudflare_page


def scrape_daparto(part_number):
    print(f"[Daparto] Scraping products for part number: {part_number}...")

    url = f"https://www.daparto.de/Teilenummernsuche/Teile/Alle-Hersteller/{part_number}?ref=fulltext&sort=price"

    page = fetch_cloudflare_page(url)
    if not page:
        return []

    soup = BeautifulSoup(page.content, "html.parser")

    products_data = []
    products = soup.find_all("div", class_="spare-part")

    if not products:
        print("[Daparto] No products found for the given part number.")
        return []

    print(f"[Daparto] Found {len(products)} products for part number: {part_number}")

    for product in products:
        try:
            title = product.find("a", class_="spare-part-link").text.strip()
            product_link = product.find("a", class_="spare-part-link")["href"]
            price = product.find("strong", class_="value-price").text.strip()

            products_data.append({
                "source": "daparto",
                "price": price,
                "title": title,
                "link": product_link,
            })
        except AttributeError as e:
            print(f"[Daparto] Error parsing product data: {e}")
            continue

    return products_data
