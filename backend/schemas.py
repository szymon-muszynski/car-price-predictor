from pydantic import BaseModel


class CarPredictionRequest(BaseModel):
    przebieg: int
    pojemnosc_skokowa: int
    moc: int
    wiek: int
    rodzaj_paliwa: str      
    skrzynia_biegow: str    
    marka: str              

class CarPredictionResponse(BaseModel):
    predicted_price: float
    currency: str = "PLN"