from mongoengine import connect, Document, StringField, DateTimeField, ReferenceField, ListField
from datetime import datetime
import json

# Połącz się z bazą danych MongoDB Atlas
connect(host="mongodb+srv://username:password@cluster0.mongodb.net/mydatabase?retryWrites=true&w=majority")


class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


def load_data_to_db():
    with open('authors.json', 'r') as file:
        authors_data = json.load(file)

    with open('quotes.json', 'r') as file:
        quotes_data = json.load(file)

    # Wczytywanie autorów do bazy danych
    authors_dict = {}
    for author_data in authors_data:
        born_date = datetime.strptime(author_data['born_date'], '%B %d, %Y') if author_data['born_date'] else None
        author = Author(
            fullname=author_data['fullname'],
            born_date=born_date,
            born_location=author_data['born_location'],
            description=author_data['description']
        )
        author.save()
        authors_dict[author.fullname] = author

    # Wczytywanie cytatów do bazy danych
    for quote_data in quotes_data:
        author = authors_dict.get(quote_data['author'])
        if author:
            quote = Quote(
                tags=quote_data['tags'],
                author=author,
                quote=quote_data['quote']
            )
            quote.save()


def search_quotes(queries):
    if queries.startswith('tags:'):
        tags = queries.replace('tags:', '').split(',')
        quotes = Quote.objects(tags__in=tags)
    elif queries.startswith('author:'):
        author_name = queries.replace('author:', '').strip()
        author = Author.objects(fullname=author_name).first()
        quotes = Quote.objects(author=author)
    else:
        quotes = Quote.objects(quote__icontains=queries)

    for quote in quotes:
        print(f'Author: {quote.author.fullname}')
        print(f'Quote: {quote.quote}')
        print(f'Tags: {quote.tags}')
        print()


if __name__ == '__main__':
    load_data_to_db()

    while True:
        query = input("Wpisz zapytanie (np. 'tags:change' lub 'author:Albert Einstein' lub 'world'): ")
        search_quotes(query)
