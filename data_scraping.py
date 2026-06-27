import requests
from bs4 import BeautifulSoup
import json
import random
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


scraped_cars = []

for i in range(1,30):

    URL = f"https://www.otomoto.pl/osobowe?page={i}"

    print(f"Łączenie z {URL}...")
    
    response = requests.get(URL, headers=HEADERS)
    
    if response.status_code == 200:
        print("Połączono pomyślnie! Rozpoczynam parsowanie HTML...\n")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', attrs={'data-id': True})
        
        print(f"Znaleziono {len(articles)} ogłoszeń na tej stronie.\n")
        
        for article in articles: 
            title_tag = article.find('h2')
            title = title_tag.text.strip() if title_tag else "Brak tytułu"
            
            price_tag = article.find('h3')
            price = price_tag.text.strip() if price_tag else "Brak ceny"
            
            mileage_tag = article.find('dd', attrs={'data-parameter': 'mileage'})
            mileage = mileage_tag.text.strip() if mileage_tag else "Brak przebiegu"
            
            year_tag = article.find('dd', attrs={'data-parameter': 'year'})
            year = year_tag.text.strip() if year_tag else "Brak roku"
            
            fuel_tag = article.find('dd', attrs={'data-parameter': 'fuel_type'})
            fuel = fuel_tag.text.strip() if fuel_tag else "Brak info o paliwie"
            
            gearbox_tag = article.find('dd', attrs={'data-parameter': 'gearbox'})
            gearbox = gearbox_tag.text.strip() if gearbox_tag else "Brak info o typie skrzyni"

            car_data = {
                "title": title,
                "price": price,
                "mileage": mileage,
                "year": year,   
                "fuel": fuel,
                "gearbox": gearbox
            }
            
            scraped_cars.append(car_data)
            
        print(f"Sukces! Zapisano {len(scraped_cars)} aut do pliku raw_cars.json")
        przerwa = random.uniform(1.5, 3.5)
        print(f"Czekam {przerwa:.2f} sekundy...")
        time.sleep(przerwa)
        

    else:
        print(f"Błąd połączenia! Kod błędu: {response.status_code}")
        
with open("raw_cars.json", "w", encoding="utf-8") as file:
    json.dump(scraped_cars, file, ensure_ascii=False, indent=4)