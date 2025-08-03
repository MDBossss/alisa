from flask import Flask, request, jsonify
from flask import send_from_directory
import os
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

    filename = f"parts_{date.today()}.xlsx"
    if sorted_products:
        save_to_excel(sorted_products, sheet_name=f"p_{part_number}", filename=f"generated/{filename}")

    backend_url = "http://localhost:5000"
    download_link = f'{backend_url}/download/{filename}'
    
    return jsonify({"status": "success", "message": f'XLSX file generated. <a href="{download_link}" class="success-link" target="_blank">Download here</a>'}), 200


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'generated'), filename, as_attachment=True)

if __name__ == "__main__":
    app.run(port=5000)
    print("Server is running on port 5000")
