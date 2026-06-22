Car Price Predictor (W trakcie tworzenia / WIP)
Celem tego projektu jest zbudowanie kompleksowego systemu (End-to-End) do przewidywania cen samochodów używanych. Projekt ma na celu przejście przez pełen cykl pracy z danymi: od samodzielnego pozyskania surowych ofert z internetu, przez inżynierię danych i eksperymenty z modelami Machine Learning, aż po wystawienie gotowego modelu przez API i podpięcie go pod prosty interfejs w React.

🎯 Główne założenia i plan projektu
Projekt jest podzielony na cztery etapy, które będą realizowane po kolei:

1. Ekstrakcja danych (Web Scraping)
Cel: Zbudowanie skryptu pobierającego aktualne ogłoszenia motoryzacyjne z wybranych portali.

Zakres: Pobranie atrybutów takich jak: marka, model, rocznik, przebieg, rodzaj paliwa, pojemność silnika oraz cena docelowa.

Technologie: Python (BeautifulSoup / Scrapy).

2. Przetwarzanie danych (ETL & Feature Engineering)
Cel: Oczyszczenie surowych danych pobranych ze strony (parsowanie stringów na wartości liczbowe, obsługa braków w ogłoszeniach).

Zakres: Przygotowanie skryptu, który transformuje zeskrapowane dane i ładuje je do lokalnej bazy danych gotowej do analizy.

Technologie: Pandas, NumPy, SQLite / PostgreSQL.

3. Modelowanie i Eksperymenty (Machine Learning)
Cel: Wyłonienie modelu, który najdokładniej przewiduje cenę auta na podstawie cech.

Zakres: Eksploracyjna analiza danych (EDA) w notatnikach Jupyter. Zbadanie i porównanie skuteczności różnych podejść – od klasycznej regresji liniowej, przez modele oparte na drzewach (np. Random Forest, XGBoost), po proste sieci neuronowe.

Technologie: Scikit-learn, XGBoost, PyTorch/TensorFlow (opcjonalnie).

4. Wdrożenie (Backend + Frontend)
Cel: Udostępnienie najlepszego modelu w formie działającej mini-aplikacji webowej.

Zakres: * Backend: Napisanie API w Pythonie, które wczytuje zapisany model (.pkl / .onnx) i przyjmuje zapytania z parametrami samochodu, zwracając estymowaną cenę.

Frontend: Stworzenie prostego formularza dla użytkownika w przeglądarce, który odpytuje API i wyświetla wynik.

Technologie: FastAPI (Python), React.js.

🛠️ Planowany stos technologiczny
Python, JavaScript

Scikit-learn, Pandas, BeautifulSoup

FastAPI, React.js

SQLite

📈 Status projektu
Projekt znajduje się we wczesnej fazie rozwoju (planowanie i budowa modułu scrapującego). Skrypty oraz struktura katalogów będą dodawane na bieżąco.