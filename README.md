<img width="128" height="128" alt="image" src="https://github.com/user-attachments/assets/cfcec8e3-ce53-4243-b4ec-c858be7fadf2" />

# ALISA - Car Parts Price Comparison Tool

**ALISA** is an open-source tool for quickly comparing car part prices across multiple European retailers. Enter one or more part numbers, and ALISA will automatically scrape prices and availability from several online shops, then generate a downloadable Excel file with all results, sorted by price.

---

<img width="11992" height="4840" alt="image" src="https://github.com/user-attachments/assets/152b0c20-def8-4900-a921-5824d6f2a91f" />



## Features

- 🔍 **Multi-site price comparison**: Scrapes prices for your part numbers from Autodoc, Daparto, Impex, and Autokrešo.
- 📝 **Bulk search**: Enter multiple part numbers at once (comma or space separated).
- 📊 **Excel export**: Results are saved in a formatted XLSX file, with a separate sheet for each part number.
- 🛡️ **Bypasses anti-bot protections**: Uses Cloudscraper and browser extension to handle Cloudflare and CAPTCHA for Daparto.
- 🖥️ **Simple web interface**: Chrome extension popup for easy input and download.
- ⚡ **Fast and extensible**: Modular Python scrapers for each site, easy to add more sources.

---

## Supported Sites

- [Autodoc](https://www.autodoc.de/) (no CAPTCHA)
- [Daparto](https://www.daparto.de/) (Cloudflare + checkbox CAPTCHA, handled via extension)
- [Impex](https://impexautodijelovi.hr/) (no CAPTCHA)
- [Autokrešo](https://www.autokreso.hr/) (no CAPTCHA)

---

## Windows EXE Build (GitHub Actions)

A GitHub Actions workflow is set up to build a standalone Windows executable (`.exe`) from the Python code using PyInstaller. To build the EXE, trigger the workflow manually from the GitHub Actions tab. The resulting EXE can be downloaded from the workflow run's "Artifacts" section on GitHub.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/MDBossss/alisa.git
   cd alisa
   ```

2. **Install Python dependencies**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **(Optional) Install Chrome extension**

   - Go to `chrome://extensions` in your browser.
   - Enable "Developer mode".
   - Click "Load unpacked" and select the `extension/` folder.

4. **Start the backend server**
   ```bash
   python main.py
   ```

---

## How to Use

1. **Open the Chrome extension popup**
2. Enter one or more part numbers (comma or space separated), e.g.:
   ```
   2106980854, 2106980754, 2106908125
   ```
3. Click **Find Parts**
4. Wait for scraping to finish. A download link for the Excel file will appear if successful.
5. Click the link to download your results.

**Note:**

- For Daparto, you must be logged in and have a valid Cloudflare cookie. If you see an error, open [daparto.de](https://www.daparto.de/) in your browser and try again.
- The backend server must be running locally for the extension to work.

---

## Project Structure

- `main.py` — Flask backend API, orchestrates scraping and Excel export
- `scrapers/` — Individual Python scrapers for each supported site
- `utils/` — Helper modules for price cleaning, HTTP requests, Excel formatting, etc.
- `extension/` — Chrome extension for user input and cookie handling
- `generated/` — Output folder for generated Excel files

---

## Contributing

Pull requests and suggestions are welcome! See the code for modular scraper examples.

---

## License

MIT
