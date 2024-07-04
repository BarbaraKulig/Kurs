from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Author, Quote
from pymongo import MongoClient
from django.contrib.auth.models import User

def home(request):
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')


def migrate_mongodb_to_postgres():
    client = MongoClient('mongodb://localhost:27017/')
    mongodb_db = client['my_mongodb_database']

    # Przykład migracji autorów
    mongodb_authors = mongodb_db['authors']
    for mongodb_author in mongodb_authors.find():
        author = Author.objects.create(
            name=mongodb_author['name'],
            bio=mongodb_author['bio']
        )
        author.save()

    # Przykład migracji cytatów
    mongodb_quotes = mongodb_db['quotes']
    for mongodb_quote in mongodb_quotes.find():
        author_name = mongodb_quote['author_name']
        author = Author.objects.get(name=author_name)
        created_by = User.objects.get(username='admin')  # Ustaw użytkownika, który tworzy cytaty
        quote = Quote.objects.create(
            author=author,
            text=mongodb_quote['text'],
            created_by=created_by
        )
        quote.save()

    client.close()


# Uruchomienie migracji
if __name__ == '__main__':
    migrate_mongodb_to_postgres()
