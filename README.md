# 🚗 Car Price Predictor (W trakcie tworzenia / WIP)

**🌐 Live Demo: [Kliknij tutaj, aby przetestować aplikację na żywo!](https://car-price-frontend-jy6q.onrender.com/)**

Celem tego projektu jest zbudowanie kompleksowego systemu (End-to-End) do przewidywania cen samochodów używanych. Projekt ma na celu przejście przez pełen cykl pracy z danymi: od samodzielnego pozyskania surowych ofert z internetu, przez inżynierię danych i eksperymenty z modelami Machine Learning, aż po wystawienie gotowego modelu przez API i podpięcie go pod prosty interfejs w React.

<p align="center">
  <img width="733" height="834" alt="image" src="https://github.com/user-attachments/assets/74df8a21-ab83-4cf2-bda1-f63099952622" />
</p>

*Uwaga: Główny plik z surowymi danymi (ze względu na duży rozmiar) nie jest wgrywany do repozytorium.*

## 🎯 Główne założenia i plan projektu

Projekt jest podzielony na cztery etapy:

### 1. Ekstrakcja danych (Web Scraping) - ✅ *Zrealizowano*

- **Cel:** Zbudowanie skryptu pobierającego aktualne ogłoszenia motoryzacyjne z portalu Otomoto.
- **Wdrożenie:** Napisano skrypt (`fast_scraping.py`) iterujący przez 500 stron serwisu Otomoto, który pobiera kilkanaście tysięcy unikalnych ofert. Zamiast tradycyjnego parsowania struktury HTML, skrypt wydobywa dane bezpośrednio z ukrytego cache'u GraphQL (obiekt JSON z tagu `__NEXT_DATA__`), co zapewnia dużą stabilność i szybkość.
- **Zakres:** Pobranie atrybutów takich jak: marka, rocznik, przebieg, rodzaj paliwa, pojemność silnika, moc, skrzynia biegów oraz cena docelowa. Są to cechy dostępne z poziomu listy dostępnej pod linkiem https://www.otomoto.pl/osobowe?page=2, gdzie `?page=2` oznacza numer strony, dlatego też w modelu nie uwzględniono dokładnego modelu samochodu. W przyszłości planowane jest rozwinięcie programu o uwzględnianie modelu pojazdu.
- **Technologie:** Python (`requests`, `BeautifulSoup`, `json`).

### 2. Przetwarzanie danych (ETL & Feature Engineering) - ✅ *Zrealizowano*

- **Cel:** Oczyszczenie surowych danych pobranych ze strony i przekształcenie ich w format gotowy do trenowania algorytmów.
- **Wdrożenie:**
  - Usunięcie braków danych (NaN) oraz ekstremalnie rzadkich grup (np. napęd wodorowy).
  - Oczyszczenie ciągów znaków (usunięcie "PLN", "km", "cm3") i konwersja na typy liczbowe.
  - **Filtrowanie domenowe (Outliery):** Odrzucenie anomalii na podstawie logiki motoryzacyjnej (np. zablokowanie aut starszych niż 1990 rok, cen powyżej 800 tys. PLN czy przebiegów powyżej 700 tys. km).
  - **Inżynieria Cech:** Wyciągnięcie nazwy marki bezpośrednio z tytułu ogłoszenia, zamiana rocznika na wiek pojazdu w latach, oraz pogrupowanie rzadkich marek w jedną kategorię "Inne".
  - Przygotowanie maszyny do wczytywania zmiennych kategorycznych poprzez One-Hot Encoding.
- **Technologie:** Pandas, NumPy.

### 3. Modelowanie i Eksperymenty (Machine Learning) - ✅ *Zrealizowano*

- **Cel:** Wyłonienie modelu, który najdokładniej przewiduje cenę auta na podstawie cech.
- **Wdrożenie:** Przeprowadzono gruntowne eksperymenty, sprawdzając jak różne architektury radzą sobie z wyceną:
  1. **Klasyczna Regresja Liniowa:** Użyta jako model bazowy (Baseline) ze skutecznością na poziomie ~70.5% (R²).
  2. **Regresja Wielomianowa:** Zastosowano `Pipeline` i `ColumnTransformer`, ograniczając generowanie wielomianów i użycie `StandardScaler` wyłącznie do zmiennych ciągłych, co pozwoliło uniknąć wybuchu wymiarowości zdefiniowanej przez One-Hot Encoding.
  3. **Lasy Losowe (Random Forest):** Zoptymalizowano hiperparametry modelu (m.in. głębokość i liczbę aut w liściach blokującą szum) za pomocą algorytmu `RandomizedSearchCV`.
  4. **Gradient Boosted Trees (GBT):** Wdrożono model działający sekwencyjnie i korygujący trudne przypadki wycen.
  5. **Model Finałowy (Ensembling):** Połączono siły najlepszych modeli (Wielomianowego, RF oraz GBT) za pomocą narzędzia `StackingRegressor`. Nadzorujący Meta-Model (Regresja Liniowa) waży predykcje poszczególnych architektur, co pozwoliło na podbicie ostatecznej skuteczności do blisko 89.7% (R²) na zbiorze testowym.
- **Zapis modelu:** Wyuczony model (wraz ze skalerami i całym pipeline'em) oraz lista kolumn zostały zrzucone do plików `.pkl` za pomocą biblioteki `joblib`, co pozwala na ich bezproblemowe ładowanie po stronie serwera.
- **Technologie:** Scikit-learn, Pandas.

### 4. Wdrożenie (Backend + Frontend) - ✅ *Zrealizowano (MVP)*

- **Cel:** Udostępnienie najlepszego modelu w formie działającej aplikacji webowej.
- **Wdrożenie:**
  - **Backend (FastAPI):** Napisano API w Pythonie, które ładuje model z pliku `.pkl` do pamięci. Endpoint `/predict` przyjmuje parametry od użytkownika, automatycznie tworzy wektor z zerami i jedynkami (One-Hot Encoding w locie, na podstawie zapisanej struktury kolumn) i zwraca predykcję.
  - **Frontend (React + Vite + TypeScript):** Zbudowano formularz pozwalający użytkownikowi wpisać parametry auta, który następnie odpytuje backend i wyświetla szacowaną wartość w PLN.
  - **Rekomendacje kNN (Podobne oferty):** Wytrenowano dodatkowy model `NearestNeighbors` (Scikit-learn) na tej samej bazie ofert, który dla podanych przez użytkownika parametrów auta wyszukuje 5 najbardziej zbliżonych, prawdziwych ogłoszeń (na podstawie przebiegu, mocy, pojemności silnika, wieku, marki itp.). Wyniki wyświetlane są w formie klikalnych kart pod wyceną — kliknięcie w kartę przenosi użytkownika bezpośrednio do oryginalnego ogłoszenia, co buduje zaufanie do predykcji modelu.
- **Technologie:** FastAPI (Python), React, Vite, TypeScript.
<p align="center">
<img width="755" height="863" alt="image" src="https://github.com/user-attachments/assets/22e01dd7-97b6-4c2b-8952-eab5b775450f" />
</p>

## 🚀 Dalszy plan rozwoju (Roadmap)

Kolejne kroki, które zaplanowałem w rozwoju aplikacji:

1. ~~**Deploy:** Wystawienie backendu i frontendu na platformę hostingową.~~
2. **Wykres spadku wartości:** Dodanie symulacji (wykresu), która będzie pokazywać, jak wpisane przez użytkownika auto będzie tracić na wartości przez kolejne np. 5 lat.

## ⚙️ Uruchomienie lokalnie

Aby odpalić projekt u siebie:

**1. Backend:**

W głównym folderze uruchom serwer FastAPI (pamiętaj o zainstalowaniu zależności i byciu w wirtualnym środowisku):

```bash
uvicorn main:app --reload
```

**2. Frontend:**

Wejdź do folderu z aplikacją React, zainstaluj paczki i odpal serwer deweloperski:

```bash
npm install
npm run dev
```

## 🛠️ Stos technologiczny

- Python, JavaScript, TypeScript
- Scikit-learn, Pandas, NumPy, BeautifulSoup
- FastAPI, React.js, Vite

## 📈 Status projektu

Postawiono i wdrożono do chmury MVP aplikacji: backend przyjmujący zapytania i zasilany wytrenowanym modelem regresyjnym oraz modelem kNN do wyszukiwania podobnych ofert, a także prosty frontend w React z klikalnymi kartami rekomendacji. Trwają prace nad rozbudową funkcjonalności zgodnie z roadmapą.
