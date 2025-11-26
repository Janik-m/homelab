# Używamy oficjalnego obrazu Pythona
FROM python:3.11-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki aplikacji do kontenera
COPY . .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Otwórz port 5000
EXPOSE 5000

# Uruchom aplikację
CMD ["python", "app.py"]
