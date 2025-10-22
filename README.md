
# BookstoScrape Web Scraper

A **Python-based web scraper** that extracts book titles, prices, and availability information from the website [Books to Scrape](http://books.toscrape.com/).  
The script demonstrates **real-world web scraping techniques** including random delays, retry handling, and data export to Excel with UTF-8 encoding.

---

## Features

- Scrapes book **titles**, **prices**, and **availability**  
- Implements **retry logic** for failed requests  
- Adds **random delays** to simulate human browsing  
- Cleans and encodes text properly (removes `Â£` and similar issues)  
- Exports data to **CSV (UTF-8)** **Excel (output.xlsx)**


---

## Technologies Used

- **Python 3.x**
- **Requests**
- **BeautifulSoup (bs4)**
- **Pandas**
- **openpyxl**
- **urllib3 (for retry handling)**

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/Bookstoscrape.git
   cd Bookstoscrape
