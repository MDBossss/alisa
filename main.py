from utils.xls_utils import save_to_excel

from scrapers.autokreso_scraper import scrape_autokreso
from scrapers.impex_scraper import scrape_impex
from scrapers.autodoc_scraper import scrape_autodoc
from scrapers.daparto_scraper import scrape_daparto

# example part number: 55183562 

partNumber = 55183562

# partNumber = input("Enter the part number: ").strip()


products_impex = scrape_impex(partNumber)
products_kreso = scrape_autokreso(partNumber)
products_autodoc = scrape_autodoc(partNumber)

products = products_kreso + products_impex + products_autodoc

sorted_products = sorted(products, key=lambda x: x['price'])

if sorted_products:
    save_to_excel(sorted_products, sheet_name=partNumber, filename=f"parts_list.xlsx")
    
