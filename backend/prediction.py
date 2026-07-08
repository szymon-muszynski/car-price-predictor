import pandas as pd

def predict_car_price(car_data: dict, model, model_columns: list) -> float:
    df_input = pd.DataFrame(0, index=[0], columns=model_columns)
    
    df_input.at[0, 'Przebieg'] = car_data['przebieg']
    df_input.at[0, 'Pojemność skokowa'] = car_data['pojemnosc_skokowa']
    df_input.at[0, 'Moc'] = car_data['moc']
    df_input.at[0, 'Wiek'] = car_data['wiek']
    
    paliwo_col = f"Rodzaj paliwa_{car_data['rodzaj_paliwa']}"
    if paliwo_col in df_input.columns:
        df_input.at[0, paliwo_col] = 1
        
    skrzynia_col = f"Skrzynia biegów_{car_data['skrzynia_biegow']}"
    if skrzynia_col in df_input.columns:
        df_input.at[0, skrzynia_col] = 1
        
    marka_col = f"Marka_{car_data['marka']}"
    if marka_col in df_input.columns:
        df_input.at[0, marka_col] = 1
    elif 'Marka_Inne' in df_input.columns:
        df_input.at[0, 'Marka_Inne'] = 1
        
    wycena = model.predict(df_input)[0]
    
    return float(wycena)

def find_similar_cars(car_data: dict, knn_model, knn_scaler, knn_columns: list, df_ref: pd.DataFrame) -> list:
    df_input = pd.DataFrame(0, index=[0], columns=knn_columns)
    
    df_input.at[0, 'Przebieg'] = car_data['przebieg']
    df_input.at[0, 'Pojemność skokowa'] = car_data['pojemnosc_skokowa']
    df_input.at[0, 'Moc'] = car_data['moc']
    df_input.at[0, 'Wiek'] = car_data['wiek']
    
    paliwo_col = f"Rodzaj paliwa_{car_data['rodzaj_paliwa']}"
    if paliwo_col in df_input.columns:
        df_input.at[0, paliwo_col] = 1
        
    skrzynia_col = f"Skrzynia biegów_{car_data['skrzynia_biegow']}"
    if skrzynia_col in df_input.columns:
        df_input.at[0, skrzynia_col] = 1
        
    marka_col = f"Marka_{car_data['marka']}"
    if marka_col in df_input.columns:
        df_input.at[0, marka_col] = 1
    elif 'Marka_Inne' in df_input.columns:
        df_input.at[0, 'Marka_Inne'] = 1
        
    auto_scaled = knn_scaler.transform(df_input)
    
    odleglosci, indeksy = knn_model.kneighbors(auto_scaled)
    
    similar_cars = []
    for idx in indeksy[0]:
        auto = df_ref.iloc[idx]
        similar_cars.append({
            "tytul": auto['Tytuł'],
            "cena": float(auto['Cena']),
            "rocznik": int(auto['Rok produkcji']),
            "przebieg": int(auto['Przebieg']),
            "moc": int(auto['Moc']),
            "pojemnosc_skokowa": int(auto['Pojemność skokowa']), 
            "url": auto['URL']
        })
        
    return similar_cars