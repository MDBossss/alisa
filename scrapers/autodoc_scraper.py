import os
from bs4 import BeautifulSoup
from utils.cloudscraper_utils import fetch_cloudflare_page

def scrape_autodoc(part_number):
    print(f"[Autodoc] Scraping products for part number: {part_number}...")
    
    url = f"https://www.autodoc.de/search?keyword={part_number}"
    
    page = fetch_cloudflare_page(url)
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
        # Use more robust parsing to handle cases where elements might be missing
        try: 
            # Get the main link element
            link_element = product.find("a", class_="listing-item__name")
            if link_element:
                product_link = link_element.get("href", "No Link Found")
                # Find the title element inside the link. It might be a font tag or not.
                title_element = link_element.find("font")
                if title_element:
                    title = title_element.text.strip()
                else:
                    title = link_element.text.strip()
            else:
                title = "No Title Found"
                product_link = "No Link Found"
            
            # Get the price element. It might be missing.
            price_element = product.find("div", class_="listing-item__price-new")
            if price_element:
                price = price_element.text.strip()
            else:
                price = "Price Not Available"
            
            # Check if any crucial data is missing before appending
            if title and product_link and price:
                products_data.append({
                    "source": "autodoc",
                    "price": price,
                    "title": title,
                    "link": product_link,
                })
            else:
                print(f"[Autodoc] Skipping product due to missing data: Title='{title}', Price='{price}', Link='{product_link}'")

        except AttributeError as e:
            # This catch is now less likely to trigger, but remains as a final safeguard
            print(f"[Autodoc] Error parsing product data: {e}. Skipping this product.")
            continue

    return products_data
