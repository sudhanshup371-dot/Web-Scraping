import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target website
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

# Containers for scraped data
titles = []
prices = []
availabilities = []

# Scrape the first 3 pages for demo (can be more)
for page in range(1, 4):
    url = BASE_URL.format(page)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        # Title
        title = book.h3.a["title"]
        titles.append(title)

        # Price
        price = book.find("p", class_="price_color").text.strip()
        prices.append(price)

        # Availability
        availability = book.find("p", class_="instock availability").text.strip()
        availabilities.append(availability)

# Create DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Price": prices,
    "Availability": availabilities
})

# Save to CSV
df.to_csv("books_dataset.csv", index=False)

print("✅ Web scraping complete. Data saved to 'books_dataset.csv'")
