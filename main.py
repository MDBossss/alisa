from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.xls_utils import save_to_excel
from datetime import date

from scrapers.autokreso_scraper import scrape_autokreso
from scrapers.impex_scraper import scrape_impex
from scrapers.autodoc_scraper import scrape_autodoc
from scrapers.daparto_scraper import scrape_daparto

# # example part number: 55183562 

app = Flask(__name__)
CORS(app)

@app.route("/trigger", methods=["POST"])
def trigger():
    data = request.get_json()

    cf_clearance_cookie = data.get("cf_clearance_cookie")
    if not cf_clearance_cookie:
        return jsonify({"status": "error", "message": "Daparto Cloudflare cookie not received"}), 400
    
    part_number = data.get("part_number")
    if not part_number:
        return jsonify({"status": "error", "message": "Part number(s) is required"}), 400


    try:
        # daparto first, if returns 403, redo cookie and dont start others
        products_daparto = scrape_daparto(part_number, cookie=cf_clearance_cookie)

        products_impex = scrape_impex(part_number)
        products_kreso = scrape_autokreso(part_number)
        products_autodoc = scrape_autodoc(part_number)
     
    except ValueError:
        return jsonify({
            "status": "error",
            "message": 'Open <a href="https://www.daparto.de/" class="error-link" target="_blank">Daparto</a> again, bad cookie. '
        }), 400

    products = products_kreso + products_impex + products_autodoc + products_daparto

    sorted_products = sorted(products, key=lambda x: float(x['price'].replace('€', '').strip()))

    if sorted_products:
        save_to_excel(sorted_products, sheet_name=f"p_{part_number}", filename=f"generated/parts_{date.today()}.xlsx")

    
    return jsonify({"status": "success", "message": "XLSX file generated."}), 200


if __name__ == "__main__":
    app.run(port=5000)
    print("Server is running on port 5000")
