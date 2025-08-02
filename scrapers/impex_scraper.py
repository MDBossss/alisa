from bs4 import BeautifulSoup
from utils.web_utils import fetch_page

def scrape_impex(part_number):
    url = f"https://impexautodijelovi.hr/trazi?sort=priceAsc&search={part_number}"

    print(f"[Impex] Scraping products for part number: {part_number}...")

    page = fetch_page(url)
    if not page:
        return []

    soup = BeautifulSoup(page.content, "html.parser")

    products_data = []
    products = soup.find_all("section", class_="productInline")

    if not products:
        print("[Impex] No products found for the given part number.")
        return []

    print(f"[Impex] Found {len(products)} products for part number: {part_number}")

    for product in products:
        try:
            title = product.find("h2", class_="heading").find("a").text.strip()
            product_link = product.find("h2", class_="heading").find("a")["href"]
            price = product.find("span", class_="price__primary").text.strip()

            products_data.append({
                "source": "impex",
                "price": price,
                "title": title,
                "link": product_link,
            })
        except AttributeError as e:
            print(f"[Impex] Error parsing product data: {e}")
            continue

    return products_data

    