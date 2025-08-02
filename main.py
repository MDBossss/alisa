from scrapers.autokreso_scraper import scrape_autokreso
from utils.xls_utils import save_to_excel

partNumber = input("Enter the part number: ").strip()

products = scrape_autokreso(partNumber)
if products:
    save_to_excel(products, sheet_name=partNumber, filename=f"{partNumber}_autokreso.xlsx")
    
