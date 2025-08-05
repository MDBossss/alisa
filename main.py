import os
import time

from flask import Flask, request, jsonify
from flask import send_from_directory
from flask_cors import CORS

from utils.xls_utils import save_to_excel
from utils.format_part_numbers import format_part_numbers
from datetime import date

from scrapers.autokreso_scraper import scrape_autokreso
from scrapers.impex_scraper import scrape_impex
from scrapers.autodoc_scraper import scrape_autodoc
from scrapers.daparto_scraper import scrape_daparto

# # example part number: 55183562,0532p5,6351fr

app = Flask(__name__)
CORS(app)

@app.route("/trigger", methods=["POST"])
def trigger():
    data = request.get_json()

    cf_clearance_cookie = data.get("cf_clearance_cookie")
    if not cf_clearance_cookie:
        return jsonify({"status": "error", "message": "Daparto Cloudflare cookie not received"}), 400
    
    part_numbers_string = data.get("part_number")
    if not part_numbers_string:
        return jsonify({"status": "error", "message": "Part number(s) is required"}), 400

    part_numbers = format_part_numbers(part_numbers_string)

    all_results = {}
    for part_number in part_numbers:
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
        all_results[part_number] = sorted_products
        time.sleep(1)  # 1 second delay between scrapes

    # Write all results to a single Excel file with multiple sheets
    filename = f"parts_{date.today()}.xlsx"
    excel_path = f"generated/{filename}"
    # Ensure the directory exists
    os.makedirs("generated", exist_ok=True)
    save_to_excel(all_results, filename=excel_path)

    backend_url = "http://localhost:5000"
    download_link = f'{backend_url}/download/{filename}'
    return jsonify({"status": "success", "message": f'XLSX file generated. <a href="{download_link}" class="success-link" target="_blank">Download here</a>'}), 200


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'generated'), filename, as_attachment=True)
    
if __name__ == "__main__":
    app.run(port=5000)
    print("Server is running on port 5000")
