import requests
from bs4 import BeautifulSoup
import json
import random
import time
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

OUTPUT_FILE = "test_raw_cars_detailed.json"
LINKS_FILE = "test_car_links.json"

print("=== ETAP 2: POBIERANIE SZCZEGÓŁÓW (EXTRACTION) ===")

# 1. Wczytanie bazy linków
if not os.path.exists(LINKS_FILE):
    print(f"Błąd: Nie znaleziono pliku {LINKS_FILE}. Uruchom najpierw step1_harvest.py.")
    exit()

with open(LINKS_FILE, "r", encoding="utf-8") as file:
    car_listings = json.load(file)

print(f"Wczytano {len(car_listings)} linków do sprawdzenia.")

# 2. Wczytanie dotychczasowego progresu (jeśli istnieje)
scraped_cars = []
scraped_urls = set()

if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        try:
            scraped_cars = json.load(file)
            # Tworzymy zbiór URLi, które już mamy w bazie, żeby ich nie powtarzać
            scraped_urls = {car["URL"] for car in scraped_cars}
            print(f"Znaleziono zapisany postęp: {len(scraped_cars)} aut już jest w pliku. Pomijam je.")
        except json.JSONDecodeError:
            print("Plik docelowy jest pusty lub uszkodzony. Zaczynam od zera.")

t_start = time.time()

# 3. Pętla główna (np. sprawdzamy pierwsze 3000)
for idx, car in enumerate(car_listings[:5], 1):
    
    # Pomijamy, jeśli to auto już zostało pobrane w poprzedniej sesji
    if car['url'] in scraped_urls:
        continue
        
    print(f"[{idx}/{len(car_listings[:3000])}] Skanowanie: {car['title']}...")
    
    try:
        response = requests.get(car['url'], headers=HEADERS)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            def get_detail(label_name):
                label_p = soup.find(lambda tag: tag.name == 'p' and label_name == tag.text.strip())
                if label_p:
                    value_p = label_p.find_next('p')
                    if value_p:
                        return value_p.text.strip()
                return "Brak"

            detailed_data = {
                "Tytuł": car['title'],
                "Cena": car['price'],
                "Marka pojazdu": get_detail("Marka pojazdu"),
                "Model pojazdu": get_detail("Model pojazdu"),
                "Rok produkcji": get_detail("Rok produkcji"),
                "Przebieg": get_detail("Przebieg"),
                "Pojemność skokowa": get_detail("Pojemność skokowa"),
                "Moc": get_detail("Moc"),
                "Rodzaj paliwa": get_detail("Rodzaj paliwa"),
                "Skrzynia biegów": get_detail("Skrzynia biegów"),
                "Typ nadwozia": get_detail("Typ nadwozia"),
                "Liczba drzwi": get_detail("Liczba drzwi"),
                "Liczba miejsc": get_detail("Liczba miejsc"),
                "Kolor": get_detail("Kolor"),
                "URL": car['url']
            }
            
            # Dodajemy do listy pamięci podręcznej
            scraped_cars.append(detailed_data)
            scraped_urls.add(car['url'])
            
            # BIEŻĄCY ZAPIS - chroni przed utratą danych w przypadku przerwania!
            with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
                json.dump(scraped_cars, file, ensure_ascii=False, indent=4)
                
        else:
            print(f"Błąd (Kod: {response.status_code}): {car['url']}")
            
    except Exception as e:
        print(f"Wystąpił błąd podczas skanowania {car['url']}: {e}")
        
    # Odstęp czasowy, żeby nie dostać bana
    przerwa = random.uniform(1.5, 3.5)
    print(f"  -> Zapisano. Czekam {przerwa:.2f} s...")
    time.sleep(przerwa)

t_end = time.time()
print(f"\nSukces! Proces zakończony. Całość zajęła: {t_end - t_start:.2f} s")