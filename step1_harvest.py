import requests
from bs4 import BeautifulSoup
import json
import random
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

car_listings = []
t_start = time.time()

print("=== ETAP 1: ZBIERANIE LINKÓW (HARVESTING) ===")
# Ustaw zakres stron, który Cię interesuje
for i in range(1, 5):
    URL = f"https://www.otomoto.pl/osobowe?page={i}"
    print(f"Pobieranie listy aut z: {URL}...")
    
    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', attrs={'data-id': True})
        
        for article in articles:
            link_tag = article.find('a', href=True)
            url = link_tag['href'] if link_tag else None
            
            title_tag = article.find('h2')
            title = title_tag.text.strip() if title_tag else "Brak tytułu"
            
            price_tag = article.find('h3')
            price = price_tag.text.strip() if price_tag else "Brak ceny"
            
            if url:
                car_listings.append({
                    "url": url,
                    "title": title,
                    "price": price
                })
    else:
        print(f"Błąd połączenia na stronie {i}! Kod: {response.status_code}")
        
    time.sleep(random.uniform(1.0, 2.0))

print(f"\nZebrano {len(car_listings)} unikalnych linków do aut.")

# Zapis zebranych linków do pliku
with open("test_car_links.json", "w", encoding="utf-8") as file:
    json.dump(car_listings, file, ensure_ascii=False, indent=4)

t_end = time.time()
print(f"Zakończono. Czas działania: {t_end - t_start:.2f} s")