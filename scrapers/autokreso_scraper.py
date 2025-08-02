from bs4 import BeautifulSoup
from utils.web_utils import fetch_page

def scrape_autokreso(part_number):
    url = f"https://www.autokreso.hr/?orderby=price&paged=1&s={part_number}+&post_type=product"

    print(f"[AutoKrešo] Scraping products for part number: {part_number}...")

    page = fetch_page(url)
    if not page: 
        return []

    soup = BeautifulSoup(page.content, "html.parser")

    products_data = []
    products = soup.find_all("div", class_="product")

    if not products:
        print("[AutoKrešo] No products found for the given part number.")
        return []

    print(f"[AutoKrešo] Found {len(products)} products for part number: {part_number}")

    for product in products:
        try:
            title = product.find("p", class_="product-title").find("a").text.strip()
            product_link = product.find("p", class_="product-title").find("a")["href"]
            price = product.find("div", class_="ProductPrice").text.strip().replace(" ","")

            products_data.append({
                "source": "autokreso",
                "price": price,
                "title": title,
                "link": product_link,
            })
        except AttributeError as e:
            print(f"[Autokrešo] Error parsing product data: {e}")
            continue
    return products_data
