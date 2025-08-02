from bs4 import BeautifulSoup
from utils.web_utils import fetch_page

def scrape_autodoc(part_number):
    url = f"https://www.autodoc.de/search?keyword={part_number}"

    print(f"[Autodoc] Scraping products for part number: {part_number}...")

    page = fetch_page(url)
    if not page: 
        return []

    soup = BeautifulSoup(page.content, "html.parser")

    products_data = []
    products = soup.find_all("div", class_="listing-item")

    if not products:
        print("[Autodoc] No products found for the given part number.")
        return []

    print(f"[Autodoc] Found {len(products)} products for part number: {part_number}")

    for product in products:
        try: 
            title = product.find("a", class_="listing-item__name").find("font").text.strip()
            product_link = product.find("a", class_="listing-item__name")["href"]
            price = product.find("div", class_="listing-item__price-new").text.strip()

            products_data.append({
                "source": "autodoc",
                "price": price,
                "title": title,
                "link": product_link,
            })
        except AttributeError as e:
            print(f"[Autodoc] Error parsing product data: {e}")
            continue
    return products_data