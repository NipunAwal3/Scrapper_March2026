# python -m pip install requests
# ==> get data from web (html, json, xml)
# python -m pip install beautifulsoup4
# ==> parse html

import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "http://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    # Set encoding explicitly to handle special characters correctly
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_ = "product_pod")

    all_books = []
    for book in books:
        title = book.h3.a['title']
        price_text = book.find('p', class_='price_color').text
        currency = price_text[0]
        price = float(price_text[1:])
        all_books.append(
            {
                "title": title,
                "price": price,
                "currency": currency,
            }
        )
    return all_books

all_books = scrape_books(url)

with open("books.json", "w", encoding="utf-8") as f:
    import json

    json.dump(all_books, f, ensure_ascii=False, indent=4)

import csv

with open("books.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "currency"])
    writer.writeheader()
    writer.writerows(all_books)