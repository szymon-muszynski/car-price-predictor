import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

URL = "https://www.otomoto.pl/osobowe"

print(f"Łączenie z {URL}...")

response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    print("Połączono pomyślnie! Rozpoczynam parsowanie HTML...\n")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = soup.find_all('article', attrs={'data-id': True})
    
    print(f"Znaleziono {len(articles)} ogłoszeń na tej stronie.\n")
    print("-" * 40)
    
    for article in articles[:15]:
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

        print(f"Auto: {title}")
        print(f"Cena: {price}")
        print(f"Skrzynia: {gearbox}")
        print(f"Rok: {year} | Przebieg: {mileage} | Paliwo: {fuel}")
        print("-" * 40)

else:
    print(f"Błąd połączenia! Kod błędu: {response.status_code}")