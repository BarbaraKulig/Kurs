import sqlite3
from faker import Faker
import random

# Połączenie z bazą danych
conn = sqlite3.connect('szkola.db')
cursor = conn.cursor()

# Tworzenie tabel
cursor.execute('''CREATE TABLE IF NOT EXISTS Uczniowie (
                    id INTEGER PRIMARY KEY,
                    imie TEXT,
                    nazwisko TEXT,
                    grupa_id INTEGER,
                    FOREIGN KEY (grupa_id) REFERENCES Grupy(id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Grupy (
                    id INTEGER PRIMARY KEY,
                    nazwa TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Nauczyciele (
                    id INTEGER PRIMARY KEY,
                    imie TEXT,
                    nazwisko TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Przedmioty (
                    id INTEGER PRIMARY KEY,
                    nazwa TEXT,
                    nauczyciel_id INTEGER,
                    FOREIGN KEY (nauczyciel_id) REFERENCES Nauczyciele(id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Oceny (
                    id INTEGER PRIMARY KEY,
                    uczniowie_id INTEGER,
                    przedmioty_id INTEGER,
                    ocena INTEGER,
                    data_oceny DATE,
                    FOREIGN KEY (uczniowie_id) REFERENCES Uczniowie(id),
                    FOREIGN KEY (przedmioty_id) REFERENCES Przedmioty(id)
                )''')

# Wypełnienie danymi losowymi
fake = Faker()

# Generowanie grup
grupy = ['A', 'B', 'C']
for grupa in grupy:
    cursor.execute("INSERT INTO Grupy (nazwa) VALUES (?)", (grupa,))

# Generowanie nauczycieli
for _ in range(3):
    imie = fake.first_name()
    nazwisko = fake.last_name()
    cursor.execute("INSERT INTO Nauczyciele (imie, nazwisko) VALUES (?, ?)", (imie, nazwisko))

# Tworzenie przedmiotów i przypisanie nauczycieli
przedmioty = ['Matematyka', 'Fizyka', 'Chemia', 'Biologia', 'Historia', 'Geografia', 'Informatyka']
for przedmiot in przedmioty:
    nauczyciel_id = random.randint(1, 3)  # Losowy wybór nauczyciela
    cursor.execute("INSERT INTO Przedmioty (nazwa, nauczyciel_id) VALUES (?, ?)", (przedmiot, nauczyciel_id))

# Generowanie uczniów i przypisanie do grup
for _ in range(30):
    imie = fake.first_name()
    nazwisko = fake.last_name()
    grupa_id = random.randint(1, len(grupy))  # Losowy wybór grupy
    cursor.execute("INSERT INTO Uczniowie (imie, nazwisko, grupa_id) VALUES (?, ?, ?)", (imie, nazwisko, grupa_id))


# Wybór wszystkich uczniów i przedmiotów
cursor.execute("SELECT id FROM Uczniowie")
uczniowie = cursor.fetchall()

cursor.execute("SELECT id FROM Przedmioty")
przedmioty = cursor.fetchall()

# Liczba ocen do wygenerowania dla każdego ucznia
liczba_ocen = 20

# Generowanie ocen dla każdego ucznia i przedmiotu
for ucznik in uczniowie:
    for przedmiot in przedmioty:
        for _ in range(liczba_ocen):
            ocena = random.randint(1, 6)  # Losowa ocena od 1 do 6
            data_oceny = '2024-04-20'  # Zakładamy datę oceny
            cursor.execute("INSERT INTO Oceny (uczniowie_id, przedmioty_id, ocena, data_oceny) VALUES (?, ?, ?, ?)",
                           (ucznik[0], przedmiot[0], ocena, data_oceny))

# Zapisanie zmian w bazie danych
conn.commit()

# Zamknięcie połączenia
conn.close()
