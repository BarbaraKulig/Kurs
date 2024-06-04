import json

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def scrape_quotes():
    quotes_data = []
    authors_data = {}
    page = 1

    while True:
        url = f"{BASE_URL}/page/{page}/"
        soup = get_soup(url)

        quotes = soup.select('.quote')
        if not quotes:
            break

        for quote in quotes:
            text = quote.select_one('.text').text.strip('“”')
            author_name = quote.select_one('.author').text
            tags = [tag.text for tag in quote.select('.tag')]

            # If author is not already scraped, scrape author's details
            if author_name not in authors_data:
                author_url = BASE_URL + quote.select_one('span a')['href']
                author_soup = get_soup(author_url)
                born_date = author_soup.select_one('.author-born-date').text
                born_location = author_soup.select_one('.author-born-location').text
                description = author_soup.select_one('.author-description').text.strip()

                authors_data[author_name] = {
                    'fullname': author_name,
                    'born_date': born_date,
                    'born_location': born_location,
                    'description': description
                }

            quotes_data.append({
                'quote': text,
                'author': author_name,
                'tags': tags
            })

        page += 1

    # Convert authors_data to list
    authors_list = list(authors_data.values())

    return quotes_data, authors_list

def save_to_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    quotes, authors = scrape_quotes()
    save_to_json('quotes.json', quotes)
    save_to_json('authors.json', authors)
