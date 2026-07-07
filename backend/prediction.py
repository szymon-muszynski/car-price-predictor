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