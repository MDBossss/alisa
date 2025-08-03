from flask import Flask, request, jsonify
from flask_cors import CORS

# from utils.xls_utils import save_to_excel

# from scrapers.autokreso_scraper import scrape_autokreso
# from scrapers.impex_scraper import scrape_impex
# from scrapers.autodoc_scraper import scrape_autodoc
# from scrapers.daparto_scraper import scrape_daparto

# # example part number: 55183562 

# partNumber = 55183562

# products_impex = scrape_impex(partNumber)
# products_kreso = scrape_autokreso(partNumber)
# products_autodoc = scrape_autodoc(partNumber)
# products_daparto = scrape_daparto(partNumber)

# products = products_kreso + products_impex + products_autodoc + products_daparto

# sorted_products = sorted(products, key=lambda x: float(x['price'].replace('€', '').strip()))


# if sorted_products:
#     save_to_excel(sorted_products, sheet_name=partNumber, filename=f"parts_list.xlsx")
    
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


    # TODO: pass cookie and scrape by passed product ids

    
    return jsonify({"status": "success", "message": "XLSX file generated."}), 200


if __name__ == "__main__":
    app.run(port=5000)
    print("Server is running on port 5000")
