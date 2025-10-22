import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import random
import html 

BASE_URL = "http://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def make_session():
    """Creates a requests session with retry logic."""
    session = requests.Session()
    retries = Retry(
        total=5,                # retry up to 5 times
        backoff_factor=0.5,     # delay between retries: 0.5, 1, 2, 4, ...
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(HEADERS)
    return session


def random_delay(min_delay=1, max_delay=3):
    
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)


def get_soup(session, url):
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def extract_books(soup):
    books = soup.find_all("article", class_="product_pod")
    data = []

    for book in books:
        title = book.h3.a["title"].strip()

        price = book.find("p", class_="price_color").text.strip()
        
        price = html.unescape(price).encode('latin1', errors='ignore').decode('utf-8', errors='ignore')

        availability = book.find("p", class_="instock availability").text.strip()
        availability = html.unescape(availability).encode('latin1', errors='ignore').decode('utf-8', errors='ignore')

        data.append({
            "Title": title,
            "Price": price,
            "Availability": availability
        })

    return data


def get_next_page(soup):
    
    next_button = soup.find("li", class_="next")
    if next_button:
        return next_button.a["href"]
    return None


def scrape_all_pages(start_url):
    
    session = make_session()
    all_books = []
    current_url = start_url
    page = 1

    print("📚 Starting scrape from:", current_url)

    while True:
        soup = get_soup(session, current_url)
        if not soup:
            print("❌ Skipping this page (failed to load).")
            break

        books = extract_books(soup)
        all_books.extend(books)
        print(f"✅ Page {page}: Scraped {len(books)} books")

        next_page = get_next_page(soup)
        if not next_page:
            print("🏁 No more pages found.")
            break

        current_url = urljoin(current_url, next_page)
        page += 1
        random_delay(1, 2.5)  

    return all_books


def main():
    data = scrape_all_pages(BASE_URL)

    df = pd.DataFrame(data)
    df.to_csv("output.csv", index=False, encoding="utf-8-sig")
    df.to_excel("output.xlsx", index=False, engine="openpyxl")


    print(f"\n {len(df)} books and saved to output.csv")


if __name__ == "__main__":
    main()
