import requests
from bs4 import BeautifulSoup
import json
import time
import random

time_start = time.time()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

scraped_cars = []
t_start = time.time()

for i in range(1, 500):
    URL = f"https://www.otomoto.pl/osobowe?page={i}"
    print(f"Pobieranie strony {i}...")
    
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Błąd HTTP na stronie {i}: {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    
    if not next_data_script:
        print("Nie znaleziono __NEXT_DATA__. Pomijam stronę.")
        continue

    try:
        json_data = json.loads(next_data_script.string)
        
        # Nawigujemy po strukturze do cache'u GraphQL (urqlState)
        urql_state = json_data.get('props', {}).get('pageProps', {}).get('urqlState', {})
        
        for cache_key, cache_value in urql_state.items():
            if 'data' in cache_value and isinstance(cache_value['data'], str):
                # Dane GraphQL są w Otomoto... kolejnym zagnieżdżonym JSON-em (jako tekst)
                inner_data = json.loads(cache_value['data'])
                
                if 'advertSearch' in inner_data:
                    edges = inner_data['advertSearch'].get('edges', [])
                    
                    for edge in edges:
                        node = edge.get('node', {})
                        
                        url = node.get('url')
                        title = node.get('title')
                        price = node.get('price', {}).get('amount', {}).get('value')
                        currency = node.get('price', {}).get('amount', {}).get('currencyCode')
                        
                        raw_params = node.get('parameters', [])
                        params = {p['key']: p['displayValue'] for p in raw_params}
                        
                        
                        car_info = {
                            "Tytuł": title,
                            "Cena": f"{price} {currency}" if price else "Brak",
                            "URL": url,
                            "Rok produkcji": params.get('year', 'Brak'),
                            "Przebieg": params.get('mileage', 'Brak'),
                            "Pojemność skokowa": params.get('engine_capacity', 'Brak'),
                            "Moc": params.get('engine_power', 'Brak'),          
                            "Rodzaj paliwa": params.get('fuel_type', 'Brak'),
                            "Skrzynia biegów": params.get('gearbox', 'Brak')
                        }
                        
                        scraped_cars.append(car_info)
                        
    except Exception as e:
        print(f"Błąd analizy strony {i}: {e}")
        
    przerwa = random.uniform(1.5, 2.5)
    print(f"Pobieranie zakończone -> czekam {przerwa} sekund\n")
    time.sleep(przerwa) 

print(f"\nSukces! Zebrano {len(scraped_cars)} ogłoszeń aut w {(time.time() - t_start):.2f} sekund!")

with open("../backend/data/raw/fast_cars_data.json", "w", encoding="utf-8") as f:
    json.dump(scraped_cars, f, ensure_ascii=False, indent=4)
    
time_end = time.time()

print(f"Calosc zajela {time_end - time_start} sekund")