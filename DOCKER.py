# Użyj obrazu bazowego Pythona
FROM python:3.10

# Ustaw katalog roboczy na /app
WORKDIR /app

# Skopiuj plik wymagany dla Asystenta Osobistego do katalogu roboczego
COPY requirements.txt .

# Zainstaluj wymagane pakiety
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj wszystkie pliki źródłowe do katalogu roboczego
COPY . .

# Uruchom Asystenta Osobistego
CMD ["python", "assistant.py"]

#Budowanie obrazu Dockerowego
docker build -t personal_assistant .

# Możliwość utworzenia nowego kontenera
docker run -d --name personal_assistant_container personal_assistant
