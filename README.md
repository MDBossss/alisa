# ALISA - Car Parts Price Comparison Tool

## Project Description

**alisa** is a web application designed to simplify the process of comparing car part prices. Users can input a list of part numbers, and the application will automatically scrape data from multiple online retailers, displaying a consolidated list of prices and availability in one place.

## How to Use

The application's core functionality is a text area where a user will enter a list of comma-separated part numbers.

**Example Input:**
```
2106980854,2106980754,2106908125
```

## Sites to Scrape

This project's success relies on building individual scraping scripts for the following websites:

### AUTODOC
- **Link:** https://www.autodoc.de/
- **Anti-Bot:** No CAPTCHA detected. ✅

### DAPARTO
- **Link:** https://www.daparto.de/
- **Anti-Bot:** Has a checkbox CAPTCHA. ⚠️

### IMPEX
- **Link:** https://impexautodijelovi.hr/
- **Anti-Bot:** No CAPTCHA detected. ✅

### AUTOKREŠO
- **Link:** https://www.autokreso.hr/
- **Anti-Bot:** No CAPTCHA detected. ✅

### INTERCARS
- **Link:** https://hr.intercars.com/
- **Anti-Bot:** No CAPTCHA detected. ✅

## Recommended Technologies

- **Scraper:** Use a combination of libraries. For the sites without CAPTCHAs, use `requests` and `BeautifulSoup`. For the site with a CAPTCHA, use `Playwright` to control a headless browser. Playwright is a modern and powerful tool that's often easier to set up than other options like Selenium.

- **Database:** Start with SQLite. It's a file-based database that's included with Python and requires no server setup, making it perfect for development. When you're ready to host the application, migrate to a more robust, server-based database like PostgreSQL or MongoDB.

- **Backend API:** You can build a simple backend API using a lightweight Python web framework like Flask to manage the scraping tasks and data storage.

- **Frontend:** Create the user interface and handle the communication with the backend API using a modern JavaScript library like React.

## Phases of Work

Based on the anti-bot status of each site, here is a suggested workflow to get started on the project:

- [ ] **Set up the development environment:** Install Python and core libraries like Flask, requests, BeautifulSoup, and Playwright. Set up the React development environment.

- [ ] **Plan the scraping logic:** Inspect the HTML structure of each site to identify the CSS selectors or XPATHs needed to extract part names, prices, and other data.

- [ ] **Build basic scrapers:** Create scripts for the sites without CAPTCHA: AUTODOC, IMPEX, AUTOKREŠO, and INTERCARS. These can use simple libraries like requests and BeautifulSoup.

- [ ] **Build the advanced scraper:** Develop the script for DAPARTO using a headless browser automation tool like Playwright to handle the checkbox CAPTCHA.

- [ ] **Set up the database:** Configure an SQLite database for local development to store the scraped data.

- [ ] **Build the backend API:** Create a simple Flask application to expose API endpoints for triggering the scraping tasks and retrieving the results from the database.

- [ ] **Build the front-end:** Create the user-facing application using React to interact with the Flask API and display the scraped data.

- [ ] **Plan for hosting:** Once the app is working locally, plan the migration to a production database (like PostgreSQL) and a hosting provider. Consider using an asynchronous task queue (like Celery) to run the scraping jobs in the background, keeping your web application responsive.
